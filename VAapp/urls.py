from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^signup/$', views.signup, name = 'signup'),
	url(r'^login/$', views.enter, name = 'enter'),
	url(r'^logout/$', views.exit, name = 'exit'),
	url(r'^reset_password/', views.reset_password, name = 'reset_password'),

	url(r'^admin_panel/', views.admin_panel, name = 'admin_panel'),
	url(r'^questions/(?P<username>.*)', views.questions, name = 'questions'),

	url(r'^all_polls/$', views.all_polls, name = 'all_polls'),
	url(r'^my_polls/$', views.my_polls, name = 'my_polls'),
	url(r'^create_poll/$', views.create_poll, name = 'create_poll'),
	url(r'^delete_poll/(?P<username>.*)/(?P<question>.*)$', views.delete_poll, name = 'delete_poll'),
	url(r'^vote/(?P<username>.*)/(?P<question>.*)/(?P<option>.*)$', views.vote, name = 'vote')
]