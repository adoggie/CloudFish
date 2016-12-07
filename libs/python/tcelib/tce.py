#--coding:utf-8--


'''
 2012.10.9
 1. 屏蔽connection 避免暴露给用户， sendMessage的同时建立网络连接

2014.6.21 scott
	1. RpcEndpoint 增加 compress ,默认为  ZLIB压缩
'''

import	sys

import os,sys,os.path,struct,time,traceback,string,zlib,threading
#from network import *
#from message import *

import message

import utils



from xml.dom.minidom import  parseString as xmlParseString
import loggin
import gevent
import gevent.queue
import gevent.pool

#from gevent import monkey
#monkey.patch_all()
#monkey.patch_socket()

from gevent.event import AsyncResult
import gevent.lock
import gevent.event



RPCERROR_SUCC = 0
RPCERROR_SENDFAILED = 1
RPCERROR_TIMEOUT  =2
RPCERROR_DATADIRTY = 3
RPCERROR_INTERFACE_NOTFOUND = 4 #adapter中无法定位到接口函数
RPCERROR_UNSERIALIZE_FAILED = 5 #解析rpc参数失败
RPCERROR_REMOTEMETHOD_EXCEPTION = 6 #rpc 远端服务函数调用异常

class RpcInternal:
	func_str = str
	func_type = type


class RpcConsts:
	RPCERROR_SUCC = 0
	RPCERROR_SENDFAILED =1
	RPCERROR_DATADIRTY= 3
	RPCERROR_TIMEOUT = 2
	RPCERROR_INTERFACE_NOTFOUND = 4
	RPCERROR_UNSERIALIZE_FAILED = 5
	RPCERROR_REMOTEMETHOD_EXCEPTION = 6
	RPCERROR_DATA_INSUFFICIENT = 7
	RPCERROR_REMOTE_EXCEPTION = 8

	RPCERROR_CONNECT_UNREACHABLE = 101
	RPCERROR_CONNECT_FAILED  = 102
	RPCERROR_CONNECT_REJECT = 103
	RPCERROR_CONNECTION_LOST = 104

	COMPRESS_NONE = 0
	COMPRESS_ZLIB = 1
	COMPRESS_BZIP2 = 2

	ENCRYPT_NONE = 0
	ENCRYPT_MD5  = 1
	ENCRYPT_DES  = 2

	MSGTYPE_RPC = 1
	MSGTYPE_NORPC = 2

	error_infos={
		RPCERROR_SUCC:"RPCERROR_SUCC",
		RPCERROR_SENDFAILED:"RPCERROR_SENDFAILED",
		RPCERROR_DATADIRTY:"RPCERROR_DATADIRTY",
		RPCERROR_TIMEOUT :"RPCERROR_TIMEOUT",
		RPCERROR_INTERFACE_NOTFOUND:"RPCERROR_INTERFACE_NOTFOUND",
		RPCERROR_UNSERIALIZE_FAILED:"RPCERROR_UNSERIALIZE_FAILED",
		RPCERROR_REMOTEMETHOD_EXCEPTION:"RPCERROR_REMOTEMETHOD_EXCEPTION",
		RPCERROR_DATA_INSUFFICIENT:"RPCERROR_DATA_INSUFFICIENT",
		RPCERROR_REMOTE_EXCEPTION:"RPCERROR_REMOTE_EXCEPTION",

		RPCERROR_CONNECT_UNREACHABLE:"RPCERROR_CONNECT_UNREACHABLE",
		RPCERROR_CONNECT_FAILED:"RPCERROR_CONNECT_FAILED",
		RPCERROR_CONNECT_REJECT:"RPCERROR_CONNECT_REJECT",
		RPCERROR_CONNECTION_LOST:"RPCERROR_CONNECTION_LOST"
	}


LOG_DEBUG = 1
LOG_WARN = 2
LOG_INFO = 3
LOG_ERROR = 4

def log_print(m,what):
	print m
	logger= Communicator.instance().getLogger()
	if not logger:  return
	if what == LOG_DEBUG:
		logger.debug(m)

def log_debug(m):
	log_print(m,LOG_DEBUG)

def log_warn(m):
	log_print(m,LOG_WARN)


def log_info(m):
	log_print(m,LOG_INFO)

def log_error(m):
	log_print(m,LOG_ERROR)


# class RpcLogger:
# 	def __init__(self):
# 		pass

class RpcContext:
	def __init__(self):
		self.conn = None	#RpcConnection
#		self.sequence = 0 #一次调用产生的事务编号，调用和返回匹配的编号
		self.msg = None #调用消息 RpcMessageCall

#class CallReturn:
#	def __init__(self,p):
#		pass


class RpcException(Exception):
	def __init__(self,errcode,errmsg='',data=None):
		self.errcode = errcode
		self.errmsg = errmsg
		self.subcode = 0
		self.d = data

	def what(self):
		msg = self.errmsg
		if not msg:
			msg = RpcConsts.error_infos.get(self.errcode,"Undefined Error")
		return msg

	def __str__(self):
		return self.what()


#class RpcExceptionTimeOut(Exception):
#	def __init__(self):
#		pass
#
#class RpcExceptionConnectionLost(Exception):
#	def __init__(self):
#		pass



