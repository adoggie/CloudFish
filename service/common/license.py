#coding:utf-8

import os,sys,traceback,base64,struct
from ctypes import *

import sfflib
import lemon.errors
import model.django.core.models as core
import cloudfish.base,cloudfish.errors
import service.common.config

def create_auth_data(identity,license=None):
	"""
	丧生成授权数据
	:param auth_code:
	:return:
	"""
	if not license:
		license = service.common.config.license
	auth_key = ''
	try:
		libtAuth = cdll.LoadLibrary('libfasauthcore.so')
		size = c_uint(200*1000)
		c_size = pointer(size)
		s1 = create_string_buffer('\0'*size.value)
		rc = libtAuth.CheckAuthCertFile(license)
		if rc != 0 :
			print 'identity:',identity
			print "errcode:%x"%struct.unpack('I',struct.pack('i',rc))
			return None
		rc = libtAuth.GenerateAuthFile(identity.encode("utf-8"),len(identity.encode("utf-8")),s1,byref(size))
		if rc != 0:

			print 'GenerateAuthFile()  failed,errcode:%x'%struct.unpack('I',struct.pack('i',rc))
			return None
		auth_key = s1.value
	except:
		traceback.print_exc()
	auth_key = base64.b64encode(auth_key)
	return auth_key

def get_license_info(license=None):
	"""
		'tLicesenceTerm',		c_uint64),
		nClientNum',
		"""

	if not license:
		license = service.common.config.license
	auth= sfflib.getAuInfo(license)
	if not auth:
		return None
	return auth


def assign_user_certificate(user):
	try:
		if user.app.appuser_set.all().exclude(cert=None).count() > user.app.max_lic_num:
			# licese num reached top limit.
			return cloudfish.errors.ErrorDefs.AUTH_NUM_INSUFFICTION

		rs = core.AppCertificate.objects.filter(status=cloudfish.base.CERT_STATUS_ENABLED)
		if not rs:
			return cloudfish.errors.ErrorDefs.AUTH_NUM_INSUFFICTION
		cert=rs[0]
		user.cert = cert
		user.save()
		cert.status = cloudfish.base.CERT_STATUS_ASSIGNED
		cert.save()
	except:
		traceback.print_exc()
		return lemon.errors.ErrorDefs.InternalException
	return cloudfish.errors.ErrorDefs.SUCC


def licenseCheck(lic):
	try:
		identity = sfflib.getidentity()
		libtAuth = cdll.LoadLibrary('libfasauthcore.so')
		rc = libtAuth.CheckAuthCertFile(lic)
		if rc != 0 :
			print 'identity:',identity
			print "errcode:%x"%struct.unpack('I',struct.pack('i',rc))
			return False
	except:
		traceback.print_exc()
		return False
	return True


def get_identity():
	identity = sfflib.getidentity()
	return identity
