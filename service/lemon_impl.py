
# -- coding:utf-8 --

#---------------------------------
#  TCE
#  Tiny Communication Engine
#
#  sw2us.com copyright @2012
#  bin.zhang@sw2us.com / qq:24509826
#---------------------------------

import os,os.path,sys,struct,time,traceback,time
import tcelib as tce

	
class StringList_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		for o in self.ds:
			if type(o)==type(0) or type(o) == type(0.1): o=str(o)
			if not o: o=''
			try:
				o = o.encode('utf-8')
			except:pass
			d += struct.pack('!I', len(str(o)))
			d += str(o)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			p = 0
			while p < size_:
				__size, = struct.unpack('!I',d[idx:idx+4])
				idx+=4
				v = d[idx:idx+__size]
				idx+=__size
				self.ds.append(v)
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class IntList_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		for o in self.ds:
			d += struct.pack('!i',o)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			p = 0
			while p < size_:
				v, = struct.unpack('!i',d[idx:idx+4])
				idx+=4
				self.ds.append(v)
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class UserIdList_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		for o in self.ds:
			if type(o)==type(0) or type(o) == type(0.1): o=str(o)
			if not o: o=''
			try:
				o = o.encode('utf-8')
			except:pass
			d += struct.pack('!I', len(str(o)))
			d += str(o)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			p = 0
			while p < size_:
				__size, = struct.unpack('!I',d[idx:idx+4])
				idx+=4
				v = d[idx:idx+__size]
				idx+=__size
				self.ds.append(v)
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class SIDS_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		for o in self.ds:
			if type(o)==type(0) or type(o) == type(0.1): o=str(o)
			if not o: o=''
			try:
				o = o.encode('utf-8')
			except:pass
			d += struct.pack('!I', len(str(o)))
			d += str(o)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			p = 0
			while p < size_:
				__size, = struct.unpack('!I',d[idx:idx+4])
				idx+=4
				v = d[idx:idx+__size]
				idx+=__size
				self.ds.append(v)
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class StrStr_t:
	# -- THIS IS DICTIONARY! --
	def __init__(self,ds={}):
		self.ds = ds
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds.keys()))
		for k,v in self.ds.items():
			if type(k)==type(0) or type(k) == type(0.1): k=str(k)
			if not k: k=''
			try:
				k = k.encode('utf-8')
			except:pass
			d += struct.pack('!I', len(str(k)))
			d += str(k)
			if type(v)==type(0) or type(v) == type(0.1): v=str(v)
			if not v: v=''
			try:
				v = v.encode('utf-8')
			except:pass
			d += struct.pack('!I', len(str(v)))
			d += str(v)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			_size,= struct.unpack('!I',d[idx:idx+4])
			p = 0
			idx += 4
			while p < _size:
				__size, = struct.unpack('!I',d[idx:idx+4])
				idx+=4
				x = d[idx:idx+__size]
				idx+=__size
				__size, = struct.unpack('!I',d[idx:idx+4])
				idx+=4
				y = d[idx:idx+__size]
				idx+=__size
				self.ds[x] = y
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class StrStrList_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		for o in self.ds:
			container = StrStr_t(o)
			d += container.marshall()
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			p = 0
			while p < size_:
				o ={}
				container = StrStr_t(o)
				r,idx = container.unmarshall(d,idx)
				if not r: return False,idx
				self.ds.append(o)
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class Properties_t:
	# -- THIS IS DICTIONARY! --
	def __init__(self,ds={}):
		self.ds = ds
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds.keys()))
		for k,v in self.ds.items():
			if type(k)==type(0) or type(k) == type(0.1): k=str(k)
			if not k: k=''
			try:
				k = k.encode('utf-8')
			except:pass
			d += struct.pack('!I', len(str(k)))
			d += str(k)
			if type(v)==type(0) or type(v) == type(0.1): v=str(v)
			if not v: v=''
			try:
				v = v.encode('utf-8')
			except:pass
			d += struct.pack('!I', len(str(v)))
			d += str(v)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			_size,= struct.unpack('!I',d[idx:idx+4])
			p = 0
			idx += 4
			while p < _size:
				__size, = struct.unpack('!I',d[idx:idx+4])
				idx+=4
				x = d[idx:idx+__size]
				idx+=__size
				__size, = struct.unpack('!I',d[idx:idx+4])
				idx+=4
				y = d[idx:idx+__size]
				idx+=__size
				self.ds[x] = y
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class StreamData_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		d+=self.ds
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			self.ds = d[idx:idx+size_]
			idx+=size_
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class BinaryStream_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		d+=self.ds
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			self.ds = d[idx:idx+size_]
			idx+=size_
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class ImageData_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		d+=self.ds
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			self.ds = d[idx:idx+size_]
			idx+=size_
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class ImageDataList_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		for o in self.ds:
			container = ImageData_t(o)
			d += container.marshall()
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			p = 0
			while p < size_:
				o =[]
				container = ImageData_t(o)
				r,idx = container.unmarshall(d,idx)
				if not r: return False,idx
				o = container.ds
				self.ds.append(o)
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class StreamDataArray_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		for o in self.ds:
			container = StreamData_t(o)
			d += container.marshall()
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			p = 0
			while p < size_:
				o =[]
				container = StreamData_t(o)
				r,idx = container.unmarshall(d,idx)
				if not r: return False,idx
				o = container.ds
				self.ds.append(o)
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class Error_t:
# -- STRUCT -- 
	def __init__(self,succ=False,code=0,msg=''):
		self.succ = succ
		self.code = code
		self.msg = msg
		
	def __str__(self):
		return 'OBJECT<Error_t :%s> { succ:%s,code:%s,msg:%s}'%(hex(id(self)),str(self.succ),str(self.code),str(self.msg) ) 
		
	def marshall(self):
		d =''
		if self.succ == True:self.succ=1
		else: self.succ=0
		d += struct.pack('B',self.succ)
		d += struct.pack('!i',self.code)
		if type(self.msg)==type(0) or type(self.msg) == type(0.1): self.msg=str(self.msg)
		if not self.msg: self.msg=''
		try:
			self.msg = self.msg.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.msg)))
		d += str(self.msg)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.succ, = struct.unpack('B',d[idx:idx+1])
			if self.succ == 0: self.succ = False
			else: self.succ = True
			idx+=1
			self.code, = struct.unpack('!i',d[idx:idx+4])
			idx+=4
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.msg = d[idx:idx+__size]
			idx+=__size
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class CallReturn_t:
# -- STRUCT -- 
	def __init__(self,error=Error_t(),value='',delta=''):
		self.error = error
		self.value = value
		self.delta = delta
		
	def __str__(self):
		return 'OBJECT<CallReturn_t :%s> { error:%s,value:%s,delta:%s}'%(hex(id(self)),str(self.error),str(self.value),str(self.delta) ) 
		
	def marshall(self):
		d =''
		d += self.error.marshall()
		if type(self.value)==type(0) or type(self.value) == type(0.1): self.value=str(self.value)
		if not self.value: self.value=''
		try:
			self.value = self.value.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.value)))
		d += str(self.value)
		if type(self.delta)==type(0) or type(self.delta) == type(0.1): self.delta=str(self.delta)
		if not self.delta: self.delta=''
		try:
			self.delta = self.delta.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.delta)))
		d += str(self.delta)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			r,idx = self.error.unmarshall(d,idx)
			if not r: return False,idx
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.value = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.delta = d[idx:idx+__size]
			idx+=__size
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class TimeRange_t:
# -- STRUCT -- 
	def __init__(self,start=0,end=0):
		self.start = start
		self.end = end
		
	def __str__(self):
		return 'OBJECT<TimeRange_t :%s> { start:%s,end:%s}'%(hex(id(self)),str(self.start),str(self.end) ) 
		
	def marshall(self):
		d =''
		d += struct.pack('!q',self.start)
		d += struct.pack('!q',self.end)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.start, = struct.unpack('!q',d[idx:idx+8])
			idx+=8
			self.end, = struct.unpack('!q',d[idx:idx+8])
			idx+=8
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class ResultPageCtrl_t:
# -- STRUCT -- 
	def __init__(self,page_size=0,page_index=0):
		self.page_size = page_size
		self.page_index = page_index
		
	def __str__(self):
		return 'OBJECT<ResultPageCtrl_t :%s> { page_size:%s,page_index:%s}'%(hex(id(self)),str(self.page_size),str(self.page_index) ) 
		
	def marshall(self):
		d =''
		d += struct.pack('!i',self.page_size)
		d += struct.pack('!i',self.page_index)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.page_size, = struct.unpack('!i',d[idx:idx+4])
			idx+=4
			self.page_index, = struct.unpack('!i',d[idx:idx+4])
			idx+=4
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class AuthResult_t:
# -- STRUCT -- 
	def __init__(self,user_id='',user_name='',user_realname='',login_time=0,login_type=0,expire_time=0,device_id=''):
		self.user_id = user_id
		self.user_name = user_name
		self.user_realname = user_realname
		self.login_time = login_time
		self.login_type = login_type
		self.expire_time = expire_time
		self.device_id = device_id
		
	def __str__(self):
		return 'OBJECT<AuthResult_t :%s> { user_id:%s,user_name:%s,user_realname:%s,login_time:%s,login_type:%s,expire_time:%s,device_id:%s}'%(hex(id(self)),str(self.user_id),str(self.user_name),str(self.user_realname),str(self.login_time),str(self.login_type),str(self.expire_time),str(self.device_id) ) 
		
	def marshall(self):
		d =''
		if type(self.user_id)==type(0) or type(self.user_id) == type(0.1): self.user_id=str(self.user_id)
		if not self.user_id: self.user_id=''
		try:
			self.user_id = self.user_id.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.user_id)))
		d += str(self.user_id)
		if type(self.user_name)==type(0) or type(self.user_name) == type(0.1): self.user_name=str(self.user_name)
		if not self.user_name: self.user_name=''
		try:
			self.user_name = self.user_name.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.user_name)))
		d += str(self.user_name)
		if type(self.user_realname)==type(0) or type(self.user_realname) == type(0.1): self.user_realname=str(self.user_realname)
		if not self.user_realname: self.user_realname=''
		try:
			self.user_realname = self.user_realname.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.user_realname)))
		d += str(self.user_realname)
		d += struct.pack('!q',self.login_time)
		d += struct.pack('!i',self.login_type)
		d += struct.pack('!q',self.expire_time)
		if type(self.device_id)==type(0) or type(self.device_id) == type(0.1): self.device_id=str(self.device_id)
		if not self.device_id: self.device_id=''
		try:
			self.device_id = self.device_id.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.device_id)))
		d += str(self.device_id)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.user_id = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.user_name = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.user_realname = d[idx:idx+__size]
			idx+=__size
			self.login_time, = struct.unpack('!q',d[idx:idx+8])
			idx+=8
			self.login_type, = struct.unpack('!i',d[idx:idx+4])
			idx+=4
			self.expire_time, = struct.unpack('!q',d[idx:idx+8])
			idx+=8
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.device_id = d[idx:idx+__size]
			idx+=__size
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class NotifyMessage_t:
# -- STRUCT -- 
	def __init__(self,issue_user='',issue_unit='',issue_time='',type_=0,p1='',p2='',p3='',p4=''):
		self.issue_user = issue_user
		self.issue_unit = issue_unit
		self.issue_time = issue_time
		self.type_ = type_
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.p4 = p4
		
	def __str__(self):
		return 'OBJECT<NotifyMessage_t :%s> { issue_user:%s,issue_unit:%s,issue_time:%s,type_:%s,p1:%s,p2:%s,p3:%s,p4:%s}'%(hex(id(self)),str(self.issue_user),str(self.issue_unit),str(self.issue_time),str(self.type_),str(self.p1),str(self.p2),str(self.p3),str(self.p4) ) 
		
	def marshall(self):
		d =''
		if type(self.issue_user)==type(0) or type(self.issue_user) == type(0.1): self.issue_user=str(self.issue_user)
		if not self.issue_user: self.issue_user=''
		try:
			self.issue_user = self.issue_user.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.issue_user)))
		d += str(self.issue_user)
		if type(self.issue_unit)==type(0) or type(self.issue_unit) == type(0.1): self.issue_unit=str(self.issue_unit)
		if not self.issue_unit: self.issue_unit=''
		try:
			self.issue_unit = self.issue_unit.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.issue_unit)))
		d += str(self.issue_unit)
		if type(self.issue_time)==type(0) or type(self.issue_time) == type(0.1): self.issue_time=str(self.issue_time)
		if not self.issue_time: self.issue_time=''
		try:
			self.issue_time = self.issue_time.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.issue_time)))
		d += str(self.issue_time)
		d += struct.pack('!i',self.type_)
		if type(self.p1)==type(0) or type(self.p1) == type(0.1): self.p1=str(self.p1)
		if not self.p1: self.p1=''
		try:
			self.p1 = self.p1.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.p1)))
		d += str(self.p1)
		if type(self.p2)==type(0) or type(self.p2) == type(0.1): self.p2=str(self.p2)
		if not self.p2: self.p2=''
		try:
			self.p2 = self.p2.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.p2)))
		d += str(self.p2)
		if type(self.p3)==type(0) or type(self.p3) == type(0.1): self.p3=str(self.p3)
		if not self.p3: self.p3=''
		try:
			self.p3 = self.p3.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.p3)))
		d += str(self.p3)
		if type(self.p4)==type(0) or type(self.p4) == type(0.1): self.p4=str(self.p4)
		if not self.p4: self.p4=''
		try:
			self.p4 = self.p4.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.p4)))
		d += str(self.p4)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.issue_user = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.issue_unit = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.issue_time = d[idx:idx+__size]
			idx+=__size
			self.type_, = struct.unpack('!i',d[idx:idx+4])
			idx+=4
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.p1 = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.p2 = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.p3 = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.p4 = d[idx:idx+__size]
			idx+=__size
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class ITerminal:
	# -- INTERFACE -- 
	def __init__(self):
		if not hasattr(self,'delegatecls'):
			self.delegatecls = {}
		self.delegatecls[201] = ITerminal_delegate
	
	def onNotifyMessage(self,msg,ctx):
		pass
	

