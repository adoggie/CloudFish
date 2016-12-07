#-- coding:utf-8 --
#!/usr/bin/python

import traceback,threading,time,struct,os,os.path,shutil,distutils.dir_util,array,base64,zlib,struct,binascii
import datetime
from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page

import model.django.core.models as core

from django.views.decorators.csrf import csrf_exempt
import lemon
from lemon import webapi,errors
# import service.config
from django.http import StreamingHttpResponse
import model.django.project.settings
import os, tempfile, zipfile
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import mimetypes

@csrf_exempt
def getSignImage(req):
	'''
	获取验证码信息
	1.generate vcode image
	2.put into cache-server
		vcode_vcode_id: vcode_val

	:param r:
	:return:
		{id,image_base64}
	'''
	import lemon.utils.image.vcode

	cr = webapi.SuccCallReturn()
	try:
		image,chars = lemon.utils.image.vcode.create_validate_code()

		req.session['sign_chars'] = chars
		cr.assign(image)

	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(errors.ErrorDefs.InternalException)
	return cr.httpResponse()


def root(req):
	# print 'root:',req.get_host()
	# host = 'http://'+ req.META.get('HTTP_HOST')+':'+ str(req.META.get('SERVER_PORT')) +'/admin/'
	# print host
	# return HttpResponseRedirect( host)
	return render_to_response('adminLogin.html')

@csrf_exempt
def ras(req):
	# print 'ras',req.path
	user_type = webapi.sessionValue(req,'user_type',0)
	if user_type  and user_type != lemon.basetype.LoginUserType.USER:
		del req.session['user_id']
	return render_to_response('index.html')


@csrf_exempt
def admin(req):
	# print 'ras',req.path
	# user_type = webapi.sessionValue(req,'user_type',0)
	# if user_type and  user_type != lemon.basetype.LoginUserType.ADMIN:
	# 	# del req.session['user_id']
	# 	return render_to_response('adminLogin.html')

	return render_to_response('adminIndex.html')

# @csrf_exempt
@cache_page(60*100)
def loadPage(req,prefix='/'):
	PREFIX= prefix

	# print req
	print req.path
	idx = req.path.find(PREFIX)
	# if idx == -1:
	# 	return HttpResponseNotFound()

	idx+=len(PREFIX)
	html = req.path[idx:]
	print '*-'*30
	print 'read page file:',html

	return render_to_response(html)



def fileDownload(req):
	type =  webapi.GET(req,'type')
	if type =='client':
		filename = model.django.lemon.settings.client_path
		file = "gongwen_client.tar.gz"
	else:
		filename = model.django.lemon.settings.doc_path
		file = "readme.doc"
	fp = open(filename,'rb')
	wrapper = FileWrapper(fp)
	response = HttpResponse(wrapper, content_type='text/plain')
	response['Content-Length'] = os.path.getsize(filename)

	content_type = mimetypes.guess_type(filename)[0]
	response = StreamingHttpResponse(wrapper, content_type=content_type)
	response['Content-Disposition'] = "attachment; filename=%s" % file.encode('utf-8')
	return response