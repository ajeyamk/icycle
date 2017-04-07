from main.settings.base import *
# import elasticsearch

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['*']


STATIC_ROOT = 'static/'


# Haystack connection
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'URL': '<host_url>',
#         'INDEX_NAME': '<index_name>',
#         'KWARGS': {
#             'use_ssl': True,
#             'verify_certs': True,
#             'connection_class': elasticsearch.RequestsHttpConnection,
#         },
#     },
# }


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


# Partner details
PARTNER_KEYS = {
    'shopify': {
        'api_key': '4c29c1a4d513e3b8d4bc5328b9b0bfc4',
        'shared_secret': 'aa0755c246fc6f7a4dcceb0c61085313'
    }
}


# AWS Settings
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxx'
AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


# Shopify settings
SHOPIFY_KEY = 'f4906358742dff611ae95b4e1631800e'
SHOPIFY_PASSWORD = 'a895f474d28d202e5d4a977c8357106d'
SHOPIFY_PRODUCTION_USED = True
SHOPIFY_PRODUCTION_DOMAIN = 'chefd.myshopify.com'
SHOPIFY_TEST_DOMAIN = 'chefd-staging.myshopify.com'


# API Token
API_TOKEN = 'Iry0dGh4VDDc1uPLJWmZfHMQwVo5zWp4'


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
