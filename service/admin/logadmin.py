#-- coding:utf-8 --

import traceback,threading,time,struct,os,os.path,shutil,distutils.dir_util,array,base64,zlib,struct,binascii,string
import datetime
import json,hashlib,base64

import model.django.core.models as core

from django.views.decorators.csrf import csrf_exempt
import lemon
from lemon import webapi
from lemon.errors import ErrorDefs

from django.core.servers.basehttp import FileWrapper
import mimetypes
from django.http import *
import xlwt
import cloudfish
import tempfile

def doQueryAdminUserActionLog(req):
	"""
	"""
	rs = None

	case =  webapi.GET(req,'case')
	if case :
		case = json.loads(case)
	else:
		case ={}
	start_time = case.get('start_time',0)
	end_time = case.get('end_time',0)
	user_role = case.get('user_role')
	target = case.get('target')
	result = case.get('result')
	detail = case.get('detail')
	action_ids = case.get('action_ids')

	if not start_time: start_time = 0
	if not end_time: end_time = int(time.time())

	rs = core.LogAdminUserAction.objects.all()
	if start_time:
		start_time = lemon.utils.misc.mk_datetime(start_time)
		end_time = lemon.utils.misc.mk_datetime(end_time)
		rs = rs.filter(issue_time__range=(start_time,end_time))
	if user_role:
		user_role = int(user_role)
		rs = rs.filter(user_role = user_role)
	if target:
		rs = rs.filter(target__icontains=target)
	if result:
		rs = rs.filter(result = result)
	if detail:
		rs = rs.filter(detail__icontains = detail)

	ids = map(str,action_ids)
	ids = string.join(ids,',')

	#操作类型过滤
	if ids:
		rs = rs.extra(where=['action in (%s)'%ids])

	return rs


@csrf_exempt
def getAdminLog(req):
	"""
	查询管理员平台操作日志
	"""
	cr = webapi.SuccCallReturn()
	callback = None
	try:
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)
		case =  webapi.GET(req,'case')
		if case :
			case = json.loads(case)
		else:
			case ={}
		begin,end = webapi.getDataPagingParams(req)
		action_ids = case.get('action_ids')
		if not action_ids:
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()
		rs = doQueryAdminUserActionLog(req)

		total = rs.count()
		rs = rs.order_by('-issue_time')[begin:end]

		result =[]
		for r in rs:
			result.append({
				'act_name':cloudfish.base.AdminUserActionType.nameValue(r.action),
				'user':r.user,
				'user_role': cloudfish.base.AdminUserType.nameValue(r.user_role),
				'issue_time': lemon.utils.misc.maketimestamp(r.issue_time),
				'target':r.target,
				'result':  cloudfish.base.ResultType.nameValue(r.result),
				'detail': r.detail
			})

		cr.assign( result )
		cr.setPageCtrlValue('total',total)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()

@csrf_exempt
def exportAdminLog(req):
	"""
	导出管理员平台操作日志
	"""
	cr = webapi.SuccCallReturn()
	try:
		case =  webapi.GET(req,'case')
		if case :
			case = json.loads(case)
		else:
			case ={}
		begin,end = webapi.getDataPagingParams(req)
		action_ids = case.get('action_ids')
		if not action_ids:
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()
		rs = doQueryAdminUserActionLog(req)
		rs = rs.order_by('-issue_time')[begin:end]

		hdr = u'操作人 操作人角色 操作时间 日志类型 操作对象 操作结果 操作内容'
		wbk = xlwt.Workbook()
		sheet = wbk.add_sheet('sheet 1')
		fs = hdr.split(u' ')
		c = 0
		for f in fs:
			sheet.write( 0,c,f)
			c+=1
		row = 1
		for r in rs:
			result = u'操作成功'
			if r.result != 0:
				result = u'操作失败'
			data =[
				r.user,
				cloudfish.base.AdminUserType.nameValue(r.user_role),
				lemon.utils.misc.formatTimestamp(lemon.utils.misc.maketimestamp(r.issue_time)),
				cloudfish.base.AdminUserActionType.nameValue(r.action),
				r.target,
				result,
				r.detail
			]
			for c in range(len(data)):
				sheet.write( row,c,data[c])
			row+=1

		#linux下写死tmp
		filename = os.path.join('/tmp/', 'export_admin_logs.xls')
		wbk.save(filename)

		#http download
		fp = open(filename,'rb')
		wrapper = FileWrapper(fp)
		content_type = mimetypes.guess_type(filename)[0]
		response = StreamingHttpResponse(wrapper, content_type=content_type)
		response['Content-Disposition'] = "attachment; filename=%s" % fp.name
		return response
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException)
	return cr.httpResponse()


