#--coding:utf-8--

"""
Initial data block command:

   dd if=/dev/zero of=block_1m.dat bs=1M count=1

"""
import imp
imp.load_source('init','../../init_script.py')

import gevent
from gevent import monkey
#monkey.patch_all(socket=True,time=True,ssl=True,sys=True)
monkey.patch_all()

import os,os.path,sys,struct,time,traceback,signal,threading,copy,base64,urllib,json
import datetime,base64
from datetime import datetime

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2


webserver = 'http://127.0.0.1:8088'
webserver = 'http://172.16.10.64:8088'
webapi = webserver+'/api/fileserver'
user_name='scott'
user_token=''


import cookielib
cookie = cookielib.CookieJar()
cookie_file = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(cookie_file)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}




test_cer_hash = '8dff1cb3c37290d90d1c9c948d6aec26'  # user(scott) cer

test_case_list=[
	{'name':'login','webapi':'/login/',
		'params':{	'access_token':'0c22c328643d4692ae91f2016e4de8ab',
					'secret_key':'22BN57','username':'test',
				},
		'headers':{

		}
	},{'name':'logout','webapi':'/logout/',
		'params':{
				},
		'headers':{

		}
	},
]

token=''

def get_case(name):
	for case in test_case_list:
		if case['name'] == name:
			return case
	return None

def execute(case):
	global  token

	print 'do test:(',case['name'],')'
	for n in range(1):
		if case.get('headers'):
			for k,v in case.get('headers').items():
				headers[k] = v

		headers['token'] = token

		if case.get('params'):
			req = urllib2.Request(webapi + case['webapi'] ,urllib.urlencode(case['params']),headers=headers)
		else:
			req = urllib2.Request(webapi + case['webapi'],headers=headers)

		resp =opener.open(req)

		data = resp.read()
		print data
		if case['name'] == 'login':
			obj = json.loads(data)
			token = obj['result']


def test_user_login():
	case = test_case_list[0]
	execute(case)

def  test_create_file( filename ):

	try:
		case = test_case_list[0]
		execute(case)

		url = webapi + '/files/'
		register_openers()
		datagen, headers = multipart_encode({"file": open( filename, "rb")})
		headers['token'] = token
		request = urllib2.Request(url, datagen, headers)
		print url
		resp = urllib2.urlopen(request)
		data = resp.read()
		storage_id = json.loads(data)['result']
		print 'create new file id:', storage_id
		return storage_id

		# fp = open( pdf,'wb')
		# fp.write( data)
		# fp.close()
	except:
		traceback.print_exc()
	return True

def test_login_logout():
	for case in test_case_list:
		execute(case)

def  test_get_file( file_id ):

	try:
		case = test_case_list[0]
		execute(case)

		url = webapi + '/files/?id=' + file_id
		register_openers()
		headers['token'] = token
		request = urllib2.Request(url,headers= headers)
		resp = urllib2.urlopen(request)

		data = resp.read()
		print 'retrieve data: ' ,len(data)
		print data
		fp = open( 'get_file.txt','wb')
		fp.write( data)
		fp.close()

	except:
		traceback.print_exc()
	return True

def test_login_logout():
	for case in test_case_list:
		execute(case)

def  test_delete_file( file_id ):
	try:
		case = test_case_list[0]
		execute(case)

		url = webapi + '/files/?id=' + file_id
		register_openers()
		headers['token'] = token
		request = urllib2.Request(url,headers= headers)
		request.get_method = lambda :'DELETE'

		resp = urllib2.urlopen(request)

		data = resp.read()
		print data
	except:
		traceback.print_exc()
	return True

def test_maketrans():
	import string

	ins = "/=\\,+&%$#@~`|?:"
	outs = '-'* len(ins)
	tabs = string.maketrans(ins,outs)
	print "#@#$@#4abc%".translate(tabs)

def test_share_file(from_user,to_user,file_id):
	case = get_case('login')
	case.get('params')['username'] = from_user
	execute(case)

	url = webapi + '/share/'
	register_openers()
	headers['token'] = token
	data={
		'id': file_id,
		'client_id': to_user
	}
	data = urllib.urlencode( data )
	request = urllib2.Request(url,data,headers= headers)
	resp = urllib2.urlopen(request)
	data = resp.read()
	print data


def test_perform_upload_file(max_request=1000):
	filename = './block_1m.dat'
	
	task_list=[]
	for x in xrange(max_request):
		task = 	gevent.spawn( test_create_file , filename) 
		task_list.append(task)
	gevent.joinall( task_list ) 
	print 'task completed'
	
if __name__ == '__main__':

	test_perform_upload_file(200)

#storage_id='5897885c5e3775a03cb18455f79afb1c'

#storage_id = test_create_file('./init_data.py')
# test_get_file('9f9bd036bf3834cb2b6f25268840a9cd')
#test_get_file( storage_id )
# test_delete_file( storage_id )
# test_maketrans()
# test_user_login()
# test_share_file('test2','test1','532b245425d33afce330adfdb22161f9')

