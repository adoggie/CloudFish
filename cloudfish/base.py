#--coding:utf-8--


import os,os.path,sys,struct,time,traceback,signal,threading,datetime

#管理员角色类型
AMDIN_ROLE_SYS= 0x01
AMDIN_ROLE_SEC= 0x02
AMDIN_ROLE_LOG= 0x04

# 加密算法类
ENC_TYPE_RSA = 1
ENC_TYPE_IBC = 2

# 状态类型
STATUS_TYPE_UNSET    = 0
STATUS_TYPE_ENABLED  = 1
STATUS_TYPE_DISABLED = 2

# 证书状态
CERT_STATUS_ENABLED = 1 #可用
CERT_STATUS_DISABLED = 2 #不可用
CERT_STATUS_ASSIGNED = 3 #已分配
CERT_STATUS_REMOVED = 4 # 已删除


NODE_TYPE_SERVER = 1
NODE_TYPE_CLIENT = 2
NODE_TYPE_BACKEND_CLIENT = 3	#服务器侧 客户端用户  2016.1.18

ACCESSOR_TYPE_ROOT = 1	#登录用户类型
ACCESSOR_TYPE_NORMAL = 2

class ResultType:
	RESULT_SUCC = 0
	RESULT_FAIL = 1

	@staticmethod
	def nameValue(type):
		name = ''
		if type ==ResultType.RESULT_SUCC:
			name+=u'操作成功'
		if type ==ResultType.RESULT_FAIL:
			name+=u'操作失败'
		return name

# 管理员
class AdminUserType:
	SYS 	= 0x01                 # 系统管理员
	SEC 	= 0x02                   # 安全审计管理员
	LGO 	= 0x04               # 安全保密管理员

	@staticmethod
	def nameValue(type):
		name = ''
		if not type:
			return name
		if type& AdminUserType.SYS:
			name+=u'系统管理员'
		if type& AdminUserType.SEC:
			if name:name+=','
			name+=u'安全保密管理员'
		if type& AdminUserType.LGO:
			if name: name+=','
			name+=u'安全审计管理员'
		return name

# 帐号类型
class AppUserType:
	server 	= 1                 # 服务端
	client 	= 2                   # 客户端
	backend_client = 3            #	服务器客户端

	@staticmethod
	def nameValue(type):
		name = ''
		if not type:
			return name
		if type ==AppUserType.server:
			name+=u'服务器'
		if type ==AppUserType.client:
			name+=u'客户端'
		if type ==AppUserType.backend_client:
			name+=u'服务端客户'
		return name

class UserType:
	backend_client = False
	backend_server = True

	@staticmethod
	def nameValue(type):
		name=u'前端'
		if type ==UserType.backend_client:
			name=u'前端'
		if type ==UserType.backend_server:
			name=u'后端'
		return name