'''

magic|size|msgtype|seq|calltype|interface_idx|operate_idx|error_code|data

==========
magic -   'eeff'
size -	  数据包长度(包含magic)
compress - 压缩方式 0 - 不压缩  ; 1 - zlib ; 2 - bzip
encrypt - 加密方式
ver - 消息版本

msgtype (1) - 1 : RPC
		  2 ~ 用户定义信息
seq - (4)  调用事务序号
calltype (1) - 0x01 ： call 调用方法
	       0x02 ： return 返回参数
	       0x10 ： twoway 调用方法
	       0x20 ： onway 单向调用
interface_idx (2) - 接口索引编号  (0 - 返回值类型)
operate_idx (2) - 接口函数索引编号 (0 - 返回值类型)
param_size (1)  -  参数个数
data - 参数值内容

'''


#from message import MessageBase
#import message


AF_READ = 0x01
AF_WRITE = 0x02

# class RpcMQAttribute:
# 	def __init__(self):
# 		self.src_id =0
# 		self.src_type= 0
# 		self.user_id = 0
# 	#
#
# class IEndpointImpl:
# 	def __init__(self):
# 		self.conn = None # connection object
#
# 	def open(self,ep,af):pass
# 	def close(self): pass
# 	def sendMessage(self,msg):pass

class RpcEndPoint:
	'''
		不同通信端点实现的包装类
	'''
	#ep types
	SOCKET = 0
	MQ = 1
	EASYMQ= 2
	QPIDMQ= 3
	USER = 4
	AUTO = 5
	WEBSOCKET = 6

	#access flags

	@staticmethod
	def fromAddress(address):
		'''
			tcp://host:port
			ssl://host:port/s?keyfile=server.key&certfile=server.crt
		'''
		import urlparse
		cps = urlparse.urlparse(address)




	def __init__(self,id=0,name='',host='',port='',addr='',impl=None,keyfile='',certfile='',
		compress=message.COMPRESS_ZLIB,ssl=False,type='socket'):
		self.id = id
		self.name = name
		self.host = host
		self.port = port
		self.addr = addr
		self.user = ''
		self.passwd=''
		self.impl = impl    #具体通信方式不同实现
		self.type = type # in (mq,socket,websocket)
		self.keyfile = keyfile
		self.certfile = certfile
		self.compress = compress
		self.ssl = ssl 	#是否启用ssl


	def open(self,af):
		# from rpc_svc import RpcConnectionQpidMQ
		# from rpc_svc import RpcConnectionEasyMQ
		# from rpc_svc import RpcConnectionSocket
		# from rpc_svc import RpcConnectionWebSocket

		if self.type in ('mq','easymq'):       # mesage queue , as qpid
			from conn_easymq import RpcConnectionEasyMQ
			self.impl = RpcConnectionEasyMQ(self)
		elif self.type == 'qpid':
			from conn_qpid import RpcConnectionQpidMQ
			self.impl = RpcConnectionQpidMQ(self)
		elif self.type == 'socket':
			from conn_socket import RpcConnectionSocket
			self.impl = RpcConnectionSocket(ep=self)
		elif self.type =='websocket':
			from conn_websocket import RpcConnectionWebSocket
			self.impl = RpcConnectionWebSocket(ep=self)
		else:
			log_error('just support MQ type! error ep:%s %s %s'%(self.name,self.addr,self.type))
			return False
#		print str(self)
		#socket/websocket时，此刻的connection其实是个伪连接，只是保存endpoint之用，真实的操作在socketAdapter的start()
		#如果是消息队列连接，则即刻打开读/写连接
		if self.type in ('mq','easymq','qpid'):
			return self.impl.open(af=af)
		return True


	def __str__(self):
		return 'ep: id=%s,name=%s,host=%s,port=%s,addr=%s,type=%s'%(self.id,self.name,self.host,self.port,self.addr,
		                                                            self.type)
	def close(self):
		return self.impl.close()
		pass

	def sendMessage(self,m):
#		print 'sendMessage impl:',self.impl
		if not self.impl:
			print 'no impl dispatch!'
			print str(self)
			return
		return self.impl.sendMessage(m)

	def getUnique(self):
		return self.name.strip()

	def __getUnique(self):
		import base64,hashlib
		uid = '%s:%s %s'%(self.host,self.port,self.addr)
		m = hashlib.md5()
		m.update(uid.encode('utf-8'))
		uid = base64.encodestring(m.digest()).strip()
		return uid

######## end Endpoint implementations #######################################

class RpcRouteInoutPair:
	def __init__(self):
		self.in_ = None # ep
		self.out = None

class RpcIfRouteDetail:
	CALL = 0
	RETURN = 1
	def __init__(self):
		self.ifx = 0
		self.calls = {} # {EP_IDX_in:ep}
		self.returns={} # {EP_IDX_in:ep}

	def getRouteInoutPair(self,route,epid):
		# route: 0 - call ; 1 - return
		r = self.calls
		if route == RpcIfRouteDetail.RETURN:
			r = self.returns
		return r.get(epid)



class InterfaceDef:
	def __init__(self):
		self.id = 0
		self.name=''

class ServiceDef:
	def __init__(self):
		self.name =''
		self.id = 0
		self.pattern=''
		self.ifs={} #{IF_IDX:if}


