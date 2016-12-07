# coding:utf-8
from django.conf.urls import patterns, include, url

import http

urlpatterns = patterns('',

    url(r'^getSignImage/',http.getSignImage),
    # url(r'^fileDownload/',http.fileDownload),
	# #- notice
    # url(r'^getNoticeList/',notice.getNoticeList),
    # url(r'^getNoticeDetail/',notice.getNoticeDetail),
    # url(r'^createNotice/',notice.createNotice),
    # url(r'^removeNotice/',notice.removeNotice),
    # url(r'^updateNotice/',notice.updateNotice),



)
