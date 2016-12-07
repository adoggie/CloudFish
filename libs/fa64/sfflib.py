#-- coding:utf-8 --

from ctypes import *
import traceback,os,os.path,sys,time,ctypes
import base64
import StringIO

class C_ST_tagBuffer(Structure):
	_fields_ =	[
				('pbData',		c_void_p),
				('nLen',		c_uint)
			]

class C_ST_tagToken(Structure):
	_fields_ =	[
				('exCert',		C_ST_tagBuffer),
				('signCert',	C_ST_tagBuffer)
			]

class C_ST_tagExPrivilegeAttr(Structure):
	_fields_ =	[
				('nPriID',		c_ushort),
				('nReserve',	c_uint)
			]

class C_ST_tagExPrivilegeAttrList(Structure):
	_fields_ =	[
				('nExtPriCount',		c_uint),
				('pExtPriAttrList',	POINTER(C_ST_tagExPrivilegeAttr))
			]

class C_ST_tagPrivilegeAttr(Structure):
	_fields_ =	[
				('exCert',		POINTER(C_ST_tagBuffer)),
				('bRead',		c_ubyte),
				('uTotalRead',	c_uint),
				('uAlread',		c_uint),
				('bWrite',		c_ubyte),
				('bDel',		c_ubyte),
				('bPrint',		c_ubyte),
				('uPrintCount',	c_uint),
				('uPrintedCount',	c_uint),
				('exPriList',	C_ST_tagExPrivilegeAttrList)
			]

class C_ST_AuInfo(Structure):
	_fields_ =	[
				('szAppName',			c_char*55),
				('szDeptName',			c_char*55),
				('tInstallTerm',		c_uint64),
				('tLicesenceTerm',		c_uint64),
				('nClientNum',			c_ushort),
				('funCode',				c_char*64),
				('bID',					c_char*64)
			]


#获取授权文件属性
#返回授权文件属性
#clAuthFile 授权文件路径
def getAuInfo(clAuthFile):
	libsff = cdll.LoadLibrary('libfasauthcore.so')
	AuInfo = C_ST_AuInfo()
	ret = libsff.Au_GetAuInfo(clAuthFile,byref(AuInfo))

	if ret <> 0 :
		print "getAuInfo Error"
		return None
	return AuInfo



#获取机器码
#返回机器码，错误抛出异常
def getidentity():
	libsff = cdll.LoadLibrary('libfasauthcore.so')
	size = c_uint(200*1000)
	c_size = pointer(size)
	s1 = create_string_buffer('\0'*size.value)
	ret = libsff.GetIdentity(s1,c_size)
	if ret <> 0 :
		raise ImportError(ret)
	else:
		return s1.value

#初始化 每次服务启动运行一次
#返回0 正常 错误返回错误码
#szPriExPath PFX加密证书文件路径 szPriExPin 加密证书密码 szPriSignPath PFX签名证书路径 szPriSignPin 签名证书密码 szpServerpin 服务器保护证书密码
#szSavePath 发布路径 clAuthFile 许可文件路径
def init(szPriExPath, szPriExPin, szPriSignPath, szPriSignPin,szpServerpin, szSavePath, clAuthFile):
	# libsff = cdll.LoadLibrary('libsfl.so')
	libsff = cdll.LoadLibrary('libfasfl.so')
	ret = libsff.SFF_CheckAuthFile(clAuthFile)
	print "SFF_CheckAuthFile",ret
	if ret <> 0 :
		print "SFF_CheckAuthFile"
		return ret

	#设置私钥发布路径
	ret = libsff.SFF_SetKeyPath(szSavePath);
	if ret <> 0 :
		print "SFF_SetKeyPath"
		return ret;

	#发布加密私钥,和签名私钥
	ret = libsff.SFF_PublishUserKey(szPriExPath, szPriExPin, szPriSignPath, szPriSignPin,szpServerpin);
	if ret <> 0 :
		print "SFF_PublishUserKey"
		return ret;
	return ret