class LocalServer:
	def __init__(self,id='',name=''):
		self.id = id
		self.name = name
		self.service = None # ServiceDef
		self.routes = {}    #{IFIDX:{call:{in,out},return:{in,out}}}
		self.ep_reads={}    #{name:ep,...}
		self.ep_writes={}   #{name:ep,...}
		self.name_eps={}    #{name:ep,...}
		self.props={}

	def isLocalInterface(self,ifid):
		'''
			判别ifid是否是本地服务器接口
		'''
		if self.service:
			return ifid in self.service.ifs.keys()
		return False

	def getPropertyValue(self,name,val=None):
		return self.props.get(name,val)

	def findRoutePair(self,ifidx,epidx,af=AF_READ):
		pass

	def findEndPointByName(self,name):
		ep = self.name_eps.get(name)
#		print ep
		return ep

	def getId(self):
		return 0        # 服务器已不具备整型编号表示服务器标示
		#return self.id
		# if self.service:
		# 	return ( (self.service.id<<8)&0xffff) | (self.id&0xff)
		# return 0

	def getName(self):
		return self.name

	def getServiceId(self):
		if self.service:
			return self.service.id
		return 0


def getUniqueSequence():
	return RpcCommunicator.instance().generateSeq()
	# return 0

class RpcExtraData:
	NODATA = 0  	# 0 表示没有附加数据，每种数据都可以自己标识自己
	BYTE_STREAM = 1 #字节流
	STRING=2
	STRING_DICT= 3
	STRING_LIST = 4

	def __init__(self):
#		self.type = RpcExtraData.NODATA
#		self.d = ''
		self.props={}

	def setStrDict(self,d):
		self.props = d

	def getStrDict(self):
		return self.props

	def setPropertyValue(self,name,value):
		self.props[name] = value

	def getValue(self,name,dft=None):
		return self.props.get(name,dft)

#	def getStrList(self):
#		return None
#
#	def getString(self):
#		return None
#
#	def getBytes(self):
#		return self.d


	def marshall(self):
#		size = (self.type<<24)| (len(self.d)&0xffffff)
#		return struct.pack('!I',size) + self.d
		d = ''
		# print repr(self.props)

		if not self.props :
			self.props ={}
		d = struct.pack('!I',len(self.props))
		for k,v in self.props.items():
			d+=struct.pack('!I',len(k)) + k.encode('utf-8')	# 2014.7.2 scott
			d+=struct.pack('!I',len(v)) + v.encode('utf-8')
		return d


	def size(self):
		return self.datasize()+4

	def datasize(self):
		size = 0
		for k,v in self.props.items():
			size += len(k)+len(v)+8
		return size

	def unmarshall(self,stream):
#		size, = struct.unpack('!I',stream[:4])
#		self.type,size = (size>>24)&0xff,size&0xffffff
#		self.d = stream[4:size+4]
		p=0

		size, = struct.unpack('!I',stream[p:p+4])
		p+=4
		for n in range(size):
			size, = struct.unpack('!I',stream[p:p+4])
			p+=4
			key = stream[p:p+size]
			p+=size
			size, = struct.unpack('!I',stream[p:p+4])
			p+=4
			val = stream[p:p+size]
			p+=size
			self.props[key] = val



class RpcMessage:

	CALL = 0x01
	RETURN = 0x02
	TWOWAY = 0x10
	ONEWAY = 0x20
	ASYNC = 0x40

	DEFAULT_CALL = CALL | TWOWAY	#默认调用等待方式

	def __init__(self):
#		self.params=[]

		self.type =  message.MSGTYPE_RPC #
		self.sequence = 0
		self.calltype = RpcMessage.DEFAULT_CALL
		self.ifidx = 0 	#接口类编号
		self.opidx = 0 	#函数编号
		self.errcode = RPCERROR_SUCC # RETURN 包 会使用到错误码
		self.paramsize = 0  # byte 宽度
		self.call_id = 0  # 调用者编号   第15位 0 - 本地发起RPC， 1 - 转向的RPC；第14-8位 服务类型编号 ; 第7-0 服务id编号
		self.extra = RpcExtraData()   #额外数据
		#--以下成员用于接收解析临时存储

		self.paramstream = ''
		self.mtx = AsyncResult() #utils.MutexObject()
		self.prx = None
		self.async = None #异步通知函数 异步调用时使用
		self.asyncparser = None #异步返回值解析出参数对象传递到 async
		self.conn = None  # which RpcConnection object

#		self.attr = None # mq'attr
		self.callmsg = None
		self.user_id = 0
		self.cookie = None # 异步调用本地传递到回调函数的用户变量  2013.11.30

		# self.async( self.asyncparser( streamdata) )

	def __str__(self):
		return 'type:%s,sequence:%s,calltype:%s,ifidx:%s,opidx:%s,errcode:%s'%(self.type,self.sequence,
		self.calltype,self.ifidx,self.opidx,self.errcode)

#	#添加参数数据进去
#	def addParam(self,p):
#		self.params.append(p)

	# 打包Rpc消息包，讲序列化的参数打包成自己流
	def marshall(self):
		d =''
		if True:
		#try:
			#self.call_id = 0
			#print self.call_id,type(self.call_id)
#			self.paramsize = len(self.params)
			d = struct.pack('!BIBHHIBH',self.type,
							self.sequence,
							self.calltype,
							self.ifidx,
							self.opidx,
							self.errcode,	# 2012.9.9 错误码
							self.paramsize,
							self.call_id
							)
