#coding:utf-8
# __author__ = 'root'

import os,time,sys,traceback
import gevent
import gevent.subprocess
from gevent.subprocess import  Popen,PIPE

def encrypt_file(filename,passwd):
	"""
	encrypt file and return new file
	:param filename:
	:param passwd:
	:return:
	"""
	rc = -1
	target_des = filename+'.des'
	try:
		cmd = "tar -zcf - %s | openssl des3x -salt -k %s | dd of=%s"%(filename,passwd,target_des)
		cmd_list = cmd.split(' ')
		sub = Popen([cmd],stdout=PIPE,shell=True)
		out,err = sub.communicate()
		print err
		print sub
		# print cmd_list
		# rc =  gevent.subprocess.call(cmd_list)
	except:
		traceback.print_exc()
	print 'encrypt_file call return:',rc
	if rc!=0:
		target_des = ''
	return target_des


encrypt_file('init_data.py','1111111')