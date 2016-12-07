#-- coding:utf-8 --

import traceback,threading,time,struct,os,os.path,shutil,distutils.dir_util,array,base64,zlib,struct,binascii,string
import datetime
import json,hashlib,base64

from django.db import transaction

import model.django.core.models as core

from django.views.decorators.csrf import csrf_exempt
import lemon
from lemon import webapi
from lemon.errors import ErrorDefs

import xlwt

from django.core.servers.basehttp import FileWrapper
import mimetypes
from django.http import *
import service.common.logging
import cloudfish


@csrf_exempt
def createAppServer(req):
	"""
	添加应用服务器
	@params:
		@return:
			{status,errcode,result}

	"""
	cr = webapi.SuccCallReturn()
	callback = None
	try:
		name = webapi.GET(req,'name')
		ip_addr = webapi.GET(req,'ip_addr')
		app_id = webapi.GET(req,'app_id')
		is_addr_restricted = webapi.GET(req,'is_addr_restricted')
		status=  webapi.GET(req,'status')

		name = name.strip()
		ip_addr = ip_addr.strip()


		if not name or not ip_addr:
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()

		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		appServer = core.AppServer()
		app = core.Application.objects.get(id = int(app_id))
		appServer.app = app
		if name: appServer.name = name[:40]
		if ip_addr: appServer.ip_addr = ip_addr[:30]

		if is_addr_restricted=='1':
			is_addr_restricted = True
		if is_addr_restricted=='2':
			is_addr_restricted = False
		appServer.is_addr_restricted = is_addr_restricted

		if status:
			appServer.status = int(status)

		appServer.create_time = datetime.datetime.now()

		#调用生成服务器访问令牌和访问口令(判断token是否存在)

		# while True:
		# 	access_token = lemon.utils.misc.genUUID()
    		# if not core.AppServer.objects.objects.filter(access_token= access_token).exits():
       	# 		break
		appServer.access_token = lemon.utils.misc.genUUID()
		appServer.secret_key = lemon.utils.misc.random_password()

		appServer.save()
		result = {
			'id':appServer.id,
			'access_token':appServer.access_token,
			'secret_key':appServer.name
		}
		cr.assign(result)

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.CreateAppServer,request=req)
		log.result = 0
		log.target = appServer.name
		log.detail = str(req.META['REMOTE_ADDR'])
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()


@csrf_exempt
def updateAppServer(req):
	"""
	修改应用服务器
	"""
	cr = webapi.SuccCallReturn()
	try:
		id = webapi.GET(req,'id')
		name = webapi.GET(req,'name')
		ip_addr = webapi.GET(req,'ip_addr')
		app_id = webapi.GET(req,'app_id')
		is_addr_restricted = webapi.GET(req,'is_addr_restricted')
		status=  webapi.GET(req,'status')

		name = name.strip()
		ip_addr = ip_addr.strip()

		if not name or not ip_addr:
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()

		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)

		appServer = core.AppServer.objects.get(id=int(id))
		app = core.Application.objects.get(id = int(app_id))
		appServer.app = app
		if name: appServer.name = name[:40]
		if ip_addr: appServer.ip_addr = ip_addr[:30]

		if is_addr_restricted=='1':
			is_addr_restricted = True
		if is_addr_restricted=='2':
			is_addr_restricted = False
		appServer.is_addr_restricted = is_addr_restricted

		if status:
			appServer.status = int(status)

		appServer.save()

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.UpdateAppServer,request=req)
		log.result = 0
		log.target = appServer.name
		log.detail = str(req.META['REMOTE_ADDR'])
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()



@csrf_exempt
def getAppServerList(req):
	"""
	获取应用服务器列表
	"""
	cr = webapi.SuccCallReturn()
	try:
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)
		begin,end = webapi.getDataPagingParams(req)

		rs = doQueryAppServer(req)

		total = rs.count()
		rs = rs.order_by('-create_time')[begin:end]

		result =[]
		for r in rs:
			result.append({'id':r.id,'name':r.name,'ip_addr':r.ip_addr,'app_name':r.app.name,'create_time':lemon.utils.misc.maketimestamp(r.create_time),'status':r.status})

		cr.assign(result)
		cr.setPageCtrlValue('total',total)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()


@csrf_exempt
def doQueryAppServer(req):

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

	rs = core.AppServer.objects.all()
	if name:
		rs = rs.filter(name__icontains=name)
	if status:
		status = int(status)
		rs = rs.filter(status = status)

	return rs


@csrf_exempt
def changeAppServerStatus(req):
	"""
	更改应用服务器状态
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
			appServers = core.AppServer.objects.all()
			for appServer in appServers:
				appServer.status = status
				appServer.save()
		if ids:
			for id in ids:
				id = ','.join(id)
				appServer =  core.AppServer.objects.get(id = id)
				appServer.status = status
				appServer.save()

		log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.EnableAppServer,request=req)
		if status == '1':
			log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.EnableAppServer,request=req)
		if status == '2':
			log = service.common.logging.createLog(cloudfish.base.AdminUserActionType.DisableAppServer,request=req)
		log.result = 0
		log.detail = str(req.META['REMOTE_ADDR'])
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException)
	return cr.httpResponse()


@csrf_exempt
def getAppServerDetail(req):
	"""
	获取应用服务器详情
	"""
	cr = webapi.SuccCallReturn()
	try:
		id = webapi.GET(req,'id')
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)
		appServer = core.AppServer.objects.get(id = int(id))
		if appServer.is_addr_restricted == True:
			is_addr_restricted = 1
		if appServer.is_addr_restricted == False:
			is_addr_restricted = 2
		result={
			'id':appServer.id,
			'name':appServer.name,
			'ip_addr':appServer.ip_addr,
			'app_id':appServer.app.id,
			'app_name':appServer.app.name,
			'is_addr_restricted':is_addr_restricted,
			'status':appServer.status,
			'access_token':appServer.access_token,
			'secret_key':appServer.secret_key
		}
		cr.assign(result)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException)
	return cr.httpResponse()







