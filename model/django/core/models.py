# coding=utf-8

from django.db import models
from datetime import datetime

import cloudfish



class SystemParameter(models.Model):
	name = models.CharField(max_length=128,db_index=True)
	value = models.CharField(max_length=512,null=True)
	comment = models.CharField(max_length=256,null=True)
	delta = models.TextField(null=True)

# 
class AdminUser(models.Model):
	"""
	系统管理员 root
	"""
	login = models.CharField(max_length=20,db_index=True)								#
	password = models.CharField(max_length=40)											#
	name = models.CharField(max_length=40,db_index=True)								#
	role = models.SmallIntegerField(db_index=True)										# 
	create_time = models.DateTimeField(db_index=True)						                # 
	email = models.CharField(max_length=40,db_index=True,null=True)
	phone = models.CharField(max_length=20,db_index=True,null=True)

	ROLE_SYS= 0x01
	ROLE_SEC= 0x02
	ROLE_LOG= 0x04


class Application(models.Model):
	"""
	应用表
	"""
	app_id = models.CharField(max_length=40,unique=True)		# 
	name = models.CharField(max_length=40,db_index=True)		# 
	comment = models.CharField(max_length= 200,null=True)		# 
	create_time = models.DateTimeField(db_index=True)			# 
	creator = models.ForeignKey(AdminUser,null=True,db_index=True)	#
	status = models.SmallIntegerField()   							    # 1:enabled,2:disabled
	file_encrypt_shadow = models.CharField(max_length = 40,null=True)   # 文件加密密码关联key
	access_token = models.CharField(max_length=80,db_index=True)	# 应用于API访问登录、应用管理员登录（UI交互）
	secret_key = models.CharField(max_length=40)					#
	container_name = models.CharField(max_length=40,default='')	#swift存储容器


class AppUser(models.Model):
	"""
	外部应用系统内的用户账号
	"""
	app = models.ForeignKey(Application,db_index=True,related_name='appuser_set')
	name = models.CharField(max_length=40,db_index=True)                # 用户账号名
	last_login_time = models.DateTimeField(db_index=True,null =True)    # 最近一次登录时间
	status = models.SmallIntegerField()                                 # 1 -启用   ; 2 - 停用
	token = models.CharField(max_length=1000,null=True)                 #
	username = models.CharField(max_length=20,default='')               #用户名称（非登录名）
	passwd = models.CharField(max_length=40,default='')
	salt = models.CharField(max_length=10,default='')
	phone = models.CharField(max_length=30,null =True)
	address = models.CharField(max_length=80,null =True)
	create_time = models.DateTimeField(db_index=True)					#
	storage_id = models.CharField(max_length=40,default='')		#存储端的用户目录，散列生成


class LogAdminUserAction(models.Model):
	"""
	
	"""
	user = models.CharField(max_length=40,db_index=True)                #
	user_role = models.SmallIntegerField(db_index=True,default=0)   			# 
	action = models.SmallIntegerField(db_index=True)
	issue_time = models.DateTimeField(db_index=True)
	target = models.CharField(max_length=80,null=True)	#
	result = models.IntegerField() 	# succ - 0 ,else failed
	categary = models.CharField(max_length=40,db_index=True,null=True)
	detail = models.CharField(max_length=2000,null=True)


class LogAppUserAction(models.Model):
	"""
	
	"""
	user = models.CharField(max_length=40,db_index=True)
	token = models.CharField(max_length=1000,null=True)
	issue_time = models.DateTimeField(db_index=True)
	action = models.SmallIntegerField(db_index=True)
	target = models.CharField(max_length=80,null=True)	#
	result = models.IntegerField(default=0) 	# succ - 0 ,else failed
	categary = models.CharField(max_length=40,db_index=True,null=True)
	detail = models.CharField(max_length=2000,null=True)
	user_role = models.IntegerField() 	#用户类型 1 - normal ; 2 - root



class AppUserFile(models.Model):
	"""
	file info
	"""
	user = models.ForeignKey(AppUser,db_index=True,related_name='userfile_set')
	create_time = models.DateTimeField(db_index=True)
	storage_id = models.CharField(max_length = 200,db_index=True)	#文件名被转换成散列
	file_name = models.CharField(max_length =200,db_index=True)		#原始文件名称
	file_size = models.IntegerField(db_index=True)
	pick_passwd = models.CharField(max_length = 20,null=True)   # 文件访问密码
	digest = models.CharField(max_length = 40,db_index=True)    # 未加密前文件hash , MD5/SHA1
	access_id = models.CharField(max_length = 80,db_index=True,default='')    # 交换文件编号 digets+size+time => SHA
	access_salt = models.CharField(max_length = 40,default='')    # 交换文件编号 digets+size+time => SHA
# 统计
# 1. 应用使用存储空间状况
# 2. 应用内用户使用存储空间状况