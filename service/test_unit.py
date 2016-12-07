#coding:utf-8
__author__ = 'root'



def test():
	import service.common.license
	print service.common.license.get_identity()

	# print service.common.license.licenseCheck('/home/projects/cloudfish/test/license160112-3-10-100.cer')
	auth = service.common.license.get_license_info('/home/projects/cloudfish/test/license160112-3-10-100.cer')
	print auth.tLicesenceTerm,auth.nClientNum

	#
	#print service.common.license.create_auth_data( service.common.license.get_identity(),'/home/projects/cloudfish/test/license160112-3-10-100.cer')


