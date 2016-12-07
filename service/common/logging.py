#--coding:utf-8 --

__author__ = 'root'

import model.django.core.models as core

def createLog(action,detail=None,request=None):
	"""
	日志记录辅助创建函数
	:param act:	 basetype.LogActionType.XXX
	:param detail:
	:param result:
	:param request: http request
	:return:
	"""
	import lemon.webapi
	import lemon.basetype
	import datetime
	act = core.LogAdminUserAction()
	act.issue_time = datetime.datetime.now()
	act.action = action
	if request:
		act.user_role =  lemon.webapi.sessionValue(request,'user_role')
		user_id = lemon.webapi.sessionValue(request,'user_id')
		user = core.AdminUser.objects.get(id=user_id)
		act.user = user.login
	if detail:
		act.detail = detail
	return act