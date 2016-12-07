# -- coding:utf-8 --

"""
 初始化系统结构树
"""

import  imp
import os,sys,datetime
imp.load_source('init','../init_script.py')
PATH = os.path.dirname(os.path.abspath(__file__))





sys.path.append(PATH+'/../')
import model.django.core.models as core
import lemon.encrypt
import lemon.utils.misc
import model.django.project.settings
import base64



def clearup():
	print "clear table data..."
	core.AdminUser.objects.all().delete()

SYS_ID='ras_sh_001'

AdminUsers=[
	{'name':'sysadmin','passwd':'111111','type':'sys'},
	#{'name':'sysadmin','passwd':'111111','type':'sys'},
	#{'name':'secadmin','passwd':'111111','type':'sec'},
	#{'name':'logadmin','passwd':'111111','type':'log'},
]


def create_admin_user():
	print "create_admin_user..."

	for e in AdminUsers:
		user = core.AdminUser()

		user.login = e['name']
		user.password = lemon.encrypt.md5(e['passwd'])
		user.name = user.login
		user.role = core.AdminUser.ROLE_SYS
		if e['type'] == 'sec':
			user.role = core.AdminUser.ROLE_SEC
		elif e['type'] == 'log':
			user.role = core.AdminUser.ROLE_LOG
		user.create_time = datetime.datetime.now()
		user.save()

	print "create_admin_user successful!"

def init_database():
	clearup()
	create_admin_user()
	# init_server_certificate()

def init_server_license():
	"""	:return:
	"""

def test_recalculate_cer_hash():
	for cer in core.AppCertificate.objects.all():
		cer.hash_cer = lemon.encrypt.md5( base64.b64decode(cer.cer) )
		cer.hash_pfx = lemon.encrypt.md5( base64.b64decode(cer.pfx) )
		cer.save()


def test_init_certificate():
	"""
	初始化服务器证书
	:return:
	"""

	core.AppCertificate.objects.all().delete()
	cert_path = PATH+'/../etc/cert'
	for file in os.listdir(cert_path+'/cer'):
		name = cert_path+'/cer/'+file
		f = open(name,'rb')
		data = f.read()
		f.close()
		data_cer = base64.b64encode(data)

		name = cert_path+'/pfx/'+ os.path.splitext(file)[0]+'.p12'
		f = open(name,'rb')
		data = f.read()
		f.close()
		data_pfx = base64.b64encode(data)

		data_passwd = '111111'

		cert = core.AppCertificate(
			name=os.path.splitext(file)[0],
			cer = data_cer,
			pfx = data_pfx,
			type = 1 ,
			passwd = data_passwd,
			hash_cer = lemon.encrypt.md5(base64.b64decode(data_cer) ),
			hash_pfx = lemon.encrypt.md5(base64.b64decode(data_pfx) ),
			create_time = datetime.datetime.now(),
			expire_time = datetime.datetime.now(),
			status = 1
		)
		cert.save()



# def init_server_certificate():
# 	"""
# 	初始化服务器证书
# 	:return:
# 	"""
#
# 	# core.AppCertificate.delete()
# 	cert_path = PATH+'/../etc/cert'
# 	f = open(cert_path+'/server.cer','rb')
# 	data = f.read()
# 	f.close()
# 	data_cer = base64.b64encode(data)
#
# 	f = open(cert_path+'/server.pfx','rb')
# 	data = f.read()
# 	f.close()
# 	data_pfx = base64.b64encode(data)
#
# 	data_passwd = '111111'
#
# 	cert = core.AppCertificate(
# 		name='server_certificate',
# 		cer = data_cer,
# 		pfx = data_pfx,
# 		type = 1 ,
# 		passwd = data_passwd,
# 		hash_cer = base64.b64encode(data_cer),
# 		hash_pfx = base64.b64encode(data_pfx),
# 		create_time = datetime.datetime.now(),
# 		expire_time = datetime.datetime.now(),
# 		status = 1
# 	)
# 	cert.save()


def test_init_appserver():
	core.AppServer.objects.all().delete()
	server = core.AppServer( app = core.Application.objects.filter()[0],
		name='192.168.10.100',
		ip_addr = '192.168.10.100',
		is_addr_restricted = False,
		create_time = datetime.datetime.now(),
		access_token = '100',
		secret_key = '100',
		status = 1
	)
	server.save()


def test_init_data():

	test_init_certificate()

	core.Application.objects.all().delete()
	cert = core.AppCertificate.objects.all()[0]
	app = core.Application(app_id='first.app',
		name='first_app_name',
		create_time = datetime.datetime.now(),
		status = 1,
		license = None,
		max_lic_num = 30,
		cert = cert
	)
	cert.status = 3
	app.save()

	test_init_appserver()


if __name__ == "__main__":
	# test_recalculate_cer_hash()

	print "init start..."
	init_database()
	# test_init_data()
	print "init successful!"

