#-- coding:utf-8 --

import traceback,threading,time,struct,os,os.path,shutil,distutils.dir_util,array,base64,zlib,struct,binascii
import datetime,json

import model.django.core.models as core
from django.views.decorators.csrf import csrf_exempt
import lemon
from lemon import webapi
from lemon.errors import ErrorDefs
from lemon.utils.app import BaseAppServer
from django.http import *
import service.common.logging
import service.common.license
import base64
import cloudfish
import gzip
from cStringIO import StringIO
from django.core.servers.basehttp import FileWrapper
import zipfile
import mimetypes
import tempfile
from django.db.models import Min,Max,Sum
from django.shortcuts import render_to_response
import model.django.project.settings
import random, string

@csrf_exempt
def createApp(req):
	"""
	添加应用
	@params:
		@return:
			{status,errcode,result}

	"""
	cr = webapi.SuccCallReturn()
	callback = None
	try:
		app_id  = webapi.GET(req,'app_id')
		name = webapi.GET(req,'name')
		comment = webapi.GET(req,'comment')
		status = webapi.GET(req,'status')


		app_id = app_id.strip()
		name = name.strip()
		status = status.strip()


		if not app_id or not name :
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()

		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		creator_id = webapi.sessionValue(req,'user_id')
		creator =core.AdminUser.objects.get(id=(int(creator_id)))
		app = core.Application()
		if app_id:
			appforid = core.Application.objects.filter(app_id = app_id)
			if appforid:
				return webapi.FailCallReturn(ErrorDefs.AppExisted).httpResponse()
			app.app_id = app_id[:40]
		if name: app.name = name[:40]
		if comment: app.comment = comment[:200]

		if status:
			app.status = int(status)

		app.creator = creator
		app.create_time = datetime.datetime.now()
		app.access_token = lemon.utils.misc.genUUID()
		app.secret_key = lemon.utils.misc.random_password()
		app.save()

		result = app.id
		cr.assign(result)

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.CreateApplicate,request=req)
		log.result = 0
		log.target = app.name
		log.detail = str(req.META['REMOTE_ADDR'])
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()


@csrf_exempt
def updateApp(req):
	"""
	修改应用
	:param req:
	:return:
	"""
	cr = webapi.SuccCallReturn()
	try:
		id = webapi.GET(req,'id')
		app_id  = webapi.GET(req,'app_id')
		name = webapi.GET(req,'name')
		comment = webapi.GET(req,'comment')
		status = webapi.GET(req,'status')

		app_id = app_id.strip()
		name = name.strip()
		status = status.strip()

		if not app_id or not name or not name:
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()

		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		creator_id = webapi.sessionValue(req,'user_id')
		creator =core.AdminUser.objects.get(id=(int(creator_id)))

		app = core.Application.objects.get(id=int(id))
		#应用标识不能更新
		# if app_id:
		# 	appforid = core.Application.objects.filter(app_id = app_id)
		# 	if appforid:
		# 		return webapi.FailCallReturn(ErrorDefs.AppExisted).httpResponse()
		# 	app.app_id = app_id[:40]
		if name: app.name = name[:40]
		if comment: app.comment = comment[:200]

		if status:
			app.status = int(status)

		app.creator = creator
		#app.create_time = datetime.datetime.now()
		app.save()

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.UpdateApplicate,request=req)
		log.result = 0
		log.target = app.name
		log.detail = str(req.META['REMOTE_ADDR'])
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()