#明文到外联式标签(密文+纯标签)
#exServerCertOfbase64 CER加密证书(base64编码) siServerCertOfbase64 CER签名证书(base64编码) szpServerpin 服务器保护证书密码 
#szSavePath 发布路径 szPlainFile 标签文件路径 szCryptFile 密文实体文件路径 szSflFile 明文路径
def EncryptFile(exServerCertOfbase64,siServerCertOfbase64,szpServerpin,szSavePath,szPlainFile,szCryptFile,szSflFile):
	exServerCert = base64.b64decode(exServerCertOfbase64)
	siServerCert = base64.b64decode(siServerCertOfbase64)

	exServerCertBuffer = C_ST_tagBuffer()
	exServerCertBuffer.nLen = len(exServerCert)
	exServerCertBuffer.pbData = cast(exServerCert, c_void_p)

	
	siServerCertBuffer = C_ST_tagBuffer()
	siServerCertBuffer.nLen = len(siServerCert)
	siServerCertBuffer.pbData = cast(siServerCert, c_void_p)
	
	sToken = C_ST_tagToken()	
	sToken.exCert	=	exServerCertBuffer
	sToken.signCert 	= 	siServerCertBuffer	

	
	libsff = cdll.LoadLibrary('libfasfl.so')
	if libsff.SFF_IsLabel(szSflFile) == 0 :
		return 1
	# 登陆
	ret = libsff.SFF_LoginMultip(szpServerpin, szSavePath,byref(sToken)) 
	if ret <> 0 :
		return ret;
	
	pSfl = c_void_p()
	
	# 新建标签
	ret = libsff.SFF_OpenSFL(byref(sToken), None , byref(pSfl))
	if ret <> 0 :
		return ret
	
	# 加密文件
	ret = libsff.SFF_ExternalWriteSF(pSfl,szSflFile,szCryptFile)
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret
	
	# 保存标签文件
	ret = libsff.SFF_SaveSFL(pSfl,szPlainFile)
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret
	
	ret = libsff.SFF_CloseSFL(pSfl)
	if ret <> 0 :
		return ret
	
	return 0


#外联式标签(密文+纯标签)到新的内联式标签
#exServerCertOfbase64 CER加密证书(base64编码) siServerCertOfbase64 CER签名证书(base64编码) szpServerpin 服务器保护证书密码 
#szSavePath 发布路径 szPlainFile 标签文件路径 szCryptFile 密文实体文件路径 szCryptSflFile 内联式标签路径
#exUserCertOfbase64 添加的用户CER加密证书(base64编码) 
def LabelFile(exServerCertOfbase64,siServerCertOfbase64,szpServerpin,szSavePath,exUserCertOfbase64,szPlainFile,szCryptFile,szCryptSflFile):	
	exServerCert = base64.b64decode(exServerCertOfbase64)
	siServerCert = base64.b64decode(siServerCertOfbase64)

	exServerCertBuffer = C_ST_tagBuffer()
	exServerCertBuffer.nLen = len(exServerCert)
	exServerCertBuffer.pbData = cast(exServerCert, c_void_p)

	
	siServerCertBuffer = C_ST_tagBuffer()
	siServerCertBuffer.nLen = len(siServerCert)
	siServerCertBuffer.pbData = cast(siServerCert, c_void_p)
	
	sToken = C_ST_tagToken()	
	sToken.exCert	=	exServerCertBuffer
	sToken.signCert 	= 	siServerCertBuffer
	
	libsff = cdll.LoadLibrary('libfasfl.so')
	if libsff.SFF_IsLabel(szPlainFile) <> 0 :
		return 1
	# 登陆
	ret = libsff.SFF_LoginMultip(szpServerpin, szSavePath,byref(sToken)) 
	if ret <> 0 :
		return ret;
	
	pSfl = c_void_p()
	
	# 打开标签
	ret = libsff.SFF_OpenSFL(byref(sToken), szPlainFile , byref(pSfl))
	if ret <> 0 :
		return ret
	
	
	pAttr = C_ST_tagPrivilegeAttr()

	exUserCert = base64.b64decode(exUserCertOfbase64)
	exUserCertBuffer = C_ST_tagBuffer()
	exUserCertBuffer.nLen = len(exUserCert)
	exUserCertBuffer.pbData = cast(exUserCert, c_void_p)
	
	pAttr.exCert = pointer(exUserCertBuffer)
	
	pAttr.bRead 		= 1		#读权限
	pAttr.uTotalRead 	= 0		#可读份数
	pAttr.uAlread 		= 0		#已读份数
	pAttr.bWrite 		= 1		#修改文件权限
	pAttr.bDel 			= 1		#删除权限
	pAttr.bPrint 		= 1		#打印权限
	pAttr.uPrintCount 	= 0		#可打印份数
	pAttr.uPrintedCount = 0		#已打印份数

	# 添加权限
	ret = libsff.SFF_AddPrivilegeAttr(pSfl,byref(pAttr))
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret
	
	# 合并文件
	ret = libsff.SFF_ExternalToInternal(pSfl,szCryptFile,szCryptSflFile)
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret
	
	
	ret = libsff.SFF_CloseSFL(pSfl)
	if ret <> 0 :
		return ret
	
	return 0

