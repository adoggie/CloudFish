#--coding:utf-8--


'''
 socket通信方式的实现
 包括: connection , adapter,mqset
'''

from tce import *


class RpcAdapterMQ(RpcCommAdapter):
	def __init__(self,id,ep):
		RpcCommAdapter.__init__(self,id,ep)
		self.addConnection(ep.impl)
		ep.impl.attachAdapter(self)
		ep.impl = self      #


	@staticmethod
	def create(id,conn):
		adapter = RpcAdapterMQ(id,conn.ep)
		adapter.start()
		return adapter

	def start(self):
		print 'qpid-mq:<%s> adapter started!'%self.id

	def stop(self):
		self.ep.impl.close()        #关闭mq connection

	def sendMessage(self,m):
		if self.conns:
			c = self.conns[0]
			c.sendMessage(m)
			print 'one msg sent through mq!'




class RpcConnectionMQ_Collection:
	def __init__(self):
		self.list = {}

	_handle = None
	@classmethod
	def instance(cls):
		if not cls._handle:
			cls._handle = cls()
		return cls._handle

	def add(self,conn):
		self.list[conn.ep.getUnique()] = conn
		#print 'add in collection:',conn.ep.name

	def remove(self,conn):
		pass

	def get(self,name):
		return self.list.get(name)


RpcConnectionEasyMQ_Collection = RpcConnectionMQ_Collection
