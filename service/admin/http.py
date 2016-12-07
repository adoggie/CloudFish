#-- coding:utf-8 --
#!/usr/bin/python

import traceback,threading,time,struct,os,os.path,shutil,distutils.dir_util,array,base64,zlib,struct,binascii
import datetime
import json,hashlib,base64
from django.http import *
from django.core.handlers.wsgi import WSGIHandler
from gevent.wsgi import WSGIServer

from django.shortcuts import render_to_response


import model.django.core.models as core

from django.views.decorators.csrf import csrf_exempt
import lemon
from lemon import encrypt
from lemon import webapi
from lemon.errors import ErrorDefs
import service.lemon_impl
import service.common.logging
import cloudfish
from lemon import webapi,errors
import service.common.license

@csrf_exempt
def login(req):
	"""
	login
	@params:
		@return:
			{status,errcode,result}

	"""
	cr = webapi.SuccCallReturn()
	callback =None
	log = None
	try:
		username =  webapi.GET(req,'user')
		password = webapi.GET(req,'password')
		signcode = webapi.GET(req,'signcode')
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.Login)
		log.user = username
		if not username or not password :
			# log.result = 1
			# log.detail = u'用户名或密码错误'
			# log.user_role = 0
			# log.save()
			return lemon.webapi.FailCallReturn(ErrorDefs.UserNameNotExisted).httpResponse()
		#验证码
		# if signcode.lower() != req.session['sign_chars'].lower():
		# 	# log.result = 1
		# 	# log.detail = u'验证码错误'
		# 	# log.save()
		# 	return lemon.webapi.FailCallReturn(ErrorDefs.SignCodeIncorret).httpResponse()
		#MD加密
		password = lemon.encrypt.md5(password)
		rs = core.AdminUser.objects.filter(login=username,password=password)
		if not rs:
			log.result = 1
			log.detail = u'用户名或密码错误'
			log.user_role = 0
			log.save()
			return lemon.webapi.FailCallReturn(ErrorDefs.UserNameNotExisted).httpResponse()
		r = rs[0]
		req.session['user_id'] =  r.id
		req.session['user_role'] =  r.role

		ar = service.lemon_impl.AuthResult_t()
		ar.user_id = r.id
		ar.user_name = username
		ar.login_time = int(time.time())
		ar.expire_time = ar.login_time + 3600*5  #默认 5天过期
		token = lemon.encrypt.encryptUserToken(ar)

		cr.assign(token)	# {result: token}

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.Login,request=req)
		log.result = 0
		log.user_role = r.role
		log.detail = str(req.META['REMOTE_ADDR'])
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	log.save()
	return cr.httpResponse()


@csrf_exempt
def changePassword(req):
	"""
	更改当前登录用户密码
	"""

	cr = webapi.SuccCallReturn()
	callback =None
	try:
		oldpasswd =  webapi.GET(req,'oldpasswd')
		newpasswd = webapi.GET(req,'newpasswd')
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		#MD加密
		oldpasswd = lemon.encrypt.md5(oldpasswd)
		newpasswd = lemon.encrypt.md5(newpasswd)

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.ChangePassword,request=req)
		r = core.AdminUser.objects.get(id = lemon.webapi.sessionValue(req,'user_id'))
		if r.password != oldpasswd:
			log.result = 1
			log.detail = u'密码错误'
			log.save()
			return webapi.FailCallReturn(ErrorDefs.PasswdIncorret).httpResponse()
		r.password = newpasswd
		r.save()
		log.result = 0
		log.detail = str(req.META['REMOTE_ADDR'])
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()


@csrf_exempt
def getCurrentUserInfo(req):
	cr = webapi.SuccCallReturn()
	callback =None
	try:
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)
		r = core.AdminUser.objects.get(id = lemon.webapi.sessionValue(req,'user_id'))
		cr.assign({'user':r.login,'role':r.role})
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()

@csrf_exempt
def logout(req):
	cr = webapi.SuccCallReturn()
	if req.session.get('user_id'):
		#注销日志
		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.Logout,request=req)
		log.result = 0
		log.detail = str(req.META['REMOTE_ADDR'])
		log.save()
		del req.session['user_id']
	return cr.httpResponse()

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