#外联式标签(密文+纯标签)到新的内联式标签(先合并在添加权限)
#exServerCertOfbase64 CER加密证书(base64编码) siServerCertOfbase64 CER签名证书(base64编码) szpServerpin 服务器保护证书密码
#szSavePath 发布路径 szPlainFile 标签文件路径 szCryptFile 密文实体文件路径 szCryptSflFile 内联式标签路径
#exUserCertOfbase64 添加的用户CER加密证书(base64编码)
def LabelFileNew(exServerCertOfbase64,siServerCertOfbase64,szpServerpin,szSavePath,exUserCertOfbase64,szPlainFile,szCryptFile,szCryptSflFile):
	exServerCert = base64.b64decode(exServerCertOfbase64)
	siServerCert = base64.b64decode(siServerCertOfbase64)

	exServerCertBuffer = C_ST_tagBuffer()
	exServerCertBuffer.nLen = len(exServerCert)
	exServerCertBuffer.pbData = cast(exServerCert, c_void_p)


	siServerCertBuffer = C_ST_tagBuffer()
	siServerCertBuffer.nLen = len(siServerCert)
	siServerCertBuffer.pbData = cast(siServerCert, c_void_p)

	sToken = C_ST_tagToken()
	sToken.exCert	=	exServerCertBuffer
	sToken.signCert 	= 	siServerCertBuffer

	libsff = cdll.LoadLibrary('libfasfl.so')
	if libsff.SFF_IsLabel(szPlainFile) <> 0 :
		return 1
	# 登陆
	ret = libsff.SFF_LoginMultip(szpServerpin, szSavePath,byref(sToken))
	if ret <> 0 :
		return ret;

	pSfl = c_void_p()

	# 打开标签
	ret = libsff.SFF_OpenSFL(byref(sToken), szPlainFile , byref(pSfl))
	if ret <> 0 :
		return ret


	pAttr = C_ST_tagPrivilegeAttr()

	exUserCert = base64.b64decode(exUserCertOfbase64)
	exUserCertBuffer = C_ST_tagBuffer()
	exUserCertBuffer.nLen = len(exUserCert)
	exUserCertBuffer.pbData = cast(exUserCert, c_void_p)

	pAttr.exCert = pointer(exUserCertBuffer)

	pAttr.bRead 		= 1		#读权限
	pAttr.uTotalRead 	= 0		#可读份数
	pAttr.uAlread 		= 0		#已读份数
	pAttr.bWrite 		= 1		#修改文件权限
	pAttr.bDel 			= 1		#删除权限
	pAttr.bPrint 		= 1		#打印权限
	pAttr.uPrintCount 	= 0		#可打印份数
	pAttr.uPrintedCount = 0		#已打印份数

	# 合并文件
	ret = libsff.SFF_ExternalToInternal(pSfl,szCryptFile,szCryptSflFile)
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret

	ret = libsff.SFF_CloseSFL(pSfl)
	if ret <> 0 :
		return ret

	# 打开内联文件
	ret = libsff.SFF_OpenSFL(byref(sToken), szCryptSflFile , byref(pSfl))
	if ret <> 0 :
		return ret
	# 添加权限
	ret = libsff.SFF_AddPrivilegeAttr(pSfl,byref(pAttr))
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
	 	return ret

	# 保存内联标签文件
	ret = libsff.SFF_SaveSFL(pSfl,szCryptSflFile)
	#ret = libsff.SFF_SaveSFL(pSfl,"/home/test_ee1.txt")
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret

	ret = libsff.SFF_CloseSFL(pSfl)
	if ret <> 0 :
		return ret

	return 0

