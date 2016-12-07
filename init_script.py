__author__ = 'scott'

import os,sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "model.django.project.settings")
pwd =''
PRJ_PATH = os.path.dirname(os.path.abspath(__file__))

ETC_PATH = PRJ_PATH  +'/etc'

LIBS=(
	PRJ_PATH,
	PRJ_PATH+'/libs/python',
	PRJ_PATH+'/libs/fa64',
	# TCE_PATH
)
for lib in LIBS:
	sys.path.insert(0,lib)

#from model.django.project import  settings

GLOBAL_SETTINGS_FILE = ETC_PATH + '/settings.yaml'
GLOBAL_SERVICE_FILE = ETC_PATH + '/services.xml'
GLOBAL_SERVER_EPS_FILE = ETC_PATH + '/server_eps.conf'

if __name__ == '__main__':
	print globals()