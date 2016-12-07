# coding:utf-8


__author__ = 'root'


"""

"""

import time,traceback
from django.views.decorators.csrf import csrf_exempt


from lemon import webapi
import lemon.errors

import cloudfish.errors
import cloudfish.base
import model.django.core.models as core 

import token as Token


def user_auth_token_check(func):

	def _wrapper(request,*args,**kwargs):
		token = webapi.HEADER(request,'token')
		if not token:
			return webapi.FailCallReturn( cloudfish.errors.ErrorDefs.UnAuthorizedAccess).httpResponse()
		user = Token.decryptUserToken(token)
		if not user:
			return webapi.FailCallReturn( cloudfish.errors.ErrorDefs.UnAuthorizedAccess).httpResponse()

		# token expired
		if user.get('expire_time',0) < int(time.time()):
			return webapi.FailCallReturn( cloudfish.errors.ErrorDefs.UnAuthorizedAccess).httpResponse()

		request.user = user
		return func(request,*args,**kwargs)
	return _wrapper

	

def server_ip_address_restrict(func):
	"""

	:param func:
	:return:
	"""
	def _wrapper(request,*args,**kwargs):

		cr = webapi.SuccCallReturn()
		access_token = webapi.GET(request,'access_token')
		secret_key = webapi.GET(request,'secret_key')

		rs = core.AppServer.objects.filter(access_token=access_token,secret_key=secret_key,status=cloudfish.base.STATUS_TYPE_ENABLED,app__status=cloudfish.base.STATUS_TYPE_ENABLED)
		if not rs:
			return webapi.FailCallReturn(cloudfish.errors.ErrorDefs.ADDRESS_RESTRICTED).httpResponse()
		server = rs[0]
		if server.is_addr_restricted:
			if server.ip_addr != request.META['REMOTE_ADDR']:
				return webapi.FailCallReturn(cloudfish.errors.ErrorDefs.ADDRESS_RESTRICTED).httpResponse()
		request.server = server
		return func(request,*args,**kwargs)


	return _wrapper