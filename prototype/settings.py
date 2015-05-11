################################################################################
# settings.py
# Django settings for the project
#
# For more information on this file, see
# https://docs.djangoproject.com/en/1.7/topics/settings/
#
# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/1.7/ref/settings/
################################################################################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'prototypeApp/static/'),
)



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


LOGIN_URL = 'login/'
LOGIN_REDIRECT_URL = 'login/'
LOGIN_ERROR_URL    = 'login/'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lchjyz-rt38ukt67qe%v4%*f4p1s%rqavtc3z&z50-xavlnnq%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

# run pip install django-social-auth if necessary
FACEBOOK_APP_ID='357630157777770'
FACEBOOK_API_SECRET='a4868abb9b426a24d3c0923ebd6a99b2'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ALLOWED_HOSTS = ['http://lets-do-it.tk/', 'http://ec2-52-6-54-4.compute-1.amazonaws.com/', '52.6.54.4/']


# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'prototypeApp',
    'imagekit',
    'django.contrib.admin',
    #'social_auth',
    #'datetimewidget'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
)

ROOT_URLCONF = 'prototype.urls'

WSGI_APPLICATION = 'prototype.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'letsdoit.noresponse@gmail.com'
EMAIL_HOST_PASSWORD = 'flyingdragon'
DEFAULT_FROM_EMAIL = 'letsdoit.noresponse@gmail.com'
DEFAULT_TO_EMAIL = 'letsdoit.noresponse@gmail.com'
