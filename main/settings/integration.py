from main.settings.base import *


DEBUG = False


ALLOWED_HOSTS = ['*']


STATIC_ROOT = 'static/'


# Haystack connection
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
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


# Shopify settings
SHOPIFY_KEY = '2269a3b61aa4965aa405d57cb4d26568'
SHOPIFY_PASSWORD = '6c731bcb24012ad76d8ddc5602dadb71'
SHOPIFY_PRODUCTION_USED = False
SHOPIFY_PRODUCTION_DOMAIN = 'chefd.myshopify.com'
SHOPIFY_TEST_DOMAIN = 'chefd-staging.myshopify.com'


# API Token
API_TOKEN = 'eWQcFm9lT0zz9dMzWiaIZLFh4HDIpPsr'


# Email server settings
# ABSOLUTELY REMOVE THE DUMMY EMAIL SERVER IN PRODUCTION!!!
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'AKIAIGMGOKA7WFT7UBMQ'
EMAIL_HOST_PASSWORD = 'AuOSUNAbvq8IhSUPcPmQiyUEUk86Xtmq+hadQEpZQnWn'
EMAIL_FROM = 'eshan@scientist-tech.com'
