################################################################################
# urls.py
# Defines urls for the entire project
################################################################################

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('^', include('django.contrib.auth.urls'))
]

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^prototypeApp/', include('prototypeApp.urls', namespace='prototypeApp')),
    url(r'^', include('prototypeApp.urls', namespace='prototypeApp')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