class AdminUserActionType:
	Login = 1
	Logout = 2
	ChangePassword = 3
	ChangeUserProfile = 4

	CreateApplicate = 11
	UpdateApplicate = 12
	DeleteApplicate = 13
	EnableApplicate = 14
	DisableApplicate = 15
	AuthAppLicense = 16
	UnAuthAppLicense = 17
	BindAppCertificate = 18
	UnBindAppCertificate = 19

	CreateCertificate = 31
	DeleteCertificate = 32
	EnableCertificate = 33
	DisableCertificate = 34
	AvailableCertificate = 35
	importUserCertificate = 36
	importAppCertificate = 37
	ExportUserCertificate = 38
	ExportAppCertificate = 39

	CreateAppUser = 51
	DeleteAppUser = 52
	EnableAppUser = 53
	DiableAppUser = 54
	BindAppUserCertificate = 55
	UnBindAppUserCertificate = 56
	UpdateAppUser = 57
	ChangeAppUserPassword = 58

	CreateAppServer = 71
	UpdateAppServer = 72
	DeleteAppServer = 73
	EnableAppServer = 74
	DisableAppServer = 75

	@staticmethod
	def nameValue(type):
		name = ''
		if not type:
			return name
		if type:
			if type ==AdminUserActionType.Login:
				name+=u'管理员登录'
			if type ==AdminUserActionType.Logout:
				name+=u'管理员注销'
			if type ==AdminUserActionType.ChangePassword:
				name+=u'修改密码'
			if type ==AdminUserActionType.ChangeUserProfile:
				name+=u'更改用户信息'
			if type ==AdminUserActionType.CreateApplicate:
				name+=u'创建应用'
			if type ==AdminUserActionType.UpdateApplicate:
				name+=u'修改应用'
			if type ==AdminUserActionType.DeleteApplicate:
				name+=u'删除应用'
			if type ==AdminUserActionType.EnableApplicate:
				name+=u'启用应用'
			if type ==AdminUserActionType.DisableApplicate:
				name+=u'禁用应用'
			if type ==AdminUserActionType.AuthAppLicense:
			    name+=u'绑定应用'
			if type ==AdminUserActionType.UnAuthAppLicense:
				name+=u'取消应用授权'
			if type ==AdminUserActionType.BindAppCertificate:
				name+=u'绑定应用证书'
			if type ==AdminUserActionType.UnBindAppCertificate:
				name+=u'取消应用证书'
			if type ==AdminUserActionType.CreateCertificate:
				name+=u'创建证书'
			if type ==AdminUserActionType.DeleteCertificate:
				name+=u'删除证书'
			if type ==AdminUserActionType.EnableCertificate:
				name+=u'启用证书'
			if type ==AdminUserActionType.DisableCertificate:
				name+=u'禁用证书'
			if type ==AdminUserActionType.AvailableCertificate:
				name+=u'激活证书'
			if type ==AdminUserActionType.CreateAppUser:
				name+=u'创建账号'
			if type ==AdminUserActionType.DeleteAppUser:
				name+=u'删除账号'
			if type ==AdminUserActionType.EnableAppUser:
				name+=u'启用账号'
			if type ==AdminUserActionType.DiableAppUser:
				name+=u'禁用账号'
			if type ==AdminUserActionType.BindAppUserCertificate:
				name+=u'绑定账号证书'
			if type ==AdminUserActionType.UnBindAppUserCertificate:
				name+=u'取消绑定账号证书'
			if type ==AdminUserActionType.UpdateAppUser:
				name+=u'修改账号'
			if type ==AdminUserActionType.ChangeAppUserPassword:
				name+=u'修改账号密码'
			if type ==AdminUserActionType.CreateAppServer:
				name+=u'创建应用服务器'
			if type ==AdminUserActionType.UpdateAppServer:
				name+=u'修改应用服务器'
			if type ==AdminUserActionType.DeleteAppServer:
				name+=u'删除应用服务器'
			if type ==AdminUserActionType.EnableAppServer:
				name+=u'启用应用服务器'
			if type ==AdminUserActionType.DisableAppServer:
				name+=u'禁用应用服务器'
		return name

class AppUserActionType:
	"""
	终端用户操作行为记录
	"""
	ServerAuthRegister = 11		#
	ClientAuthRegister = 12		#设备授权
	EncryptFile = 13			#
	DecryptFile= 14				#
	UserLogin = 15
	UserLogout = 16
	GetCertification = 17
	GetUserStatusByCer = 18

	# followings be new added in
	CLIENT_USER_LOGIN = 101
	CLIENT_USER_LOGOUT = 102
	CLIENT_USER_CREATE_FILE = 201
	CLIENT_USER_GET_FILE = 202
	CLIENT_USER_DELETE_FILE = 203
	CLIENT_USER_SHARE_FILE = 204

	@staticmethod
	def nameValue(type):
		name = ''
		if not type:
			return name
		if type:
			if type == AppUserActionType.CLIENT_USER_LOGIN:
				name+=u'CLIENT_USER_LOGIN'
			if type == AppUserActionType.CLIENT_USER_LOGOUT:
				name+=u'CLIENT_USER_LOGOUT'
			if type  == AppUserActionType.CLIENT_USER_CREATE_FILE:
				name+=u'CLIENT_USER_CREATE_FILE'
			if type == AppUserActionType.CLIENT_USER_GET_FILE:
				name += u'CLIENT_USER_GET_FILE'
			if type == AppUserActionType.CLIENT_USER_DELETE_FILE:
				name+= u'CLIENT_USER_DELETE_FILE'
			if type == AppUserActionType.CLIENT_USER_SHARE_FILE:
				name+=u'CLIENT_USER_SHARE_FILE'

			if type ==AppUserActionType.ServerAuthRegister:
				name+=u'服务器授权注册'
			if type ==AppUserActionType.ClientAuthRegister:
				name+=u'客户端授权注册'
			if type ==AppUserActionType.EncryptFile:
				name+=u'文件加密'
			if type ==AppUserActionType.DecryptFile:
				name+=u'文件解密'
			if type ==AppUserActionType.UserLogin:
				name+=u'客户端登录'
			if type ==AppUserActionType.UserLogout:
				name+=u'客户端注销'
			if type ==AppUserActionType.GetCertification:
				name+=u'获取证书'
		return name