#			props = self.extra.getStrDict()
#			props['__user_id__'] = str(self.user_id)
#			self.extra.setStrDict(props)
			d+= self.extra.marshall()
			d+=self.paramstream

		#except:
		#	log_error(traceback.format_exc())
		#	d= ''
		#	raise 1

		return d

	@classmethod
	def unmarshall(cls,d):
		m = None
		try:
			idx = 0
			m = RpcMessage()
			m.type, = struct.unpack('B',d[idx:idx+1])
			idx+=1
			m.sequence, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			m.calltype, = struct.unpack('B',d[idx:idx+1])
			idx+=1
			m.ifidx, = struct.unpack('!H',d[idx:idx+2])
			idx+=2
			m.opidx, = struct.unpack('!H',d[idx:idx+2])
			idx+=2
			m.errcode, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			m.paramsize, = struct.unpack('B',d[idx:idx+1])
			idx+=1
			m.call_id, = struct.unpack('!H',d[idx:idx+2])
			idx+=2
			m.extra.unmarshall(d[idx:])
			idx+=m.extra.size()
			m.paramstream = d[idx:]
			m.user_id = int( m.extra.getValue("__user_id__","0"))
#			print m.extra.props,repr(m.paramstream)
		except :
			log_error(traceback.format_exc())
			m = None
		return m

#调用消息
class RpcMessageCall(RpcMessage):
	def __init__(self):
		RpcMessage.__init__(self)
		self.sequence = getUniqueSequence()
		self.calltype = RpcMessage.CALL

#返回消息包
class RpcMessageReturn(RpcMessage):
	def __init__(self):
		RpcMessage.__init__(self)
		self.calltype = RpcMessage.RETURN



class RpcConnection:
	MQ = 1
	SOCKET = 2
	def __init__(self,adapter=None,ep=None):

		self.ep = ep # RpcEndpoint
		self.conn = None
		self.delta = None
		self.rpcmsglist={}
		self.mtxrpc = threading.Lock() #连接断开，必须让通知等待rpc调用返回的对象
		self.id = str(time.time())

		self.adapter = adapter
		# self.pdest = pdest #目标地址
		# self.ep_id = 0

		self.budyconn = None #伙伴连接，读连接对应写连接
				#socket时budyconn就是自己
		self.userid = 0
		self.cb_disconnect = None
		self.id = 0

		self.recvpkg_num = 0  # 已接受报文数量
		self.token = ''
		self.appuser = None

		# if adapter:
		# 	self.adapters = [adapter]

	def getAddress(self):
		# return 'RpcConnection:'+str(id(self))
		import socket
		return 'RpcConnectionSocket:'+str( self.sock.getpeername())

	def setToken(self,token):
		self.token = token

	def getRecvedMessageCount(self):
		return self.recvpkg_num

	#将一个服务适配器绑定到一个连接上
	#之后连接上接收到的rpc消息被传递到adapter处理
	#通常应用在 client发起连接之后，server利用此连接反向调用client的服务类
	def attachAdapter(self,adapter):
		self.adapter =  adapter

	setAdatper = attachAdapter

	def detachAdapter(self):
		if self.adapter:
			self.adapter.removeConnection(self)
			self.adapter = None

	def setUserId(self,userid):
		if self.adapter:
			self.adapter.mapConnectionWithUserId(self,userid)
		self.userid = userid

	def getUserId(self):
		return self.userid

	def connect(self):
		return False


	def doReturnMsg(self,m2):
#		print 'doReturnMsg',m2,m2.sequence,repr(m2)
		m1 = RpcCommunicator.instance().dequeueMsg(m2.sequence)
		if m1:
			if m1.async:                #异步通知
				m1.asyncparser(m1, m2)   #m2.paramstream,m2.async,m2.prx)
			else:
#				m1.mtx.notify(m2)       # 传递到等待返回结果的对象线程
				m1.mtx.set(m2)


	def dispatchMsg(self,m):
		server = RpcCommunicator.instance().currentServer()
		if m.calltype & RpcMessage.CALL:

			#rpc调用请求
			if self.adapter:
				# print 'containedIf:',self.adapter.containedIf(m.ifidx)
				if self.adapter.containedIf(m.ifidx):
					# print 'adapter.dispatchMsg',m
					self.adapter.dispatchMsg(m)
					return
			# redirect to next

			#用户未认证，不能转发到下级节点
			route = server.routes.get(m.ifidx)  #查找接口路由信息
			if route:
				if self.ep.type in ('socket','websocket'): # 内向外的rpc请求
					#-- 鉴别用户是否已经通过认证  userid=0 非法用户编号
					server = RpcCommunicator.instance().currentServer()
					if server.getPropertyValue('userid_check','false') == 'true': #判别舒服需要用户检查
						if not self.userid: #用户id为0，未认证连接，取消转发
							print 'userid checked (is null),unauthorized skip redirect..'
							return
				if self.userid:
					m.extra.props['__user_id__'] = str(self.userid)
				#开始查找路由表，定位
				inout = route.getRouteInoutPair(RpcIfRouteDetail.CALL,self.ep.id)
				if inout:   #路由输出ep
					peer_ep = inout.out
					# if peer_ep.type !='mq':
					# 	log_error('out-ep must be mq-type ,please check config of server: %s '%server.name)
					# 	return
					m.call_id |= 1<<15  #最高位1表示此消息包是转发消息包
					#print 'redirect CALL msg,call_id',hex(m.call_id)
					peer_ep.sendMessage(m)
					#系统开始，用于已经将rpc调用回路设置好了 EasyMqConnection.setLoopbackMq()

		if m.calltype & RpcMessage.RETURN:
			#print 'call_id:',hex(m.call_id),m.extra.props
			#最高位为0表示此RETURN为本地调用产生的RETURN
			#routes表项记录为空，表示非转发服务，直接本地处理
			if not m.call_id>>15 or not server.routes:
				self.doReturnMsg(m)
				return
			#分派到其他ep
			# type_,id = (m.call_id>>8)&0x7f, m.call_id&0xff
			route = server.routes.get(m.ifidx)
			#print 'RETURN:',route
			if route:
				inout = route.getRouteInoutPair(RpcIfRouteDetail.RETURN,self.ep.id)
				if inout:   #路由输出ep
					peer_ep = inout.out
					print 'redirect RETURN ..'
					peer_ep.sendMessage(m)


	def close(self):
		return self

	def sendMessage(self,m):
		if m.calltype&RpcMessage.CALL:
			# if not m.extra.props.get('__user_id__'):
			# 	m.extra.props['__user_id__'] = str(m.user_id)

			#2013.11.25 following line commented
