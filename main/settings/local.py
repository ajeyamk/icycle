from main.settings.base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']


INSTALLED_APPS += (
    'debug_toolbar',
    'debug_panel',
    'django_extensions',
)


MIDDLEWARE_CLASSES += (
    'debug_panel.middleware.DebugPanelMiddleware',
)

DEBUG_TOOLBAR_MONGO_STACKTRACES = True


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
