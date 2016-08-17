from demo_sql.settings.base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']


INSTALLED_APPS += (
    'debug_toolbar',
    'debug_panel',
    'django_extensions',
)


MIDDLEWARE_CLASSES += [
    'debug_panel.middleware.DebugPanelMiddleware',
]


# Haystack connections


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

}


# GRAPH_MODELS = {
#     'all_applications': True,
#     'group_models': True,
# }