def doQueryAppUserActionLog(req):
	"""
	"""
	rs = None

	case =  webapi.GET(req,'case')
	if case :
		case = json.loads(case)
	else:
		case ={}
	begin,end = webapi.getDataPagingParams(req)
	start_time = case.get('start_time',0)
	end_time = case.get('end_time',0)
	user_role = case.get('user_role')
	target = case.get('target')
	result = case.get('result')
	detail = case.get('detail')
	action_ids = case.get('action_ids')

	if not start_time: start_time = 0
	if not end_time: end_time = int(time.time())

	rs = core.LogAppUserAction.objects.all()
	if start_time:
		start_time = lemon.utils.misc.mk_datetime(start_time)
		end_time = lemon.utils.misc.mk_datetime(end_time)
		rs = rs.filter(issue_time__range=(start_time,end_time))
	if user_role:
		user_role = int(user_role)
		rs = rs.filter(user_role = user_role)
	if target:
		rs = rs.filter(target__icontains=target)
	if result:
		rs = rs.filter(result = result)
	if detail:
		rs = rs.filter(detail__icontains = detail)

	ids = map(str,action_ids)
	ids = string.join(ids,',')

	#操作类型过滤
	if ids:
		print ids
		rs = rs.extra(where=['action in (%s)'%ids])

	return rs


@csrf_exempt
def getAppUserLog(req):
	"""
	查询管理员平台操作日志
	"""
	cr = webapi.SuccCallReturn()
	callback = None
	try:
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)
		case =  webapi.GET(req,'case')
		if case :
			case = json.loads(case)
		else:
			case ={}
		begin,end = webapi.getDataPagingParams(req)
		action_ids = case.get('action_ids')
		if not action_ids:
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()
		rs = doQueryAppUserActionLog(req)

		total = rs.count()
		rs = rs.order_by('-issue_time')[begin:end]

		result =[]
		for r in rs:
			result.append({
				'act_name':cloudfish.base.AppUserActionType.nameValue(r.action),
				'user':r.user,
				'user_role': cloudfish.base.AppUserType.nameValue(r.user_role),
				'issue_time': lemon.utils.misc.maketimestamp(r.issue_time),
				'target':r.target,
				'result':  cloudfish.base.ResultType.nameValue(r.result),
				'detail': r.detail
			})

		cr.assign( result )
		cr.setPageCtrlValue('total',total)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()


@csrf_exempt
def exportAppUserLog(req):
	"""
	导出用户客户端操作行为日志
	"""
	cr = webapi.SuccCallReturn()
	try:
		case =  webapi.GET(req,'case')
		if case :
			case = json.loads(case)
		else:
			case ={}
		begin,end = webapi.getDataPagingParams(req)
		action_ids = case.get('action_ids')
		if not action_ids:
			return webapi.FailCallReturn(ErrorDefs.ParameterIllegal).httpResponse()
		rs = doQueryAppUserActionLog(req)
		rs = rs.order_by('-issue_time')[begin:end]

		hdr = u'操作人 操作人角色 操作时间 日志类型 操作对象 操作结果 操作内容'
		wbk = xlwt.Workbook()
		sheet = wbk.add_sheet('sheet 1')
		fs = hdr.split(u' ')
		c = 0
		for f in fs:
			sheet.write( 0,c,f)
			c+=1
		row = 1
		for r in rs:
			result = u'操作成功'
			if r.result != 0:
				result = u'操作失败'
			data =[
				r.user,
				cloudfish.base.AppUserType.nameValue(r.user_role),
				lemon.utils.misc.formatTimestamp(lemon.utils.misc.maketimestamp(r.issue_time)),
				cloudfish.base.AppUserActionType.nameValue(r.action),
				r.target,
				result,
				r.detail
			]
			for c in range(len(data)):
				sheet.write( row,c,data[c])
			row+=1

		#linux下写死tmp
		filename = os.path.join('/tmp/', 'export_user_logs.xls')
		wbk.save(filename)

		#http download
		fp = open(filename,'rb')
		wrapper = FileWrapper(fp)
		content_type = mimetypes.guess_type(filename)[0]
		response = StreamingHttpResponse(wrapper, content_type=content_type)
		response['Content-Disposition'] = "attachment; filename=%s" % fp.name
		return response
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(ErrorDefs.InternalException)
	return cr.httpResponse()
