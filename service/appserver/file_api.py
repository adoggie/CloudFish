#coding:utf-8


__author__ = 'root'

import os,traceback,datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from lemon import webapi
import lemon.errors
import lemon.base
from lemon.utils.app import BaseAppServer

import model.django.core.models as core

from service.common.decorator import user_auth_token_check,server_ip_address_restrict

import cloudfish.base
import service.common.token as Token

from django.conf import settings
from django.core.servers.basehttp import FileWrapper
import mimetypes
from django.http import StreamingHttpResponse,HttpResponseForbidden


#
# import gevent.subprocess
# from gevent.fileobject import FileObject
#
# from poster.encode import multipart_encode
# from poster.streaminghttp import register_openers
# import urllib2



def get_temp_filename(purpose=''):
	tmpdir = BaseAppServer.instance().getConfig().get("tmpdir")
	filename = lemon.utils.misc.genUUID()
	filename =  u'%s/%s'%(tmpdir, filename.decode('utf-8'))
	return filename


def calc_file_digest(file,bufsize=1024*5,type='md5'):
	import hashlib
	m = hashlib.md5()
	try:
		# fp = FileObject( open(file,'rb'),'rb')
		fp = open(file,'rb')
		while True:
			data = fp.read(bufsize)
			if not data:break
			m.update(data)
		fp.close()
		return m.hexdigest()
	except:
		traceback.print_exc()
		return ''

def get_user_file_access_id(auf):
	from lemon.utils.misc import getdigest
	size = auf.file_size
	digest = auf.digest
	salt = auf.access_salt
	text = "%s$%s$%s"%(salt,size,digest)
	return getdigest( text )

def new_salt():
	from lemon.utils.misc import random_password
	return random_password()


def encrypt_file(filename,passwd):
	"""
	encrypt file and return new file
	:param filename:
	:param passwd:
	:return:
	"""
	from gevent.subprocess import  Popen,PIPE

	rc = -1
	target_des = get_temp_filename()+'.des'
	try:
		cmd = "tar -zcf  - %s | openssl des3 -salt -k %s | dd of=%s"%(filename,passwd,target_des)
		# cmd_list = cmd.split(' ')
		# rc =  gevent.subprocess.call(cmd_list)
		sub = Popen([cmd],stdout=PIPE,shell=True)
		out,err = sub.communicate()
		if not os.path.exists( target_des):
			target_des = ''
	except:
		traceback.print_exc()
		target_des = ''

	return target_des



def decrypt_file(filename,passwd):
	"""
	decrypt file and return new file
	:param filename:
	:param passwd:
	:return:
	"""
	from gevent.subprocess import  Popen,PIPE
	rc = -1
	target_file = get_temp_filename()
	try:
		cmd = "dd if=%s | openssl des3 -d -k %s | dd of=%s"%(filename,passwd,target_file)
		# cmd_list = cmd.split(' ')
		# rc =  gevent.subprocess.call(cmd_list)
		print cmd
		sub = Popen([cmd],stdout=PIPE,shell=True)
		out,err = sub.communicate()
		if not os.path.exists( target_file):
			target_file = ''
	except:
		traceback.print_exc()
		target_file = ''
	return target_file

def get_encrypt_password(user_id):
	rs = core.AppUser.objects.filter(id= user_id)
	if not rs:
		return ''
	user = rs[0]
	shadow = user.app.file_encrypt_shadow
	shadow = '111111'
	return shadow


def storage_post_file(request,filename):
	"""
	:param request:
	:param filename:
	:return:
	 	storage_id
	"""
	import swift
	user_storage_id = request.user.get('user_storage_id')
	# fr = FileObject(filename,'rb')
	fr = open(filename,'rb')
	container = request.user.get('app_container')
	filename = os.path.basename(filename)
	print 'container name:',container
	storage_id = swift.create_user_file(container,user_storage_id,filename,fr)

	return storage_id


def storage_delete_file(request,storage_id):
	import swift
	container = request.user.get('app_container')
	swift.delete_user_file(container,storage_id)
	return True


def storage_get_file(request,storage_id):
	import swift
	filename = get_temp_filename()
	container = request.user.get('app_container')
	content = swift.get_user_file( container,storage_id)
	# fp = FileObject( filename,'wb')
	fp = open(filename,'wb')
	fp.write( content)
	fp.close()
	return filename

@csrf_exempt
@user_auth_token_check
def create_file(request):
	"""
		load file
		encrypt file
		save to swift
		return storage_id
	"""
	cr = webapi.SuccCallReturn()
	try:
		tmpdir = BaseAppServer.instance().getConfig().get("tmpdir")
		for name,file in request.FILES.items():
			upload_filename = file.name
			filename = lemon.utils.misc.genUUID()
			filename =  u'%s/%s'%(tmpdir, filename.decode('utf-8'))

			# fw = FileObject(open(filename,'wb'),'wb')

			fw = open(filename,'wb')

			file_size = 0
			# c = file.read()
			for chunk in file.chunks():
				file_size += len(chunk)
				fw.write( chunk)
			fw.close()

			digest = calc_file_digest(filename)

			passwd = get_encrypt_password(request.user.get('id'))
			enable = BaseAppServer.instance().getConfig().get('encrypt_enable',False)
			if enable:
				filename = encrypt_file(filename,passwd)
			if not filename:
				return webapi.FailCallReturn(lemon.errors.ErrorDefs.InternalException,u'encrypt file failed')

			storage_id = storage_post_file(request,filename)


			user = core.AppUser.objects.get(id=request.user.get('id'))
			auf = core.AppUserFile()
			auf.user = user
			auf.create_time = datetime.datetime.now()
			auf.storage_id = storage_id
			auf.file_name = upload_filename
			auf.file_size = file_size
			auf.digest = digest
			auf.access_salt = new_salt()
			auf.access_id = get_user_file_access_id(auf)
			auf.save()

			cr.assign(auf.access_id)

			log = core.LogAppUserAction(
				user= request.user.get('user_id'),
				user_role=request.user.get('node_type'),
				issue_time=datetime.datetime.now(),
				action = cloudfish.base.AppUserActionType.CLIENT_USER_CREATE_FILE,
				target = auf.file_name,
				detail = u'file:%s size:%s'%(auf.file_name,auf.file_size)
			)
			log.save()
			break
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn( lemon.errors.ErrorDefs.InternalException)
	return cr.httpResponse()



