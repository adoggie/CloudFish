#coding:utf-8
__author__ = 'root'

import os,traceback,base64,time,datetime
from django.views.decorators.csrf import csrf_exempt

from lemon import webapi
import lemon.errors
import lemon.base

import model.django.core.models as core
from service.common.decorator import user_auth_token_check,server_ip_address_restrict
import cloudfish.base
import service.common.token as Token

def normalize_user_storage_id(user_name):
	return user_name

	import string
	ins = "/=\\,+&%$#@~`|?:"
	outs = '-'* len(ins)
	tabs = string.maketrans(ins,outs)
	return user_name.translate(tabs)

def get_user_storage_id(user):
	if not user.storage_id:
		return normalize_user_storage_id(user.name)
	return user.storage_id

@csrf_exempt
# @server_ip_address_restrict
def userLogin(request):
	"""
	服务器发送用户登录
	:param request:
		access_token
		secret_key
		user_id
		is_root - 是否是server发起的登录
		timeout - token超时时间(hour),默认有效时间: 24hours

	:return:
	"""

	cr = webapi.SuccCallReturn()
	username = webapi.GET(request,'username')

	access_token = webapi.GET(request,'access_token')
	secret_key = webapi.GET(request,'secret_key')

	is_root = webapi.GET(request,'is_root',0)
	timeout = webapi.GET(request,'timeout',24)

	if not access_token:
		access_token = webapi.GET(request,'app_key')
	if not secret_key:
		secret_key = webapi.GET(request,'app_secret')
	if not username:
		username = webapi.GET(request,'client_id')


	try:
		user = None
		username = username.strip()
		is_root = int(is_root)
		timeout = int(timeout)

		if timeout ==0 :
			timeout = 0xffff

		if not len(username):
			return webapi.FailCallReturn(lemon.errors.ErrorDefs.ParameterIllegal).httpResponse()

		rs = core.Application.objects.filter(access_token = access_token,secret_key = secret_key)
		if not rs:
			return webapi.FailCallReturn(lemon.errors.ErrorDefs.ObjectNotExisted).httpResponse()
		app = rs[0]

		rs = core.AppUser.objects.filter(name = username)
		if not rs :
			#用户不存在,将插入新的应用用户记录
			user = core.AppUser(app = app,name = username,last_login_time = datetime.datetime.now(),
				create_time = datetime.datetime.now(),
				status = cloudfish.base.STATUS_TYPE_ENABLED,
				storage_id = normalize_user_storage_id( username )
			)
			user.save()
		else:
			user = rs[0]


		usertype = cloudfish.base.ACCESSOR_TYPE_NORMAL
		if is_root:
			usertype = cloudfish.base.ACCESSOR_TYPE_ROOT

		user_dict ={
			'id': user.id,
			'user_id': username,
			'app_id':app.id,
			'app_sid': app.app_id,
			'app_name': app.name,
			'node_type':usertype,
			'create_time': int(time.time()),
			'expire_time': int(time.time()) + 3600 * timeout,
			'app_container':app.container_name,
			'user_storage_id': get_user_storage_id(user)
		}

		token = Token.encryptUserToken(user_dict)
		result= token


		cr.assign(result)
		user.token = token
		user.last_login_time = datetime.datetime.now()
		user.save()

		log = core.LogAppUserAction(user= user.name,
			user_role= usertype,
			token=token,
			issue_time=datetime.datetime.now(),
			action = cloudfish.base.AppUserActionType.CLIENT_USER_LOGIN,
			target = None,
		)
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(lemon.errors.ErrorDefs.InternalException,traceback.format_exc())
	return cr.httpResponse()

@csrf_exempt
@user_auth_token_check
def userLogout(request):
	"""
	服务器发送用户登出
	:param request:
	:return:
	"""
	cr = webapi.SuccCallReturn()
	try:
		user = core.AppUser.objects.get(id= request.user.get('id'))
		# 日志记录
		log = core.LogAppUserAction(user=user.name,
			user_role= request.user.get('node_type'),
			issue_time=datetime.datetime.now(),
			action = cloudfish.base.AppUserActionType.CLIENT_USER_LOGOUT,
			target = None,
		)
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(lemon.errors.ErrorDefs.InternalException,traceback.format_exc())
	return cr.httpResponse()