@csrf_exempt
def getAppList(req):
	"""
	获取应用列表
	"""
	cr = webapi.SuccCallReturn()
	try:

		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)
		begin,end = webapi.getDataPagingParams(req)
		rs = doQueryApp(req)

		total = rs.count()
		rs = rs.order_by('-create_time')[begin:end]

		result =[]
		for r in rs:
			#app = core.Application.objects.get(id= r.id)
			appusers = core.AppUser.objects.filter(app_id =int(r.id))
			ids=[]
			for appuser in appusers:
				ids.append(appuser.id)

			file_size = core.AppUserFile.objects.filter(user_id__in = ids).aggregate(Sum('file_size'))

			filesize = file_size.get('file_size__sum')
			if filesize == None:
				filesize = 0
			if  filesize < 1048576:
				filesizestr = str(filesize / 1024) + 'K'
			if  1048576 < filesize < 1073741824:
				filesizestr = str(filesize / 1024) + 'M'
			if  filesize > 1073741824:
				filesizestr = str(filesize / 1024) + 'G'

			result.append({'id':r.id,'name':r.name,'app_id':r.app_id,'create_time':lemon.utils.misc.maketimestamp(r.create_time),'status':r.status,'creator':r.creator.name,'file_size':filesizestr})

		cr.assign(result)
		cr.setPageCtrlValue('total',total)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()


@csrf_exempt
def doQueryApp(req):

	"""
	"""
	rs = None

	json_query_parameters = webapi.GET(req, "query_parameters")

	if json_query_parameters :
		query_parameters = json.loads(json_query_parameters)
	else:
		query_parameters ={}

	name = query_parameters.get('case').get("name")
	status = query_parameters.get('case').get("status")

	rs = core.Application.objects.all()
	if name:
		rs = rs.filter(name__icontains=name)
	if status:
		status = int(status)
		rs = rs.filter(status = status)

	return rs

@csrf_exempt
def getAppDetail(req):
	"""
	获取应用详情
	"""
	cr = webapi.SuccCallReturn()
	try:
		id = webapi.GET(req,'id')
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)
		app = core.Application.objects.get(id = int(id))
		appusers = core.AppUser.objects.filter(app_id =int(id))

		ids=[]
		for appuser in appusers:
			ids.append(appuser.id)

		file_size = core.AppUserFile.objects.filter(user_id__in = ids).aggregate(Sum('file_size'))

		filesize = file_size.get('file_size__sum')
		if filesize == None:
			filesize = 0
		if  filesize < 1048576:
			filesizestr = str(filesize / 1024) + 'K'
		if  1048576 < filesize < 1073741824:
			filesizestr = str(filesize / 1024) + 'M'
		if  filesize > 1073741824:
			filesizestr = str(filesize / 1024) + 'G'
		result={
			'id':app.id,
			'app_id':app.app_id,
			'name':app.name,
			'access_token':app.access_token,
			'secret_key':app.secret_key,
			'comment':app.comment,
			'file_size':filesizestr,
			'status':app.status
		}
		cr.assign(result)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException)
	return cr.httpResponse()


@csrf_exempt
def changeAppStatus(req):
	"""
	更改应用状态
	"""

	cr = webapi.SuccCallReturn()
	callback = None
	try:
		json_ids =  webapi.GET(req,'ids')
		status =  webapi.GET(req,'status')
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		ids = json.loads(json_ids)

		#空数组
		if not ids:
			apps = core.Application.objects.all()
			for app in apps:
				app.status = status
				app.save()

		if ids:
			for app_id in ids:
				id = ','.join(app_id)
				app =  core.Application.objects.get(id = int(id))
				app.status = status
				app.save()

				log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.EnableApplicate,request=req)
				if status == '1':
					log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.EnableApplicate,request=req)
				if status == '2':
					log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.DisableApplicate,request=req)
				log.target = app.name
				log.result = 0
				log.detail = str(req.META['REMOTE_ADDR'])
				log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException)
	return cr.httpResponse()


@csrf_exempt
def getAccountList(req):
	"""
	获取帐号列表
	"""
	cr = webapi.SuccCallReturn()
	try:

		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		begin,end = webapi.getDataPagingParams(req)
		rs = doQueryAccount(req)

		total = rs.count()
		rs = rs.order_by('-create_time')[begin:end]

		result =[]
		for r in rs:
			file_size = core.AppUserFile.objects.filter(user_id =int(r.id)).aggregate(Sum('file_size'))
			filesize = file_size.get('file_size__sum')
			if filesize == None:
				filesize = 0
			if  filesize < 1048576:
				filesizestr = str(filesize / 1024) + 'K'
			if  1048576 < filesize < 1073741824:
				filesizestr = str(filesize / 1024) + 'M'
			if  filesize > 1073741824:
				filesizestr = str(filesize / 1024) + 'G'
			result.append({'id':r.id,'name':r.name,'app_name':r.app.name,'status':r.status,'create_time':lemon.utils.misc.maketimestamp(r.create_time),'file_size':filesizestr})

		cr.assign(result)
		cr.setPageCtrlValue('total',total)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()

