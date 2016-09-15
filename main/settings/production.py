from demo_mongo.settings.base import *
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # 'default': {
    #     'ENGINE': '<backend_engine_name>',
    #     'NAME': '<db_name>',
    #     'USER': '<db_user>',
    #     'PASSWORD': '<password>',
    #     'HOST': '<host>',
    #     'PORT': '<port>',
    # }
}


# AWS Settings
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxx'
AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


# Email server settings
# ABSOLUTELY REMOVE THE DUMMY EMAIL SERVER IN PRODUCTION!!!
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.xx-xxxx-x.amazonaws.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = AWS_ACCESS_KEY_ID
EMAIL_HOST_PASSWORD = AWS_SECRET_ACCESS_KEY
