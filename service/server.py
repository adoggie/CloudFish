#--coding:utf-8--


import imp,os,sys
import traceback,os,os.path,sys,time,ctypes


PATH = os.path.dirname(os.path.abspath(__file__))
imp.load_source('init',PATH +'/../init_script.py')

import init_script


from gevent import monkey
monkey.patch_all(socket=True,time=True,ssl=True,sys=True)
# monkey.patch_all()

import psycogreen.gevent
psycogreen.gevent.patch_psycopg()

from gevent.pywsgi import WSGIServer
from django.core.handlers.wsgi import WSGIHandler
import getopt
import lemon.utils

class ServerApp(lemon.utils.app.BaseAppServer):
	def __init__(self,name):
		lemon.utils.app.BaseAppServer.__init__(self,name)


	def initRpc(self):
		pass

	def initNosql(self):pass

	def initCache(self):pass


	def run(self):
		self.init(init_script.GLOBAL_SETTINGS_FILE,init_script.GLOBAL_SERVICE_FILE)

		#- init http service
		cfg = self.conf['http']
		host= cfg['host']
		if not host:
			host = ''
		address = (host,cfg['port'])
		ssl = cfg['ssl']
		lemon.utils.app.BaseAppServer.run(self)
		if ssl:
			print 'Webservice Serving [SSL] on %s...'%str(address)
			WSGIServer(address, WSGIHandler(),keyfile=cfg['keyfile'],certfile=cfg['certfile']).serve_forever()
		print 'WebService serving on %s...'%str(address)
		WSGIServer(address, WSGIHandler()).serve_forever()

def usage():
	pass


if __name__ == '__main__':
	"""identity = ServerApp(servername).getidentity()
	server.py
		-h
		help
		-n xxx
		--name=xxx
	"""

	if '--test' in sys.argv:
		import  test_unit
		sys.exit( test_unit.test())

	servername = 'cloudfish_server'
	try:
		options,args = getopt.getopt(sys.argv[1:],'hn:',['help','name='])
		for name,value in options:
			if name in ['-h',"--help"]:
				usage()
				sys.exit()
			if name in ('-n','--name'):
				servername = value
		print 'server name:',servername

		ServerApp(servername).run()

	except:
		traceback.print_exc()
		sys.exit()
