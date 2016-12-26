#coding:utf-8
__author__ = 'zhangbin'


import swiftclient as sw
from django.utils.http import urlsafe_base64_encode


"""

tenant -     global account for cloudfish
containter - application id
  directory - user of application
    object  -  user's file


curl -X POST -d '{"auth”: {"passwordCredentials":{"username": "admin", "password": "605ab45d701f4256"}}}' -H "Content-type: application/json" http://172.16.10.249:5000/v2.0/tokens | python -mjson.tool

http://docs.openstack.org/developer/python-swiftclient/client-api.html#examples

"""




class SwiftServer:
	def __init__(self):
		self.conn_list =[]
		self.conn_index =0		

	_handle = None

	@staticmethod
	def instance():
		if SwiftServer._handle == None:
			SwiftServer._handle = SwiftServer()
		return SwiftServer._handle

	def open(self,authurl,user,key,tenant,pool_size=5):
		authurl = authurl
		auth_version = '2'
		# _auth_version = '1'
		user = user
		key = key
		tenant_name = tenant
		if self.conn_list:
			return self
			
		for _ in xrange(pool_size):
			conn = sw.client.Connection(
				authurl=authurl,
				user=user,
				key=key,
				tenant_name=tenant_name,
				auth_version=auth_version
			)
			self.conn_list.append( conn ) 
		
		return self
	
	def next_conn(self):
		conn = None
		if self.conn_index == len(self.conn_list):
			self.conn_index = 0 
		conn = self.conn_list[self.conn_index]
		self.conn_index+=1 
		return conn 
	
	def free(self,conn):
		pass
		
	def reset(self):
		pass 
		
	
def reset_swift_connection():
	SwiftServer.instance().reset()

def get_swift_connection():
	from  lemon.utils.app import BaseAppServer
	conf = BaseAppServer.instance().getConfig()
	authurl = conf.get('swift_auth_server')
	user = conf.get('swift_username')
	key  = conf.get('swift_password')
	tenant = conf.get('swift_tenant_name')
	conn = SwiftServer.instance().open(authurl,user,key,tenant).next_conn()
	return conn
	
def free_swift_connection(conn):
	""" put connection object free , or put back into pool"""
	SwiftServer.instance().free( conn ) 
	
def secured_connection(func):
	def _wrapper(*args,**kwargs):
		conn = get_swift_connection()
		if conn:
			try:
				ret = func( conn,*args,**kwargs )
			except:
				raise 'error: detail code on connection execution broken' 
			free_swift_connection(conn)
			return ret 
		else:
			print 'error: swift connection cannot allocated'
			raise "swift resource(connection) insufficiant,please enlarge connection numbers"
	return _wrapper
	
@secured_connection	
def create_application(conn,app_id,should_hash=False):
	"""
	create container in swift with app_id
	:param app_id:
	:return:
	"""
	#conn = get_swift_connection()
	if should_hash:
		app_id = hash_application_id(app_id)
	conn.put_container( hash_application_id(app_id))

@secured_connection
def create_user_file(conn,container,user_storage_id,file_name,content):
	#conn = get_swift_connection()
	file_name = hash_appuser_id(user_storage_id)+'/'+hash_appfile_id(file_name)
	conn.put_object(container,file_name,contents= content)
	return  file_name

@secured_connection
def delete_user_file(conn,container,file_name):
	#conn = get_swift_connection()
	conn.delete_object(container,file_name)

@secured_connection
def get_user_file(conn,container,file_name):
	#conn = get_swift_connection()
	headers,obj_contents = conn.get_object(container,file_name)
	return obj_contents


def hash_application_id(app_id):
	from lemon.utils.misc import getdigest
	app_id = getdigest( app_id)
	return 'app_'+ app_id

def hash_appuser_id(user_name):
	return user_name

def hash_appfile_id(file_name):
	return file_name



def test_swift():
	_authurl = 'http://172.16.10.249:5000/v2.0/'
	_authurl = 'http://172.16.10.61:5000/v2.0/'
	_auth_version = '2'
	# _auth_version = '1'
	_user = 'admin'
	_key = '605ab45d701f4256'
	_key = '111111'
	_tenant_name = 'admin'

	conn = sw.client.Connection(
		authurl=_authurl,
		user=_user,
		key=_key,
		tenant_name=_tenant_name,
		auth_version=_auth_version
	)

	# print conn.token
	headers,containers = conn.get_account()
	print 'containers:',containers
	# print conn.get_auth()
	overview,files = conn.get_container("yidong")
	for f in files :
		print f

	# print conn.put_object('cc01',"001/abc.txt",contents="china city.")
	#print conn.delete_object('cc01',"001/abc.txt")
	# print conn.get_object("cc01",u'\u80d6\u5b50-cap.jpg')
	# print conn.get_object("cc01",u'f01/swift.conf')
	# print conn.put_container("002")

if __name__ == '__main__':
	test_swift()
