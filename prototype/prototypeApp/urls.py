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
    url(r'^group$', views.group, name='group'),
    url(r'^event/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)