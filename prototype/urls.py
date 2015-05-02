from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    url('^', include('django.contrib.auth.urls'))
]

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prototype.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'', include('social_auth.urls')),
    url(r'^prototypeApp/', include('prototypeApp.urls', namespace='prototypeApp')),
    url(r'^', include('prototypeApp.urls', namespace='prototypeApp')),
    # url(r'^index$', views.index, name='index'),
    # url(r'^$', views.index, name='index'),


)