#			m.call_id |= RpcCommunicator.instance().currentServer().getId()

			if m.calltype& RpcMessage.ONEWAY == 0:
				RpcCommunicator.instance().enqueueMsg(m) #置入等待队列
		r = False
		r = self.sendDetail(m)
		if not r:
			if m.calltype&RpcMessage.CALL: #发送失败，删除等待队列中的消息
				if m.calltype& RpcMessage.ONEWAY == 0:
					RpcCommunicator.instance().dequeueMsg(m.sequence)
		return r

	def sendDetail(self,m):
		return False

	def getCompressionType(self):
		'''
			获取数据压缩方式
			默认: zlib
		'''
		ep = None
		if self.adapter:
			ep = self.adapter.getEndpoint()
		else:
			ep = self.ep
		compress = message.COMPRESS_ZLIB
		if ep:
			compress = ep.compress
		return compress



class RpcCommAdapter:
	def __init__(self,id,ep=None): # uri =  192.168.14.1:12000
#		if type(uri) == type(''):
#			self.endpoint = utils.parseNetAddr(uri)
		# self.endpoint = uri
		self.ep = ep
		self.servants = {}  # idx:servant
		self.id = id

		self.conns =[]
		# self.id_conns={}    #用户id绑定链接   2013.5.10
		self.user_conns={}
		# self.mtxconns = gevent.coros.Semaphore()  #threading.Lock()
		self.logger = None
#		self.stopmtx = gevent.event.Event() #此对象的wait调用必须之前有thread与行中，否则wait将失败，所以mq的
		# pygwa 一启动socket的adapter，因该使用gevent的event，以便进入消息循环
		self.stopmtx = threading.Event() #此对象的wait调用必须之前有thread与行中，否则wait将失败，所以mq的
		self.sequence = 0

	def getUserConnection(self,userid):
		return self.user_conns.get(userid)

	def getEndpoint(self):
		return self.ep

	def getUserConnection(self,userid):
		return self.user_conns.get(userid)

	def getMutex(self):
		return self.stopmtx

	def makeUniqueId(self):
		return str(time.time())

	def generateSeq(self):
		self.sequence+=1
		if self.sequence >0xffffff00:
			self.sequence = 1
		return self.sequence

	def start(self):
		return True

	def stop(self):
		self.getMutex().set()

	def join(self):
		self.getMutex().wait()
#		self.stopmtx.wait() #驱动时间模型

	#目前不支持单用户id在多conn上登陆传输
	def mapConnectionWithUserId(self,conn,userid):
		# self.mtxconns.acquire()
		self.user_conns[userid] = conn
		# self.mtxconns.release()

	def addConnection(self,conn):
		conn.setAdatper(self)
		# self.mtxconns.acquire()
		self.conns.append(conn)
		# self.mtxconns.release()

	def removeConnection(self,conn):
		# self.mtxconns.acquire()
		if self.conns.count(conn):
			self.conns.remove(conn)

		c = self.user_conns.get(conn.userid)
		#if self.user_conns.has_key(conn.userid):
		if c == conn:
			del self.user_conns[conn.userid]
		# self.mtxconns.release()

	def addServant(self,servant):
#		clsdelegate = servant.delegatecls
#		dg = clsdelegate(servant,self)
#		dg.id = self.makeUniqueId()
#		self.servants[ dg.index] = dg #保存委托对象
#		return dg.id

		for ifidx,dgcls in servant.delegatecls.items():
			dg = dgcls(servant,self)
			dg.id = self.makeUniqueId()
			self.servants[ dg.index ] = dg


	def containedIf(self,ifidx):
#		print self.servants
		return self.servants.has_key(ifidx)

	def dispatchMsg(self,m):
		#print 'Adapter Got Msg..',str(m)
		if m.calltype & RpcMessage.CALL:
			if not self.servants.has_key(m.ifidx): #不存在调用接口类
				self._doError(RPCERROR_INTERFACE_NOTFOUND,m)
				return
			dg = self.servants[m.ifidx]
			if not dg.optlist.has_key(m.opidx): #不存在接口函数
				self._doError(RPCERROR_INTERFACE_NOTFOUND,m)
				return
			func = dg.optlist[m.opidx]

			ctx = RpcContext()
#			if not conn.delta:
#				conn.delta = RpcConnection(conn)
			ctx.conn = m.conn  # it's RpcConnection
			ctx.msg = m
			try:
				func( ctx ) #讲消息传递到 servant对象的函数 (通过elegate间接传递)
			except:
				traceback.print_exc()
				self._doError(RPCERROR_REMOTEMETHOD_EXCEPTION,m)

