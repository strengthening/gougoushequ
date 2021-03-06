"""
Django settings for gougoushequ project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__)).replace('\\','/')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#^00bi&=6%+c4_x&oh2@)$91yw28kw00tv8&i6gai5ck**vcqc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['www.5idoge.com','5idoge.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'gougoushequ',
    'weixin',
    'testapp',
    #'djcelery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gougoushequ.urls'

WSGI_APPLICATION = 'gougoushequ.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gougoushequ',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

TIME_ZONE = 'Asia/Shanghai'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

#TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False#True



#STATIC_ROOT = '/var/www/html/gougoushequ/static/'

# STATIC_ROOT = os.path.join(BASE_DIR,'static').replace('\\','/')
# print STATIC_ROOT

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, STATIC_URL.replace("/", ""))

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(BASE_DIR, "static").replace('\\','/'),
    MEDIA_ROOT,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#    '/var/www/html/gougoushequ/templates',
    os.path.join(BASE_DIR,'templates').replace('\\','/')
    
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': ['115.28.51.15:11211'],
#        'TIMEOUT': 60,
#    }
#}


WEIXIN = {
    'appid':'wx9d377fa47a93e6d6',
    'appsecret':'35019e0992dc1f715571a5375ca35c68',
    'token':'dogecoinchina',
    'encodingaeskey':'WgcW5hFF61wJCkUXmCDiSsdx7e8eA47mhlVSSr7HWr0',
    'prefix':'ggsq_',
    'username':'gougoushequ',
    'domainname':'www.5idoge.com',
    'istest':0,
    'fileurl':'/var/www/',
}

WEIXIN_TOKEN='dogecoinchina'


#WEIXIN = {
#    'appid':'wxa4ac32f98462cc3d',
#    'appsecret':'43b07fae59164da9274c1c74fe399ef4',
#    'token':'dogecoinchina',
#    'encodingaeskey':'WgcW5hFF61wJCkUXmCDiSsdx7e8eA47mhlVSSr7HWr0',
#    'prefix':'test_',
#    'username':'gh_fc6c5bc238f0',
#    'istest':1,
#    'domainname':'50.62.58.107',
#    'fileurl':'/var/www/html/',
#}

DOGECOIND = {
    'rpc_username':'strengthening',
    'rpc_password':'iedeebahngoekoh6idohgh2Ni1ahmi',
    'rpc_ip':'115.28.51.15',
}

#DOGECOIND = {
#    'rpc_username':'<strengthening>',
#    'rpc_password':'<dcg8280828>',
#    'rpc_ip':'115.28.51.15',
#}


BROKER_URL = 'amqp://guest:guest@localhost:5672//'
#BROKER_TRANSPORT = 'redis'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 60*60*36}
#CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER='json'
CELERY_ACCEPT_CONTENT=['json']  # Ignore other content
CELERY_RESULT_SERIALIZER='json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
