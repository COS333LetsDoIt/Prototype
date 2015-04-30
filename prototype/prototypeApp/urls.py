from django.conf.urls import patterns, include, url
from prototypeApp import views
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'prototype.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),

#     url(r'^$', views.index, name='index'),
# )

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    
    url(r'^people$', views.people, name='people'),
    
    url(r'^login/$', views.login_view, name='login'),
    url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', views.logout_view, name='logout'),
    
    url(r'^event/(?P<event_id>\d+)/$', views.event, name='event'),
    url(r'^join_event/(?P<event_id>\d+)/$', views.join_event, name='join_event'),
    url(r'^leave_event/(?P<event_id>\d+)/$', views.leave_event, name='leave_event'),

    url(r'^group$', views.group, name='group'),
    url(r'^group/(?P<group_id>\d+)/$', views.aGroup, name='aGroup'),
    url(r'^leave_group/(?P<group_id>\d+)/$', views.leave_group, name='leave_group'),
    
    url(r'^add_friend/(?P<friend_id>\d+)/$', views.add_friend, name='add_friend'),
    url(r'^remove_friend/(?P<friend_id>\d+)/$', views.remove_friend, name='remove_friend'),

    #url(r'^sdk$', views.sdk, name='sdk'),

    #url('^', include('django.contrib.auth.urls')),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)