@csrf_exempt
def doQueryAccount(req):

	"""
	"""
	rs = None

	json_query_parameters = webapi.GET(req, "query_parameters")

	if json_query_parameters :
		query_parameters = json.loads(json_query_parameters)
	else:
		query_parameters ={}

	name = query_parameters.get('case').get("name")
	app_name = query_parameters.get('case').get("app_name")
	status = query_parameters.get('case').get("status")

	rs = core.AppUser.objects.all()
	if name:
		rs = rs.filter(name__icontains=name)
	if app_name:
		rs = rs.filter(app__name__icontains=app_name)
	if status:
		status = int(status)
		rs = rs.filter(status = status)

	return rs


@csrf_exempt
def changeAccountStatus(req):
	"""
	更改账号状态
	"""

	cr = webapi.SuccCallReturn()
	callback = None
	try:
		json_ids =  webapi.GET(req,'ids')
		status =  webapi.GET(req,'status')
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		ids = json.loads(json_ids)

		#空数组
		if not ids:
			appUsers = core.AppUser.objects.all()
			for appUser in appUsers:
				appUser.status = status
				appUser.save()
		if ids:
			for appUser_id in ids:
				id = ','.join(appUser_id)
				appUser =  core.AppUser.objects.get(id = id)
				appUser.status = status
				appUser.save()

				log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.EnableAppUser,request=req)
				if status == '1':
					log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.EnableAppUser,request=req)
				if status == '2':
					log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.DiableAppUser,request=req)
				log.target = appUser.name
				log.result = 0
				log.detail = str(req.META['REMOTE_ADDR'])
				log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException)
	return cr.httpResponse()

@csrf_exempt
def changeAccountPassword(req):
	"""
	更改当前登录用户密码
	"""

	cr = webapi.SuccCallReturn()
	callback =None
	try:
		id =  webapi.GET(req,'id')
		oldpasswd =  webapi.GET(req,'oldpasswd')
		newpasswd = webapi.GET(req,'newpasswd')
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		r = core.AppUser.objects.get(id = int(id))
		#MD加密
		oldpasswd = lemon.encrypt.md5(r.salt + oldpasswd)
		newpasswd = lemon.encrypt.md5(r.salt + newpasswd)

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.ChangeAppUserPassword,request=req)

		if r.passwd != oldpasswd:
			log.result = 1
			log.detail = u'密码错误'
			log.save()
			return webapi.FailCallReturn(ErrorDefs.PasswdIncorret).httpResponse()
		r.passwd = newpasswd
		r.save()
		log.result = 0
		log.detail = str(req.META['REMOTE_ADDR'])
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()

@csrf_exempt
def createAccount(req):
	"""
	添加应用
	@params:
		@return:
			{status,errcode,result}

	"""
	cr = webapi.SuccCallReturn()
	callback = None
	try:
		app_id  = webapi.GET(req,'app_id')
		name = webapi.GET(req,'name')
		username = webapi.GET(req,'username')
		passwd = webapi.GET(req,'passwd')
		phone = webapi.GET(req,'phone')
		address = webapi.GET(req,'address')
		status = webapi.GET(req,'status')

		name = name.strip()

		if not name :
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()

		appusername = core.AppUser.objects.filter(name=name)
		if (appusername.exists()):
			return webapi.FailCallReturn(ErrorDefs.AccountExisted).httpResponse()

		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		app = core.Application.objects.get(id= int(app_id))
		appUser = core.AppUser()
		appUser.app = app

		appUser.salt = genPassword(10)
		if name: appUser.name = name[:40]
		if username: appUser.username = username[:20]
		if passwd: appUser.passwd = lemon.encrypt.md5(appUser.salt+ passwd[:20])
		if phone: appUser.phone = phone[:20]
		if address: appUser.address = address[:80]

		if status:
			appUser.status = int(status)

		appUser.create_time = datetime.datetime.now()

		appUser.save()

		result = appUser.id
		cr.assign(result)

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.CreateAppUser,request=req)
		log.result = 0
		log.target = appUser.name
		log.detail = str(req.META['REMOTE_ADDR'])
		log.user_role = req.session['user_role']
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()


