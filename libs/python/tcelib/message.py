# -- coding:utf-8 --


#scott  shanghai china
#86-13916624477 qq:24509826 msn: socketref@hotmail.com
#

import socket,traceback,os,os.path,sys,time,struct,base64,gzip,array,json,zlib
from errbase import *

'''
------------------
msghdr
cmdtxt
\0\0
二进制流
-----------------
视频包由三部分构成: MetaMessage数据元封套,控制命令文本(json格式),二进制数据，后两者之间采用连续两个\0区分，表示开始二进制流数据
[metamsg,cmdtxt,bindata]
bindata部分格式、编码由cmdtxt控制

# [magic,size,compress,encrypt,version],[command text(json)],[\0\0],[binary data..]
'''

'''
	< 100 不压缩
'''

COMPRESS_NONE = 0	#压缩方式ß
COMPRESS_ZLIB = 1
COMPRESS_BZIP2 = 2

ENCRYPT_NONE = 0  #加密方式
ENCRYPT_MD5  = 1
ENCRYPT_DES  = 2
ENCRYPT_AES  = 3

MSGTYPE_RPC = 1
MSGTYPE_NORPC = 2

class NetMetaPacket:
	def __init__(self,msg=None ):
		self.msg = msg
		self.size4 = 0
		self.encrypt1 = ENCRYPT_NONE	#加密算法
		self.ver4 = 0x01000000 			# means 1.0.0.0

	magic4=0xEFD2BB99
	
	@classmethod
	def minSize(cls):
		return 14
		
	def marshall(self,compress=COMPRESS_ZLIB):
		d = self.msg.marshall()
		if compress != COMPRESS_NONE:
			if len(d)>100:
				if compress == COMPRESS_ZLIB:
					d = zlib.compress(d)
					compress = COMPRESS_ZLIB	# zlib default
			else:
				compress = COMPRESS_NONE
		r = struct.pack('!BBI',compress,self.encrypt1,self.ver4)
		r+= d
		self.size4 = len(r)+4
		r = struct.pack('!II', self.magic4,self.size4) + r
		return r


class NetPacketQueue:
	def __init__(self,conn = None,size= 1024):
		self.size = size
		self.outs={}
		self.ins={}
		self.user=None
		self.conn = conn
		self.bf=''
		self.pktlist=[] #解出来的消息
		self.invalid = False

	def clearPackets(self):
		self.pktlist=[]

	def destroy(self):
		self.invalid = True

	def getMessageList(self):
		pkts = self.pktlist
		self.pktlist=[]
		return pkts

	'''
		@return: false - 脏数据产生
	'''
	def dataQueueIn(self,d):


		rc = (True,2) # 2表示ok
		self.bf+=d
		d = self.bf
		while True:
			hdrsize = NetMetaPacket.minSize()
			if len(d)<NetMetaPacket.minSize():
				rc = True,0 #数据不够,等待
				break

			magic,size,compress,encrypt,ver = struct.unpack('!IIBBI',d[:hdrsize])
			if magic != NetMetaPacket.magic4:
				return False, NETMSG_ERROR_MAGIC#
			if size<=10:
				return False,NETMSG_ERROR_SIZE
			if len(d)< size+4:
				rc = True,1 #数据不够
				break
			size-=10

			s = d[hdrsize:hdrsize+size]
			d = d[hdrsize+size:]
			if compress == COMPRESS_ZLIB:
				try:
					s = zlib.decompress(s)
				except:
					return False,NETMSG_ERROR_DECOMPRESS
			elif compress != COMPRESS_NONE:
				return False,NETMSG_ERROR_NOTSUPPORTCOMPRESS
			self.pktlist.append(s)
		self.bf = d
		return rc


		
		
if __name__=='__main__':
	#print NetMetaPacket(msg=MsgCallReturn(value=range(10),bin='abc' ),compress=COMPRESS_NONE).marshall()
	#print NetMetaPacket.minSize()
	# m = MsgCallReturn()
	# m['name']='scott'
	# print m.attrs
	#
	pass