#外联式标签(密文+纯标签)到新的内联式标签(无权限)
#exServerCertOfbase64 CER加密证书(base64编码) siServerCertOfbase64 CER签名证书(base64编码) szpServerpin 服务器保护证书密码
#szSavePath 发布路径 szPlainFile 标签文件路径 szCryptFile 密文实体文件路径 szCryptSflFile 内联式标签路径
#exUserCertOfbase64 添加的用户CER加密证书(base64编码)
def LabelFileWithoutAttr(exServerCertOfbase64,siServerCertOfbase64,szpServerpin,szSavePath,exUserCertOfbase64,szPlainFile,szCryptFile,szCryptSflFile):
	exServerCert = base64.b64decode(exServerCertOfbase64)
	siServerCert = base64.b64decode(siServerCertOfbase64)

	exServerCertBuffer = C_ST_tagBuffer()
	exServerCertBuffer.nLen = len(exServerCert)
	exServerCertBuffer.pbData = cast(exServerCert, c_void_p)


	siServerCertBuffer = C_ST_tagBuffer()
	siServerCertBuffer.nLen = len(siServerCert)
	siServerCertBuffer.pbData = cast(siServerCert, c_void_p)

	sToken = C_ST_tagToken()
	sToken.exCert	=	exServerCertBuffer
	sToken.signCert 	= 	siServerCertBuffer

	libsff = cdll.LoadLibrary('libfasfl.so')
	if libsff.SFF_IsLabel(szPlainFile) <> 0 :
		return 1
	# 登陆
	ret = libsff.SFF_LoginMultip(szpServerpin, szSavePath,byref(sToken))
	if ret <> 0 :
		return ret;

	pSfl = c_void_p()

	# 打开标签
	ret = libsff.SFF_OpenSFL(byref(sToken), szPlainFile , byref(pSfl))
	if ret <> 0 :
		return ret


	pAttr = C_ST_tagPrivilegeAttr()

	print "len =" , len(exUserCertOfbase64)
	exUserCert = base64.b64decode(exUserCertOfbase64)
	exUserCertBuffer = C_ST_tagBuffer()
	exUserCertBuffer.nLen = len(exUserCert)
	exUserCertBuffer.pbData = cast(exUserCert, c_void_p)

	pAttr.exCert = pointer(exUserCertBuffer)

	pAttr.bRead 		= 1		#读权限
	pAttr.uTotalRead 		= 0		#可读份数
	pAttr.uAlread 		= 0		#已读份数
	pAttr.bWrite 		= 1		#修改文件权限
	pAttr.bDel 			= 1		#删除权限
	pAttr.bPrint 		= 1		#打印权限
	pAttr.uPrintCount 	= 0		#可打印份数
	pAttr.uPrintedCount 	= 0		#已打印份数

	# 合并文件
	ret = libsff.SFF_ExternalToInternal(pSfl,szCryptFile,szCryptSflFile)
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret

	# 添加权限
	ret = libsff.SFF_AddPrivilegeAttr(pSfl,byref(pAttr))
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret

	ret = libsff.SFF_CloseSFL(pSfl)
	if ret <> 0 :
		return ret

	return 0

