# coding:utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import model.django.core.models as core
import model.django.project.settings

from lemon import webapi
from lemon import basetype
from lemon import  errors

__author__ = ''


class Authentication:
	def __init__(self):
		pass

	def process_request(self, request):
		count = request.session.get('view_count')
		# request.session["view_count"] = 0


		if count is not None and count > 3:
			# return HttpResponse('Forbidden / Access Denied, already visit %s' % count)
			return None

		else:
			return None

class SessionMiddleware:
	def __init__(self):
		pass


	def process_request(self,req):
		"""
		session 检查
			- 超时或用户身份为鉴定，提示用户登录
		webapi权限调用检查
			- 业务用户与管理员api调用控制
			- 不同权限用户的api调用控制
		:param request:
		:return:
		"""
		if model.django.project.settings.DEBUG:
			print 'PATH:',req.path
			print 'GET:',req.GET
			print 'POST:',req.POST
			print 'USER_ID:',webapi.sessionValue(req,'user_id')
			print 'USER_ROLE:',webapi.sessionValue(req,'user_role')
			print 'USER_TYPE:',webapi.sessionValue(req,'user_type')

		real_ip = req.META.get('HTTP_X_REAL_IP')
		if real_ip:
			req.META['REMOTE_ADDR'] = real_ip
		prefix = '/webapi/'
		# if req.path[-1]!='/':
		# 	req.path +='/'
		# return
		#

		if req.path.find('/api/fileserver/')!=-1:
			return

		if req.path.find('/static/') != -1:
			return

		#此处必须判别 当前登录的用户类型 admin/user,
		if req.path.find(prefix) != -1:
			IGNAL_LIST=('/login','/logout','/getSignImage','/','/getIdentity')
			match = False
			for path in IGNAL_LIST:
				if req.path.find(path)!=-1:
					match = True
					break
			if match:
				return

			user_id = webapi.sessionValue(req,'user_id')
			# user_role = webapi.sessionValue(req,'user_id')
			# user_type = webapi.sessionValue(req,'user_type')	# user or admin_user
			if not user_id:
				return webapi.FailCallReturn(errors.ErrorDefs.SessionExpired).httpResponse()
			else:
				user_type = webapi.sessionValue(req,'user_type')
				# if req.path.find('/webapi/ras/')!=-1 and user_type!=basetype.LoginUserType.USER:
				# 	print 'error: cross user privillages access! (current user is not USER)'
				# 	return webapi.FailCallReturn(errors.ErrorDefs.PermissionDenied)
				# if req.path.find('/webapi/admin/')!=-1 and user_type!=basetype.LoginUserType.ADMIN:
				# 	print 'error: cross user privillages access! (current user is not ADMIN)'
				# 	return webapi.FailCallReturn(errors.ErrorDefs.PermissionDenied)

		# todo
		# 启用身份状态识别，导致 文件下载 错误： user_id 不存在 ？？？？
		# 可能是 /ras时注销了用户会话？？
		if 1:
			user_id = webapi.sessionValue(req,'user_id')
			if not user_id:
				# if req.path=='/admin/':
				return render_to_response('adminLogin.html')
				# else:
			# return render_to_response('adminIndex.html')
			return