@csrf_exempt
def updateAccount(req):
	cr = webapi.SuccCallReturn()
	try:
		id = webapi.GET(req,'id')
		app_id  = webapi.GET(req,'app_id')
		name = webapi.GET(req,'name')
		username = webapi.GET(req,'username')
		phone = webapi.GET(req,'phone')
		address = webapi.GET(req,'address')
		#is_backend = webapi.GET(req,'is_backend')
		status = webapi.GET(req,'status')

		name = name.strip()

		if not name :
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()

		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		app = core.Application.objects.get(id= int(app_id))
		appUser = core.AppUser.objects.get(id=int(id))

		#如果修改app，则会查询对应授权数
		if app!= appUser.app:
			#判断应用授权数量
			#已用数量
			cert_num = core.AppUser.objects.filter(cert__isnull= False,app=app).count()

			if cert_num >= app.max_lic_num:
				return webapi.FailCallReturn(ErrorDefs.AppNoLic).httpResponse()

		appUser.app = app

		if name:
			appUser.name = name[:40]
		if username:
			appUser.username = username[:20]
		if phone:
			appUser.phone = phone[:20]
		else:
			appUser.phone = phone
		if address:
			appUser.address = address[:80]
		else:
			appUser.address = address
		if status:
			appUser.status = int(status)

		#不能修改用户是否前后端
		# if is_backend=='1':
		# 	is_backend = True
		# 	appUser.cert = app.cert
        #
		# if is_backend=='2':
		# 	is_backend = False
		# 	rs = core.AppCertificate.objects.filter(status = 1)
		# 	if rs:
		# 		appUser.cert = rs[0]
		# 	else:
		# 		appUser.cert = None
        #
		# appUser.is_backend = is_backend

		appUser.save()

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.UpdateAppUser,request=req)
		log.result = 0
		log.target = appUser.name
		log.detail = str(req.META['REMOTE_ADDR'])
		log.user_role = req.session['user_role']
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()


@csrf_exempt
def getAccountDetail(req):
	"""
	获取应用详情
	"""
	cr = webapi.SuccCallReturn()
	try:
		id = webapi.GET(req,'id')
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)
		appUser = core.AppUser.objects.get(id = int(id))
		file_size = core.AppUserFile.objects.filter(user_id =int(id)).aggregate(Sum('file_size'))
		filesize = file_size.get('file_size__sum')
		if filesize == None:
			filesize = 0
		if  filesize < 1048576:
			filesizestr = str(filesize / 1024) + 'K'
		if  1048576 < filesize < 1073741824:
			filesizestr = str(filesize / 1024) + 'M'
		if  filesize > 1073741824:
			filesizestr = str(filesize / 1024) + 'G'
		result={
			'id':appUser.id,
			'app_id':appUser.app.id,
			'app_name':appUser.app.name,
			'name':appUser.name,
			'username':appUser.username,
			'passwd':appUser.passwd,
			'phone':appUser.phone,
			'address':appUser.address,
			'file_size':filesizestr,
			'status':appUser.status
		}
		cr.assign(result)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException)
	return cr.httpResponse()

@csrf_exempt
def genPassword(length):
    #随机出数字的个数
    numOfNum = random.randint(1,length-1)
    numOfLetter = length - numOfNum
    #选中numOfNum个数字
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    #选中numOfLetter个字母
    slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
    #打乱这个组合
    slcChar = slcNum + slcLetter
    random.shuffle(slcChar)
    #生成密码
    genPwd = ''.join([i for i in slcChar])
    return genPwd
