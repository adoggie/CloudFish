#-- coding:utf-8 --

# ems: mac mini ez402929766cn


import traceback,threading,time,struct,os,os.path,shutil,distutils.dir_util,array,base64,zlib,struct,binascii
import datetime,json


import model.django.core.models as core

from django.views.decorators.csrf import csrf_exempt
from lemon import webapi
from lemon import errors
from lemon import basetype
import lemon
import service.common.logging

@csrf_exempt
def getNoticeList(r):
	"""
	获取通知消息列表
	"""
	cr = webapi.SuccCallReturn()
	callback = None
	try:
		start,end = webapi.getDataPagingParams(r)
		callback = webapi.GET(r,'callback')
		cr.setCallBackJsonp(callback)

		rs = core.Notice.objects.all().order_by('-modify_time')[start:end]
		result = []
		for r in rs:
			result.append({'id':r.id,
				'title':r.title,
				'content':r.content,
				'create_time':lemon.utils.misc.maketimestamp(r.create_time),
				'issuer':r.issuer.name,
				'issuer_id':r.issuer.id,
				'alert': lemon.base.IntValOfBoolean(r.alert) ,
				'end_alert_time': lemon.utils.misc.maketimestamp(r.end_alert_time)
			})
		cr.assign( result )
		cr.setPageCtrlValue('total',core.Notice.objects.all().count() )
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(errors.ErrorDefs.InternalException)
	return cr.httpResponse()

@csrf_exempt
def getNoticeDetail(r):
	"""
	获取通知消息详情
	"""
	cr = webapi.SuccCallReturn()

	try:
		notice_id =  webapi.GET(r,'id')
		notice_id = int(notice_id)

		callback = webapi.GET(r,'callback')
		cr.setCallBackJsonp(callback)

		r = core.Notice.objects.get(id = notice_id)
		result = {'id':r.id,
				'title':r.title,
				'content':r.content,
				'create_time':lemon.utils.misc.maketimestamp(r.create_time),
				'issuer':r.issuer.name,
				'issuer_id':r.issuer.id,
				'alert': lemon.base.IntValOfBoolean(r.alert) ,
				'end_alert_time': lemon.utils.misc.maketimestamp(r.end_alert_time)
			}
		cr.assign(result)
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(errors.ErrorDefs.InternalException)
	return cr.httpResponse()



@csrf_exempt
def createNotice(r):
	"""
	创建系统通知消息
	"""
	cr = webapi.SuccCallReturn()
	callback = None
	try:
		title =  webapi.GET(r,'title')
		content = webapi.GET(r,'content')
		alert = webapi.GET(r,'alert',0)
		end_alert_time = webapi.GET(r,'end_alert_time',None)
		alert = int(alert)
		if alert:
			alert = True
		else:
			alert = False

		if end_alert_time:
			end_alert_time = lemon.utils.misc.mk_datetime(end_alert_time)

		callback = webapi.GET(r,'callback')
		cr.setCallBackJsonp(callback)
		if not title or not content:
			return webapi.FailCallReturn(errors.ErrorDefs.ParameterIllegal).httpResponse()

		user_id = webapi.sessionValue(r,'user_id')
		admin = core.AdminUser.objects.get(id = int(user_id))
		notice = core.Notice()
		notice.issuer = admin
		notice.title = title[:255]
		notice.content = content[:2000]
		notice.create_time = datetime.datetime.now()
		notice.modify_time = notice.create_time
		notice.alert = alert
		notice.end_alert_time = end_alert_time
		notice.save()
		cr.result = notice.id

		log = service.common.logging.createLog(lemon.basetype.LogActionType.L312,notice.title,request=r)
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(errors.ErrorDefs.InternalException)
	return cr.httpResponse()



@csrf_exempt
def removeNotice(req):
	"""
	删除系统通知消息
	"""
	cr = webapi.SuccCallReturn()
	callback = None
	try:
		notice_id =  webapi.GET(req,'id')
		callback = webapi.GET(req,'callback')
		cr.setCallBackJsonp(callback)
		notice = core.Notice.objects.get(id = int(notice_id))
		core.Notice.objects.filter( id = int(notice_id)).delete()

		log = service.common.logging.createLog(lemon.basetype.LogActionType.L314,notice.title,request=req)
		log.save()

	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(errors.ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()

@csrf_exempt
def updateNotice(r):
	"""
	更新系统通知消息
	"""
	cr = webapi.SuccCallReturn()
	callback = None
	try:
		notice_id = webapi.GET(r,'id')
		title =  webapi.GET(r,'title')
		content = webapi.GET(r,'content')

		alert = webapi.GET(r,'alert',0)
		end_alert_time = webapi.GET(r,'end_alert_time',None)
		alert = int(alert)
		if alert:
			alert = True
		else:
			alert = False

		if end_alert_time:
			end_alert_time = lemon.utils.misc.mk_datetime(end_alert_time)


		callback = webapi.GET(r,'callback')
		cr.setCallBackJsonp(callback)
		if  not notice_id:
			return webapi.FailCallReturn(errors.ErrorDefs.ParameterIllegal).httpResponse()

		user_id = webapi.sessionValue(r,'user_id')
		admin = core.AdminUser.objects.get(id = int(user_id))
		notice = core.Notice.objects.get( id = int(notice_id))
		notice.issuer = admin
		if title!=None:
			notice.title = title[:255]
		if content!=None:
			notice.content = content[:2000]
		notice.modify_time = datetime.datetime.now()
		notice.alert = alert
		notice.end_alert_time = end_alert_time

		notice.save()
		cr.result = notice.id

		log = service.common.logging.createLog(lemon.basetype.LogActionType.L313,notice.title,request=r)
		log.save()
	except:
		traceback.print_exc()
		cr = webapi.FailCallReturn(errors.ErrorDefs.InternalException).setCallBackJsonp(callback)
	return cr.httpResponse()