#外联式标签(密文+纯标签)到新的内联式标签
#exServerCertOfbase64 CER加密证书(base64编码) siServerCertOfbase64 CER签名证书(base64编码) szpServerpin 服务器保护证书密码
#szSavePath 发布路径 szPlainFile 标签文件路径 szCryptFile 密文实体文件路径 szCryptSflFile 内联式标签路径
#exUserCertOfbase64 添加的用户CER加密证书(base64编码)
def LabelFileWithAttr(exServerCertOfbase64,siServerCertOfbase64,szpServerpin,szSavePath,exUserCertOfbase64,szPlainFile,szCryptFile,szCryptSflFile):
	exServerCert = base64.b64decode(exServerCertOfbase64)
	siServerCert = base64.b64decode(siServerCertOfbase64)

	exServerCertBuffer = C_ST_tagBuffer()
	exServerCertBuffer.nLen = len(exServerCert)
	exServerCertBuffer.pbData = cast(exServerCert, c_void_p)


	siServerCertBuffer = C_ST_tagBuffer()
	siServerCertBuffer.nLen = len(siServerCert)
	siServerCertBuffer.pbData = cast(siServerCert, c_void_p)

	sToken = C_ST_tagToken()
	sToken.exCert	=	exServerCertBuffer
	sToken.signCert 	= 	siServerCertBuffer

	libsff = cdll.LoadLibrary('libfasfl.so')
	if libsff.SFF_IsLabel(szPlainFile) <> 0 :
		return 1
	# 登陆
	ret = libsff.SFF_LoginMultip(szpServerpin, szSavePath,byref(sToken))
	if ret <> 0 :
		return ret;

	pSfl = c_void_p()

	# 打开标签
	ret = libsff.SFF_OpenSFL(byref(sToken), szPlainFile , byref(pSfl))
	if ret <> 0 :
		return ret


	pAttr = C_ST_tagPrivilegeAttr()

	print "len =" , len(exUserCertOfbase64)
	exUserCert = base64.b64decode(exUserCertOfbase64)
	exUserCertBuffer = C_ST_tagBuffer()
	exUserCertBuffer.nLen = len(exUserCert)
	exUserCertBuffer.pbData = cast(exUserCert, c_void_p)

	pAttr.exCert = pointer(exUserCertBuffer)

	pAttr.bRead 		= 1		#读权限
	pAttr.uTotalRead 		= 0		#可读份数
	pAttr.uAlread 		= 0		#已读份数
	pAttr.bWrite 		= 1		#修改文件权限
	pAttr.bDel 			= 1		#删除权限
	pAttr.bPrint 		= 1		#打印权限
	pAttr.uPrintCount 	= 0		#可打印份数
	pAttr.uPrintedCount 	= 0		#已打印份数

	# 添加权限
	ret = libsff.SFF_AddPrivilegeAttr(pSfl,byref(pAttr))
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret

	# # 合并文件
	# ret = libsff.SFF_ExternalToInternal(pSfl,szCryptFile,szCryptSflFile)
	# if ret <> 0 :
	# 	return ret


	ret = libsff.SFF_CloseSFL(pSfl)
	if ret <> 0 :
		return ret

	return 0

#内联式标签解密
#exServerCertOfbase64 CER加密证书(base64编码) siServerCertOfbase64 CER签名证书(base64编码) szpServerpin 服务器保护证书密码 
#szSavePath 发布路径 szPlainFile 内联标签文件路径  szSflFile 明文路径
def DecryptFile(exServerCertOfbase64,siServerCertOfbase64,szpServerpin,szSavePath,szPlainFile,szSflFile):
	exServerCert = base64.b64decode(exServerCertOfbase64)
	siServerCert = base64.b64decode(siServerCertOfbase64)

	exServerCertBuffer = C_ST_tagBuffer()
	exServerCertBuffer.nLen = len(exServerCert)
	exServerCertBuffer.pbData = cast(exServerCert, c_void_p)

	
	siServerCertBuffer = C_ST_tagBuffer()
	siServerCertBuffer.nLen = len(siServerCert)
	siServerCertBuffer.pbData = cast(siServerCert, c_void_p)
	
	sToken = C_ST_tagToken()	
	sToken.exCert	=	exServerCertBuffer
	sToken.signCert 	= 	siServerCertBuffer
	
	libsff = cdll.LoadLibrary('libfasfl.so')

	if libsff.SFF_IsLabel(szPlainFile) <> 0 :
		print "SFF_IsLabel"
		print libsff.SFF_IsLabel(szPlainFile)
		return 1
	# 登陆
	ret = libsff.SFF_LoginMultip(szpServerpin, szSavePath,byref(sToken)) 
	if ret <> 0 :
		print "SFF_LoginMultip",szpServerpin,szSavePath
		return ret;

	pSfl = c_void_p()

	#打开标签
	ret = libsff.SFF_OpenSFL(byref(sToken), szPlainFile , byref(pSfl))
	if ret <> 0 :
		print "SFF_OpenSFL"
		print ret
		return ret


	#解密标签
	ret = libsff.SFF_InternalReadSF(pSfl,szSflFile)
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		print "SFF_InternalReadSF"
		return ret

	ret = libsff.SFF_CloseSFL(pSfl)
	if ret <> 0 :
		print "SFF_CloseSFL"
		return ret

	return 0