#		if  m.calltype & RpcMessage.RETURN: # 在同一个连接上实现 rpc 复用
#			rpc = conn.delta
#			rpc.doReturnMsg(m)

	def _doError(self,errcode,m):
		errmsg = RpcMessageReturn()
		errmsg.sequence = m.sequence
		errmsg.errcode = errcode
		m.conn.sendMessage(errmsg)

	def sendMessage(self,m):
		conn = self.user_conns.get(m.user_id)    #找到连接对象
		print self.user_conns
		if conn:
			conn.sendMessage(m)

class RpcConnectionEventListener:
	def __init__(self):
		pass

	def onConnected(self,conn):
		pass

	def onDisconnected(self,conn):
		pass

	def onDataPacket(self,conn,msg):
		'''
			返回True进入事件分派，False则丢弃消息
		'''
		return True

#通信器
class RpcCommunicator:
	def __init__(self):
		self.adapters={}
		self.ep_adapters={}

		self.mtxadapter = threading.Lock()
		self.threads=[]
		self.condmsg = threading.Condition()
		self.msglist=[]
		self.running = False
		self.localServerId = 0 #本地服务编号

		self.msg_q={}
		self.mtxmsg_q = threading.Lock()
		self.logger = None

		self.sequence=0
		self.props={
			'rpc_call_timeout':30,  #RPC 调用默认等待超时时间
		}
		self.server = LocalServer()
		self.mtx = threading.Lock()
		self.disp_queue = gevent.queue.Queue()
		self.pool = None
		self.__inited = False     #标示是否已经初始化
		self.conneventlistener = None

	def setConnectionEventListener(self,evtlistener):
		self.conneventlistener = evtlistener

	def getConnectionEventListener(self):
		return self.conneventlistener

	def sleep(self,secs):
		gevent.sleep(secs)

	def getRpcCallTimeout(self):
		return self.props['rpc_call_timeout']

	def setRpcCallTimeout(self,wait):
		self.props['rpc_call_timeout'] = wait

	def getProperties(self):
		return self.props

	def setProperty(self,name,value):
		self.props[name] = value
		return self

	def generateSeq(self):
		self.mtx.acquire()
		self.sequence+=1
		if self.sequence >0xffffff00:
			self.sequence = 1
		self.mtx.release()
		return self.sequence

	def getLogger(self):
		return self.logger

