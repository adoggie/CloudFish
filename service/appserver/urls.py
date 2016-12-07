from django.conf.urls import patterns, include, url
import auth,file_api
urlpatterns = patterns('',

	url(r'^login/$',auth.userLogin),
	url(r'^logout/$',auth.userLogout),
	url(r'^files/$',file_api.FileView.as_view()),
	url(r'^share/$',file_api.share_file)

)