#内联式标签解密同时添加权限
#exServerCertOfbase64 CER加密证书(base64编码) siServerCertOfbase64 CER签名证书(base64编码) szpServerpin 服务器保护证书密码
#szSavePath 发布路径 szPlainFile 内联标签文件路径  szSflFile 明文路径
def DecryptFileWithAttr(exServerCertOfbase64,siServerCertOfbase64,exUserCertOfbase64,szpServerpin,szSavePath,szPlainFile,szSflFile):
	exServerCert = base64.b64decode(exServerCertOfbase64)
	siServerCert = base64.b64decode(siServerCertOfbase64)

	exServerCertBuffer = C_ST_tagBuffer()
	exServerCertBuffer.nLen = len(exServerCert)
	exServerCertBuffer.pbData = cast(exServerCert, c_void_p)


	siServerCertBuffer = C_ST_tagBuffer()
	siServerCertBuffer.nLen = len(siServerCert)
	siServerCertBuffer.pbData = cast(siServerCert, c_void_p)

	sToken = C_ST_tagToken()
	sToken.exCert	=	exServerCertBuffer
	sToken.signCert 	= 	siServerCertBuffer

	libsff = cdll.LoadLibrary('libfasfl.so')

	if libsff.SFF_IsLabel(szPlainFile) <> 0 :
		print "SFF_IsLabel"
		print libsff.SFF_IsLabel(szPlainFile)
		return 1
	# 登陆
	ret = libsff.SFF_LoginMultip(szpServerpin, szSavePath,byref(sToken))
	if ret <> 0 :
		print "SFF_LoginMultip",szpServerpin,szSavePath
		return ret;

	pSfl = c_void_p()

	#打开标签
	ret = libsff.SFF_OpenSFL(byref(sToken), szPlainFile , byref(pSfl))
	if ret <> 0 :
		print "SFF_OpenSFL"
		return ret

	#解密标签
	ret = libsff.SFF_InternalReadSF(pSfl,szSflFile)
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		print "SFF_InternalReadSF"
		return ret

	# ret = libsff.SFF_CloseSFL(pSfl)
	# if ret <> 0 :
	# 	print "SFF_CloseSFL"
	# 	return ret


	pAttr = C_ST_tagPrivilegeAttr()

	print "len =" , len(exUserCertOfbase64)
	exUserCert = base64.b64decode(exUserCertOfbase64)
	exUserCertBuffer = C_ST_tagBuffer()
	exUserCertBuffer.nLen = len(exUserCert)
	exUserCertBuffer.pbData = cast(exUserCert, c_void_p)

	pAttr.exCert = pointer(exUserCertBuffer)

	pAttr.bRead 		= 1		#读权限
	pAttr.uTotalRead 		= 0		#可读份数
	pAttr.uAlread 		= 0		#已读份数
	pAttr.bWrite 		= 1		#修改文件权限
	pAttr.bDel 			= 1		#删除权限
	pAttr.bPrint 		= 1		#打印权限
	pAttr.uPrintCount 	= 0		#可打印份数
	pAttr.uPrintedCount 	= 0		#已打印份数

	# 添加权限
	ret = libsff.SFF_AddPrivilegeAttr(pSfl,byref(pAttr))
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret

		# 保存标签文件
	ret = libsff.SFF_SaveSFL(pSfl,"/yidong/file/test/aaaaa.pdf")
	if ret <> 0 :
		libsff.SFF_CloseSFL(pSfl)
		return ret

	ret = libsff.SFF_CloseSFL(pSfl)
	if ret <> 0 :
		return ret
	return 0




