#	def addAdapter(self,adapter):
#		# 启动adapter ，开始处于服务状态
#		return None

	#
	# def init(self,threadnum=1):
	#
	# 		#print 'thread.start()'
	# 	return self

	def enqueueMsg(self,m):
		self.mtxmsg_q.acquire()
		self.msg_q[m.sequence] = m
		self.mtxmsg_q.release()

	def dequeueMsg(self,sequence):
		m = None
		self.mtxmsg_q.acquire()
		m = self.msg_q.get(sequence)
		if m:
			del self.msg_q[sequence]
		self.mtxmsg_q.release()
		return m


	def createAdapter(self,id,ep):
		'''
			mq: 找出ep对象，创建adapter，并将ep关联到adapter
			socket:
			ep (RpcEndPoint/str)

		'''
		# from rpc_svc import RpcAdapterMQ
		# from rpc_svc import RpcAdapterSocket
		# from rpc_svc import RpcAdapterWebSocket

		adapter = None
		self.mtxadapter.acquire()
		adapter = self.adapters.get(id)
		if adapter:
			log_error('adapter id <%s> is existed! '%id)
			self.mtxadapter.release()
			return adapter
		self.mtxadapter.release()

		if isinstance(ep,str):
			ep = self.currentServer().findEndPointByName(ep)

		if not ep:
			return None

		if ep.type == 'socket' or ep.type == RpcEndPoint.SOCKET:
			from conn_socket import RpcAdapterSocket
			adapter = RpcAdapterSocket(id,ep)
		elif ep.type == 'websocket' or  ep.type == RpcEndPoint.WEBSOCKET:
			from conn_websocket import RpcAdapterWebSocket
			adapter = RpcAdapterWebSocket(id,ep)
		elif ep.type in ('mq','easymq','qpidmq','qpid',RpcEndPoint.EASYMQ,RpcEndPoint.MQ,RpcEndPoint.QPIDMQ):
			from conn_mq import RpcAdapterMQ
			adapter = RpcAdapterMQ(id,ep)


		# ep = self.currentServer().findEndPointByName(uri)
		# if not ep:
		# 	return None
		#
		# if ep.type == 'mq':
		# 	adapter = RpcAdapterMQ(id,ep)
		# if ep.type == 'socket':
		# 	adapter = RpcAdapterSocket(id,ep)
		#
		# if ep.type =='websocket':
		# 	adapter = RpcAdapterWebSocket(id,ep)

		if adapter:
			self.mtxadapter.acquire()
			self.adapters[id] = adapter
			self.ep_adapters[ep.name] = adapter
			self.mtxadapter.release()
			adapter.start()
		return adapter

	def addAdapter(self,adapter):
		self.mtxadapter.acquire()
		self.adapters[adapter.id] = adapter
		self.mtxadapter.release()

	def findAdatperByEpIdx(self,epidx):
		self.mtxadapter.acquire()
		adapter = self.ep_adapters.get(epidx)
		self.mtxadapter.release()

	def getConnectionForProxy(self,name):
		ep = self.currentServer().findEndPointByName(name)
		if ep:
			return  ep.impl
		return None

	def dispatchMsg(self,m):
		# self.condmsg.acquire()
		# self.msglist.append(m)
		# self.condmsg.notify()
		# self.condmsg.release()
		# print 'dispatchMsg,data is:',m
		self.disp_queue.put(m)

	def _task_queue(self):
		# print '_task_queue entering..'
		self.running = True
		while self.running:
			m = self.disp_queue.get()
			# print '---pick msg to be executing..'
			try:
				m.conn.dispatchMsg(m)
			except:
				traceback.print_exc()
		print '_task_queue exiting...'
	# def run(self,threadnum = 10):
	#
	# 	self.running = True
	# 	for n in range(threadnum):
	# 		thread = threading.Thread(target=self.work_thread)
	# 		self.threads.append(thread)
	# 		thread.start()
	#
	# 	for adapter in self.adapters.values():
	# 		if not adapter.start():
	# 			return False
	# 	log_info('service started,waiting for shudown..')
	# 	for t in self.threads:
	# 		print t.join()
	# 	log_info('system exiting..')


	def shutdown(self):
		for adapter in self.adapters.values():
			adapter.stop()

		self.running = False


	_handle = None
	@classmethod
	def instance(cls):
		if not cls._handle:
			cls._handle = cls()
		return cls._handle

	def getServiceDetail(self,type_):
		svc = self.id_svcs.get(type_,None)
		return svc

	def currentServer(self):
		return self.server

	#server_id - 指定服务其名称 gwa1
	#初始化指定名称的服务器
	def init(self,server_id='localhost',poolsize=5):
		'''
			server_id - server name
			file - services.xml
		'''
		if self.__inited:
			return self
		# self.builtin_type = type
		# self.builtin_int = int

		self.__inited = True
		self.server = None
		self.id_svcs={} #系统服务
		self.logger = loggin.Logger(server_id)
		self.logger.addHandler(loggin.stdout())
		self.server = LocalServer(name=server_id)
		self.pool = gevent.pool.Pool(poolsize)
		for n in range(poolsize):
			self.pool.spawn(self._task_queue)
		return self

	def __variantReplace(self,value,variants):
		for k,v in variants.items():
			pattern = '{%s}'%k
			value = value.replace(pattern,v)
		return value

	#打开消息路由功能,将读取服务配置文件,Communicator初始化之后可以调用
	def initMessageRoute(self,xmlfile=''):
		if not xmlfile:
			return False
		f = open(xmlfile)
		d = f.read()
		f.close()
		doc = xmlParseString(d)
		r = doc.documentElement

		#- 检索服务配置信息
		servername = self.server.getName()

		e = r.getElementsByTagName('InterfaceDef')
		if not e:
			log_error('Tag:InterfaceDef not defined!')
			return False
		ifs = e[0].getElementsByTagName('if')

		#接口类型定义
		ifxdefs={} #{name:ifx}
		for e in ifs:
			ifx = InterfaceDef()
			ifx.name = e.getAttribute('name')
			ifx.id = int(e.getAttribute('id'))
			ifxdefs[ifx.name] = ifx

		#--- VariantDefs ---

		variants={}
		e =  r.getElementsByTagName('VariantDef')[0]
		if e:
			e2 = e.getElementsByTagName('var')
			for e3 in e2:
				name = e3.getAttribute('name')
				value = e3.getAttribute('value')
				variants[name] = value

		#--- End VariantDefs ---

		'''
		e =  r.getElementsByTagName('ServiceDef')[0]
		if not e:
			log_error('Tag:ServiceDef not defined!')
			return False


		#服务类型定义
		svcdefs ={} #{name:svc}

		e2 = e.getElementsByTagName('service')
		for e in e2:
			svc = ServiceDef()
			svc.name = e.getAttribute('name')
			svc.id = int(e.getAttribute('id'))
			svc.pattern = e.getAttribute('mq_pattern')
			e3 = e.getElementsByTagName('interfaces')[0].getElementsByTagName('if')
			for e in e3:
				name =  e.getAttribute('name')
				ifx = ifxdefs.get(name)
				if not ifx:
					print 'if <%s> not defined!'%name
					return False
				svc.ifs[ifx.id] = ifx
			svcdefs[svc.name] = svc
			self.id_svcs[svc.id] = svc
		'''
		# endpoints
		epdefs = {} #{EP_IDX:ep}

		e = r.getElementsByTagName('EndPoints')
		if not e:
			log_error('Tag: EndPoints not found!')
			return False
		e2 = e[0].getElementsByTagName('ep')
		epidx = 1
		for e in e2:
			ep = RpcEndPoint()          # 通信端点类
			ep.id = epidx
			ep.name = e.getAttribute('name')
			ep.type = e.getAttribute('type')

			#-- 变量替换  <VariantDef><var/></VariantDef>
			ep.host = e.getAttribute('host')
			ep.host = self.__variantReplace(ep.host,variants)

			ep.addr = e.getAttribute('address')
			ep.addr = self.__variantReplace(ep.addr,variants)

			ep.port = e.getAttribute('port')
			ep.port = self.__variantReplace(ep.port,variants)
			ep.port = int(ep.port)

			# print ep.host,ep.port

			ep.keyfile = e.getAttribute('keyfile').strip()
			ep.certfile = e.getAttribute('certfile').strip()
			s = e.getAttribute('compress').strip()
			if s:
				ep.compress = utils.intValueOfString(s,message.COMPRESS_ZLIB)

			epidx+=1
			epdefs[ep.name] = ep        # 记录通信端点

		# -- servers
		e = r.getElementsByTagName('servers')
		if not e:
			log_error('Tag: servers not found!')
			return False
		e2 = e[0].getElementsByTagName('server')
		for e in e2:
			if servername != e.getAttribute('name'):
				continue
			server = LocalServer()
			self.server = server
			server.name = e.getAttribute('name')
			'''
			type_ =  e.getAttribute('type')
			svc = svcdefs.get(type_)
			if not svc:
				log_error('service <%s> not defined!'%type_)
				return False
			server.service = svc
			server.id = int(e.getAttribute('id'))
			'''
			e3 = e.getElementsByTagName('route')
			for e4 in e3:
				route = RpcIfRouteDetail()
				ifname = e4.getAttribute('if')
				ifx = ifxdefs.get(ifname)
				if not ifx:
					log_error(' interface <%s> not defined!'%ifname)
					return False
				route.ifx = ifx

				e5 = e4.getElementsByTagName('call')        #RpcMsg CALL
				for e6 in e5:
					name = e6.getAttribute('in')
					ep = epdefs.get(name)
					inout = RpcRouteInoutPair()
					if not ep:
						print epdefs
						log_error('endpoint <%s> not defined!'%name)
						return False
					inout.in_ = ep
					server.ep_reads[ep.name] = ep   # cached ep
					server.name_eps[ep.name] = ep   # cached ep

					name = e6.getAttribute('out')
					ep = epdefs.get(name)
					if not ep:
						log_error('endpoint <%s> not defined!'%name)
						return False
					inout.out = ep
					server.ep_writes[ep.name] = ep  #cached ep
					server.name_eps[ep.name] = ep   #cached ep

					route.calls[inout.in_.id] = inout #id - increament value form 1

				e5 = e4.getElementsByTagName('return')   #RpcMsg RETURN
				for e6 in e5:
					name = e6.getAttribute('in')
					ep = epdefs.get(name)
					inout = RpcRouteInoutPair()
					if not ep:
						log_error('endpoint <%s> not defined!'%name)
						return False

					server.ep_reads[ep.name] = ep
					server.name_eps[ep.name] = ep
					inout.in_ = ep
					name = e6.getAttribute('out')
					ep = epdefs.get(name)
					if not ep:
						log_error('endpoint <%s> not defined!'%name)
						return False
					inout.out = ep
					server.ep_writes[ep.name] = ep
					server.name_eps[ep.name] = ep
					route.returns[inout.in_.id] = inout

				server.routes[route.ifx.id] = route  # cached route talbe of which interface
			#<extra_mqs/>
			els = e.getElementsByTagName('extra_mqs')
			if els:
				e5 = els[0]
				ins = e5.getAttribute('ins').strip().split(',')
				outs =e5.getAttribute('outs').strip().split(',')
				for name in ins:
					if not name.strip():continue
					ep = epdefs.get(name)
					if not ep:
						log_error('endpoint <%s> not defined!'%name)
						return False
					server.ep_reads[ep.name] = ep
					server.name_eps[ep.name] = ep

				for name in outs:
					if not name.strip():continue
					ep = epdefs.get(name)
					if not ep:
						log_error('endpoint <%s> not defined!'%name)
						return False
					server.ep_writes[ep.name] = ep
					server.name_eps[ep.name] = ep

			#properties  app 的属性配置
			els = e.getElementsByTagName('properties')
			if els:
				e5 = els[0]
				for e6 in e5.getElementsByTagName('property'):
					name = e6.getAttribute('name')
					value = e6.getAttribute('value')
					self.server.props[name] = value



		if not self.server:
			log_error('localserver not defined!')
			return False

