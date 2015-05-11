from django.conf.urls import patterns, include, url
from prototypeApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^index/byTime/$', views.indexByTime, name='indexByTime'),

    url(r'^about$', views.about, name='about'),
    
    url(r'^people$', views.people, name='people'),
    
    url(r'^login/$', views.login_view, name='login'),
    url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', views.logout_view, name='logout'),
    
    url(r'^event/(?P<event_id>\d+)/$', views.event, name='event'),
    url(r'^join_event/(?P<event_id>\d+)/$', views.join_event, name='join_event'),
    url(r'^decline_event/(?P<event_id>\d+)/$', views.decline_event, name='decline_event'),
    url(r'^leave_event/(?P<event_id>\d+)/$', views.leave_event, name='leave_event'),


    url(r'^group$', views.group, name='group'),
    url(r'^group/(?P<group_id>\d+)/$', views.aGroup, name='aGroup'),
    url(r'^leave_group/(?P<group_id>\d+)/$', views.leave_group, name='leave_group'),
    
    url(r'^add_friend/(?P<friend_id>\d+)/$', views.add_friend, name='add_friend'),
    url(r'^decline_friend/(?P<friend_id>\d+)/$', views.decline_friend, name='decline_friend'),
    url(r'^remove_friend/(?P<friend_id>\d+)/$', views.remove_friend, name='remove_friend'),

    url(r'^profile$', views.profile, name='profile'),

    # url('', include('django.contrib.auth.urls'))
    # url(r'password_change/$', 'django.contrib.auth.views.password_change', name='changePassword'),
    #override the default urls
    url(r'^password_change/$', auth_views.password_change, {'post_change_redirect' : '/prototypeApp/password_change/done/', 'template_name': 'registration/password_change_form_1.html'}, name="password_change"), 
    (r'^password_change/done/$', auth_views.password_change_done),
    # url(r'^password_change/$', auth_views.password_change, {'post_change_redirect': '/prototypeApp/password_change_done'}, name='/prototypeApp/changePassword'),
    # url(r'^password_change_done/$', auth_views.password_change_done, name='password_change_done'),

    # url(r'^password_change_done/$', auth_views.password_change_done, {'template_name': 'password_change_done.html'}),
    url(r'^password_reset/$', auth_views.password_reset, {'post_reset_redirect': '/prototypeApp/password_reset_done'}, name='password_reset_done'),
    url(r'^password_reset_done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password_reset_complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),


    #url(r'^sdk$', views.sdk, name='sdk'),

    #url('^', include('django.contrib.auth.urls')),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)