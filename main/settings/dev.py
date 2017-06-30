from main.settings.base import *
import elasticsearch

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['*']


STATIC_ROOT = 'static/'


# Haystack connection
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': '<host_url>',
        'INDEX_NAME': '<index_name>',
        'KWARGS': {
            'use_ssl': True,
            'verify_certs': True,
            'connection_class': elasticsearch.RequestsHttpConnection,
        },
    },
}


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'icycle_db',
        'USER': 'icycle_db_user',
        'PASSWORD': 'icycle_db_password',
        'HOST': 'icycle.cylwbz3rz1yz.us-east-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}