@csrf_exempt
@user_auth_token_check
def get_file(request):
	"""
	"""
	cr = webapi.SuccCallReturn()
	try:
		file_id = webapi.GET(request,'id')
		rs = core.AppUserFile.objects.filter(user__id=request.user.get('id'),access_id=file_id)
		if not rs:
			return webapi.FailCallReturn(lemon.errors.ErrorDefs.ObjectNotExisted).httpResponse()
		auf = rs[0]

		filename = storage_get_file(request,auf.storage_id)

		passwd = get_encrypt_password(request.user.get('id'))

		enable = BaseAppServer.instance().getConfig().get('encrypt_enable',False)
		if enable:
			filename = decrypt_file(filename,passwd)

		log = core.LogAppUserAction(
				user= request.user.get('user_id'),
				user_role=request.user.get('node_type'),
				issue_time=datetime.datetime.now(),
				action = cloudfish.base.AppUserActionType.CLIENT_USER_GET_FILE,
				target = auf.file_name,
				detail = u'file:%s size:%s'%(auf.file_name,auf.file_size)
			)
		log.save()

		# fp = FileObject(filename,'rb')
		fp = open(filename,'rb')
		wrapper = FileWrapper(fp)
		content_type = mimetypes.guess_type(auf.file_name)[0]
		response = StreamingHttpResponse(wrapper, content_type=content_type)
		#response['Content-Disposition'] = u"attachment; filename=%s" % auf.file_name
		response['Content-Disposition'] = u"attachment; filename=_unkown_file_" 
		return response
	except:
		traceback.print_exc()
		# return webapi.FailCallReturn( lemon.errors.ErrorDefs.InternalException).httpResponse()
	return HttpResponseForbidden()


@csrf_exempt
@user_auth_token_check
def delete_file(request):
	"""
	"""
	cr = webapi.SuccCallReturn()
	try:

		if request.method != 'DELETE':
			return webapi.FailCallReturn(lemon.errors.ErrorDefs.ParameterIllegal).httpResponse()

		file_id = webapi.GET(request,'id')
		rs = core.AppUserFile.objects.filter(user__id=request.user.get('id'),access_id=file_id)
		if not rs:
			return webapi.FailCallReturn(lemon.errors.ErrorDefs.ObjectNotExisted)
		auf = rs[0]

		storage_id = auf.storage_id
		r = storage_delete_file(request,storage_id)
		if r :
			auf.delete()

		log = core.LogAppUserAction(
				user= request.user.get('user_id'),
				user_role=request.user.get('node_type'),
				issue_time=datetime.datetime.now(),
				action = cloudfish.base.AppUserActionType.CLIENT_USER_DELETE_FILE,
				target = auf.file_name,
				detail = u'file:%s size:%s'%(auf.file_name,auf.file_size)
			)
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn( lemon.errors.ErrorDefs.InternalException)
	return cr.httpResponse()


@csrf_exempt
@user_auth_token_check
def share_file(request):
	"""
	"""
	cr = webapi.SuccCallReturn()
	try:


		file_id = webapi.GET(request,'id')
		client_id = webapi.GET(request,'client_id')


		rs = core.AppUser.objects.filter(name = client_id,app__id = request.user.get('app_id'))
		if not rs:
			return webapi.FailCallReturn(lemon.errors.ErrorDefs.ObjectNotExisted).httpResponse()
		target_user = rs[0]

		if core.AppUserFile.objects.filter(user__id = target_user.id,access_id=file_id).count():
			return cr.httpResponse() # succ ,passed

		rs = core.AppUserFile.objects.filter(user__id=request.user.get('id'),access_id=file_id)
		if not rs:
			return webapi.FailCallReturn(lemon.errors.ErrorDefs.ObjectNotExisted).httpResponse()
		auf = rs[0]


		log = core.LogAppUserAction(
				user= request.user.get('user_id'),
				user_role=request.user.get('node_type'),
				issue_time=datetime.datetime.now(),
				action = cloudfish.base.AppUserActionType.CLIENT_USER_CREATE_FILE,
				target = auf.file_name,
				detail = u'share to: %s ,file:%s size:%s'%(target_user.name,auf.file_name,auf.file_size)
			)
		log.save()

		# allocate new instance
		auf.pk = None
		auf.user = target_user
		auf.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn( lemon.errors.ErrorDefs.InternalException)
	return cr.httpResponse()


class FileView(View):
	# http_method_names = ['post','get','delete']
	def post(self,request):
		# create file
		return create_file(request)

	def get(self,request):
		return get_file(request)

	def delete(self,request):
		return delete_file(request)
