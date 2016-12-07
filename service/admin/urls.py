from django.conf.urls import patterns, include, url
import http
import admin
import sysadmin
import secadmin
import logadmin

urlpatterns = patterns('',

	# http.py
	url(r'^login/',http.login),
	url(r'^logout/',http.logout),
	url(r'^changePassword/',http.changePassword),
	url(r'^getCurrentUserInfo/',http.getCurrentUserInfo),
	url(r'^getSignImage/',http.getSignImage),

	# admin.py
	url(r'^getAllApp/',admin.getAllApp),

	# sysadmin.py
	url(r'^createApp/',sysadmin.createApp),
	url(r'^updateApp/',sysadmin.updateApp),
	url(r'^getAppList/',sysadmin.getAppList),
	url(r'^getAppDetail/',sysadmin.getAppDetail),
	url(r'^changeAppStatus/',sysadmin.changeAppStatus),
    url(r'^getAccountList/',sysadmin.getAccountList),
	url(r'^changeAccountStatus/',sysadmin.changeAccountStatus),
	url(r'^createAccount/',sysadmin.createAccount),
	url(r'^updateAccount/',sysadmin.updateAccount),
	url(r'^getAccountDetail/',sysadmin.getAccountDetail),
	url(r'^changeAccountPassword/',sysadmin.changeAccountPassword),

	# secadmin.py
	url(r'^createAppServer/',secadmin.createAppServer),
	url(r'^updateAppServer/',secadmin.updateAppServer),
	url(r'^getAppServerList/',secadmin.getAppServerList),
	url(r'^changeAppServerStatus/',secadmin.changeAppServerStatus),
	url(r'^getAppServerDetail/',secadmin.getAppServerDetail),

	# logadmin.py
	url(r'^getAdminLog/',logadmin.getAdminLog),
	url(r'^exportAdminLog/',logadmin.exportAdminLog),
	url(r'^getAppUserLog/',logadmin.getAppUserLog),
	url(r'^exportAppUserLog/',logadmin.exportAppUserLog),


)