#		print self.server.name_eps
#		print self.server.mq_reads
#		print self.server.mq_writes

		#打开ep，如是mq的情况，立刻能获取消息，此刻未绑定adapter，所以消息无法map到对应的rpc函数
		for ep in self.server.ep_reads.values():
			#print ep
			if not ep.open(AF_READ):
				return False

		for  ep in self.server.ep_writes.values():

			if not ep.open(AF_WRITE):
				return False

		return True



	def run(self):
		return True

	def waitForShutdown(self):
		self.pool.join()

		# for adapter in self.adapters.values():
		# 	adapter.join()



	def getServiceReadMQName(self,svc_id):
		'''
			根据 服务器id获取 服务接收数据的mq名称
		'''
		mq = ''
		try:
			svc_id = int(svc_id)
			type,id = (svc_id>>8)&0x7f, svc_id&0xff #类型的最高位不用
			mq = ''
			svc = self.getServiceDetail(type)
			if svc:
				mq =svc.pattern%id
		except:
			traceback.print_exc()
		return mq

	handle = None

Communicator = RpcCommunicator

class Shortcuts:
	@staticmethod
	def USER_ID(ctx):
		userid = ctx.msg.extra.getValue('__user_id__')
		return int(userid)

	@staticmethod
	def CALL_USER_ID(userid):
		return {'__user_id__':str(userid) }


def sleep(secs):
	# gevent.sleep(secs)
	time.sleep(secs)	#if gevent patched time

# def set_data_compression_on(flag):
# 	'''
# 		设置数据压缩启用和关闭,
# 			默认:启用压缩
# 	'''
# 	import message
# 	message.NetMetaPacket.data_compressoin_on = flag
