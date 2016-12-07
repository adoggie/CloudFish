#-- coding:utf-8 --

import traceback,threading,time,struct,os,os.path,shutil,distutils.dir_util,array,base64,zlib,struct,binascii

import model.django.core.models as core

from django.views.decorators.csrf import csrf_exempt
from lemon import webapi
from lemon.errors import ErrorDefs

@csrf_exempt
def getAllApp(req):
	"""
	获取全部应用
	"""
	cr = webapi.SuccCallReturn()
	try:

		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		apps = core.Application.objects.all()

		result =[]
		for app in apps:
			result.append({'id':app.id,'name':app.name})

		cr.assign(result)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()




