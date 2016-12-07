#-- coding:utf-8 --
 
#调用中间件示例
from ctypes import *
import os 
import sfflib

#获取机器码
try:
	identity = sfflib.getidentity()
	print "identity OK  = " + identity
except Exception,ex:
	print "getidentity error: " ,Exception,":",ex




	