class ITerminal_delegate:
	def __init__(self,inst,adapter,conn=None):
		self.index = 201
		self.optlist={}
		self.id = '' 
		self.adapter = adapter
		self.optlist[0] = (self.onNotifyMessage)
		
		self.inst = inst
	
	def onNotifyMessage(self,ctx):
		print "callin (onNotifyMessage)"
		d = ctx.msg.paramstream 
		idx = 0
		_p_msg = NotifyMessage_t()
		r,idx = _p_msg.unmarshall(d,idx)
		if not r: return False
		cr = None
		self.inst.onNotifyMessage(_p_msg,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn()
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	
class ITerminalPrx:
	# -- INTERFACE PROXY -- 
	def __init__(self,conn):
		self.conn = conn
		self.delta = None
		pass
	
	@staticmethod
	def create(endpoint):
		conn = tce.RpcConnectionSocket(ep=endpoint)
		proxy = ITerminalPrx(conn)
		return proxy
	
	@staticmethod
	def createWithEpName(name):
		ep = tce.RpcCommunicator.instance().currentServer().findEndPointByName(name)
		if not ep: return None
		conn = ep.impl
		proxy = ITerminalPrx(conn)
		return proxy
	
	@staticmethod
	def createWithProxy(prx):
		proxy = ITerminalPrx(prx.conn)
		return proxy
	
	#extra must be map<string,string>
	def onNotifyMessage(self,msg,timeout=None,extra={}):
		# function index: 18
		
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 201
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		d_2 += msg.marshall()
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def onNotifyMessage_async(self,msg,async,extra={}):
		# function index: 18
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 201
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		d_3 += msg.marshall()
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = ITerminalPrx.onNotifyMessage_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def onNotifyMessage_asyncparser(m,m2):
		# function index: 18 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3)
		except:
			traceback.print_exc()
		
	
	def onNotifyMessage_oneway(self,msg,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall()
			m_1.ifidx = 201
			m_1.opidx = 0
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			d_2 += msg.marshall()
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	

class IUserEventListener:
	# -- INTERFACE -- 
	def __init__(self):
		if not hasattr(self,'delegatecls'):
			self.delegatecls = {}
		self.delegatecls[413] = IUserEventListener_delegate
	
	def onUserOnline(self,userid,tgs_id,device,ctx):
		pass
	
	def onUserOffline(self,userid,tgs_id,device,ctx):
		pass
	

class IUserEventListener_delegate:
	def __init__(self,inst,adapter,conn=None):
		self.index = 413
		self.optlist={}
		self.id = '' 
		self.adapter = adapter
		self.optlist[0] = (self.onUserOnline)
		self.optlist[1] = (self.onUserOffline)
		
		self.inst = inst
	
	def onUserOnline(self,ctx):
		print "callin (onUserOnline)"
		d = ctx.msg.paramstream 
		idx = 0
		__size, = struct.unpack('!I',d[idx:idx+4])
		idx+=4
		_p_userid = d[idx:idx+__size]
		idx+=__size
		__size, = struct.unpack('!I',d[idx:idx+4])
		idx+=4
		_p_tgs_id = d[idx:idx+__size]
		idx+=__size
		_p_device, = struct.unpack('!i',d[idx:idx+4])
		idx+=4
		cr = None
		self.inst.onUserOnline(_p_userid,_p_tgs_id,_p_device,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn()
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	def onUserOffline(self,ctx):
		print "callin (onUserOffline)"
		d = ctx.msg.paramstream 
		idx = 0
		__size, = struct.unpack('!I',d[idx:idx+4])
		idx+=4
		_p_userid = d[idx:idx+__size]
		idx+=__size
		__size, = struct.unpack('!I',d[idx:idx+4])
		idx+=4
		_p_tgs_id = d[idx:idx+__size]
		idx+=__size
		_p_device, = struct.unpack('!i',d[idx:idx+4])
		idx+=4
		cr = None
		self.inst.onUserOffline(_p_userid,_p_tgs_id,_p_device,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn()
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	
class IUserEventListenerPrx:
	# -- INTERFACE PROXY -- 
	def __init__(self,conn):
		self.conn = conn
		self.delta = None
		pass
	
	@staticmethod
	def create(endpoint):
		conn = tce.RpcConnectionSocket(ep=endpoint)
		proxy = IUserEventListenerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithEpName(name):
		ep = tce.RpcCommunicator.instance().currentServer().findEndPointByName(name)
		if not ep: return None
		conn = ep.impl
		proxy = IUserEventListenerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithProxy(prx):
		proxy = IUserEventListenerPrx(prx.conn)
		return proxy
	
	#extra must be map<string,string>
	def onUserOnline(self,userid,tgs_id,device,timeout=None,extra={}):
		# function index: 19
		
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 413
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		if type(userid)==type(0) or type(userid) == type(0.1): userid=str(userid)
		if not userid: userid=''
		try:
			userid = userid.encode('utf-8')
		except:pass
		d_2 += struct.pack('!I', len(str(userid)))
		d_2 += str(userid)
		m_1.paramstream += d_2
		d_2 = '' 
		if type(tgs_id)==type(0) or type(tgs_id) == type(0.1): tgs_id=str(tgs_id)
		if not tgs_id: tgs_id=''
		try:
			tgs_id = tgs_id.encode('utf-8')
		except:pass
		d_2 += struct.pack('!I', len(str(tgs_id)))
		d_2 += str(tgs_id)
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 += struct.pack('!i',device)
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def onUserOnline_async(self,userid,tgs_id,device,async,extra={}):
		# function index: 19
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 413
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		if type(userid)==type(0) or type(userid) == type(0.1): userid=str(userid)
		if not userid: userid=''
		try:
			userid = userid.encode('utf-8')
		except:pass
		d_3 += struct.pack('!I', len(str(userid)))
		d_3 += str(userid)
		m_1.paramstream += d_3
		d_3 = '' 
		if type(tgs_id)==type(0) or type(tgs_id) == type(0.1): tgs_id=str(tgs_id)
		if not tgs_id: tgs_id=''
		try:
			tgs_id = tgs_id.encode('utf-8')
		except:pass
		d_3 += struct.pack('!I', len(str(tgs_id)))
		d_3 += str(tgs_id)
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 += struct.pack('!i',device)
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = IUserEventListenerPrx.onUserOnline_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def onUserOnline_asyncparser(m,m2):
		# function index: 19 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3)
		except:
			traceback.print_exc()
		
	
	def onUserOnline_oneway(self,userid,tgs_id,device,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall()
			m_1.ifidx = 413
			m_1.opidx = 0
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			if type(userid)==type(0) or type(userid) == type(0.1): userid=str(userid)
			if not userid: userid=''
			try:
				userid = userid.encode('utf-8')
			except:pass
			d_2 += struct.pack('!I', len(str(userid)))
			d_2 += str(userid)
			m_1.paramstream += d_2
			d_2 = '' 
			if type(tgs_id)==type(0) or type(tgs_id) == type(0.1): tgs_id=str(tgs_id)
			if not tgs_id: tgs_id=''
			try:
				tgs_id = tgs_id.encode('utf-8')
			except:pass
			d_2 += struct.pack('!I', len(str(tgs_id)))
			d_2 += str(tgs_id)
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 += struct.pack('!i',device)
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	#extra must be map<string,string>
	def onUserOffline(self,userid,tgs_id,device,timeout=None,extra={}):
		# function index: idx_4
		
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 413
		m_1.opidx = 1
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		if type(userid)==type(0) or type(userid) == type(0.1): userid=str(userid)
		if not userid: userid=''
		try:
			userid = userid.encode('utf-8')
		except:pass
		d_2 += struct.pack('!I', len(str(userid)))
		d_2 += str(userid)
		m_1.paramstream += d_2
		d_2 = '' 
		if type(tgs_id)==type(0) or type(tgs_id) == type(0.1): tgs_id=str(tgs_id)
		if not tgs_id: tgs_id=''
		try:
			tgs_id = tgs_id.encode('utf-8')
		except:pass
		d_2 += struct.pack('!I', len(str(tgs_id)))
		d_2 += str(tgs_id)
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 += struct.pack('!i',device)
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def onUserOffline_async(self,userid,tgs_id,device,async,extra={}):
		# function index: idx_4
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 413
		m_1.opidx = 1
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		if type(userid)==type(0) or type(userid) == type(0.1): userid=str(userid)
		if not userid: userid=''
		try:
			userid = userid.encode('utf-8')
		except:pass
		d_3 += struct.pack('!I', len(str(userid)))
		d_3 += str(userid)
		m_1.paramstream += d_3
		d_3 = '' 
		if type(tgs_id)==type(0) or type(tgs_id) == type(0.1): tgs_id=str(tgs_id)
		if not tgs_id: tgs_id=''
		try:
			tgs_id = tgs_id.encode('utf-8')
		except:pass
		d_3 += struct.pack('!I', len(str(tgs_id)))
		d_3 += str(tgs_id)
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 += struct.pack('!i',device)
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = IUserEventListenerPrx.onUserOffline_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def onUserOffline_asyncparser(m,m2):
		# function index: idx_4 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3)
		except:
			traceback.print_exc()
		
	
	def onUserOffline_oneway(self,userid,tgs_id,device,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall()
			m_1.ifidx = 413
			m_1.opidx = 1
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			if type(userid)==type(0) or type(userid) == type(0.1): userid=str(userid)
			if not userid: userid=''
			try:
				userid = userid.encode('utf-8')
			except:pass
			d_2 += struct.pack('!I', len(str(userid)))
			d_2 += str(userid)
			m_1.paramstream += d_2
			d_2 = '' 
			if type(tgs_id)==type(0) or type(tgs_id) == type(0.1): tgs_id=str(tgs_id)
			if not tgs_id: tgs_id=''
			try:
				tgs_id = tgs_id.encode('utf-8')
			except:pass
			d_2 += struct.pack('!I', len(str(tgs_id)))
			d_2 += str(tgs_id)
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 += struct.pack('!i',device)
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	

class ITerminalGatewayServer:
	# -- INTERFACE -- 
	def __init__(self):
		if not hasattr(self,'delegatecls'):
			self.delegatecls = {}
		self.delegatecls[409] = ITerminalGatewayServer_delegate
	
	def ping(self,ctx):
		pass
	

class ITerminalGatewayServer_delegate:
	def __init__(self,inst,adapter,conn=None):
		self.index = 409
		self.optlist={}
		self.id = '' 
		self.adapter = adapter
		self.optlist[0] = (self.ping)
		
		self.inst = inst
	
	def ping(self,ctx):
		print "callin (ping)"
		d = ctx.msg.paramstream 
		idx = 0
		cr = None
		self.inst.ping(ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn()
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	
class ITerminalGatewayServerPrx:
	# -- INTERFACE PROXY -- 
	def __init__(self,conn):
		self.conn = conn
		self.delta = None
		pass
	
	@staticmethod
	def create(endpoint):
		conn = tce.RpcConnectionSocket(ep=endpoint)
		proxy = ITerminalGatewayServerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithEpName(name):
		ep = tce.RpcCommunicator.instance().currentServer().findEndPointByName(name)
		if not ep: return None
		conn = ep.impl
		proxy = ITerminalGatewayServerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithProxy(prx):
		proxy = ITerminalGatewayServerPrx(prx.conn)
		return proxy
	
	#extra must be map<string,string>
	def ping(self,timeout=None,extra={}):
		# function index: 20
		
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 409
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def ping_async(self,async,extra={}):
		# function index: 20
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 409
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = ITerminalGatewayServerPrx.ping_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def ping_asyncparser(m,m2):
		# function index: 20 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3)
		except:
			traceback.print_exc()
		
	
	def ping_oneway(self,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall()
			m_1.ifidx = 409
			m_1.opidx = 0
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	

class IMessageServer:
	# -- INTERFACE -- 
	def __init__(self):
		if not hasattr(self,'delegatecls'):
			self.delegatecls = {}
		self.delegatecls[408] = IMessageServer_delegate
	
	def sendNotification(self,target_unit,target_user_role,msg,ctx):
		pass
	

class IMessageServer_delegate:
	def __init__(self,inst,adapter,conn=None):
		self.index = 408
		self.optlist={}
		self.id = '' 
		self.adapter = adapter
		self.optlist[0] = (self.sendNotification)
		
		self.inst = inst
	
	def sendNotification(self,ctx):
		print "callin (sendNotification)"
		d = ctx.msg.paramstream 
		idx = 0
		__size, = struct.unpack('!I',d[idx:idx+4])
		idx+=4
		_p_target_unit = d[idx:idx+__size]
		idx+=__size
		_p_target_user_role, = struct.unpack('!i',d[idx:idx+4])
		idx+=4
		_p_msg = NotifyMessage_t()
		r,idx = _p_msg.unmarshall(d,idx)
		if not r: return False
		cr = None
		self.inst.sendNotification(_p_target_unit,_p_target_user_role,_p_msg,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn()
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	
class IMessageServerPrx:
	# -- INTERFACE PROXY -- 
	def __init__(self,conn):
		self.conn = conn
		self.delta = None
		pass
	
	@staticmethod
	def create(endpoint):
		conn = tce.RpcConnectionSocket(ep=endpoint)
		proxy = IMessageServerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithEpName(name):
		ep = tce.RpcCommunicator.instance().currentServer().findEndPointByName(name)
		if not ep: return None
		conn = ep.impl
		proxy = IMessageServerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithProxy(prx):
		proxy = IMessageServerPrx(prx.conn)
		return proxy
	
	#extra must be map<string,string>
	def sendNotification(self,target_unit,target_user_role,msg,timeout=None,extra={}):
		# function index: 21
		
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 408
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		if type(target_unit)==type(0) or type(target_unit) == type(0.1): target_unit=str(target_unit)
		if not target_unit: target_unit=''
		try:
			target_unit = target_unit.encode('utf-8')
		except:pass
		d_2 += struct.pack('!I', len(str(target_unit)))
		d_2 += str(target_unit)
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 += struct.pack('!i',target_user_role)
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 += msg.marshall()
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def sendNotification_async(self,target_unit,target_user_role,msg,async,extra={}):
		# function index: 21
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall()
		m_1.ifidx = 408
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		if type(target_unit)==type(0) or type(target_unit) == type(0.1): target_unit=str(target_unit)
		if not target_unit: target_unit=''
		try:
			target_unit = target_unit.encode('utf-8')
		except:pass
		d_3 += struct.pack('!I', len(str(target_unit)))
		d_3 += str(target_unit)
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 += struct.pack('!i',target_user_role)
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 += msg.marshall()
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = IMessageServerPrx.sendNotification_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def sendNotification_asyncparser(m,m2):
		# function index: 21 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3)
		except:
			traceback.print_exc()
		
	
	def sendNotification_oneway(self,target_unit,target_user_role,msg,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall()
			m_1.ifidx = 408
			m_1.opidx = 0
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			if type(target_unit)==type(0) or type(target_unit) == type(0.1): target_unit=str(target_unit)
			if not target_unit: target_unit=''
			try:
				target_unit = target_unit.encode('utf-8')
			except:pass
			d_2 += struct.pack('!I', len(str(target_unit)))
			d_2 += str(target_unit)
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 += struct.pack('!i',target_user_role)
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 += msg.marshall()
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	

