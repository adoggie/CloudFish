#--coding:utf-8--


import os,os.path,sys,struct,time,traceback,signal,threading,datetime

import lemon.errors
class ErrorDefs(lemon.errors.ErrorDefs):
	NO_CERTIFICATE =(5001,u'无可用的用户证书')
	AUTH_NUM_INSUFFICTION =(5002,u'应用授权数量限制')
	ADDRESS_RESTRICTED = (5003,u'ip address restricted')
