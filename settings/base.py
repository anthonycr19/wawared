# coding=utf-8
import sys
from os import environ, path

import djcelery
from django.conf import global_settings
from django.core.exceptions import ImproperlyConfigured


def get_env(name):
    try:
        value = environ[name]
        return value
    except KeyError:
        raise ImproperlyConfigured(name)


BASE_DIR = path.dirname(path.dirname(__file__))

sys.path.append(path.join(BASE_DIR, 'apps'))

AUTH_USER_MODEL = 'perfiles.User'

SESSION_COOKIE_AGE = 360 * 60

SESSION_SECURITY_WARN_AFTER = 200 * 30

SESSION_SECURITY_EXPIRE_AFTER = 180 * 60

# MinsaLogin
APP_IDENTIFIER = get_env('APP_IDENTIFIER')

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_DOMAIN = get_env('LOGIN_DOMAIN')

URL_LOGIN_SERVER = get_env('URL_LOGIN_SERVER')

LOGIN_URL = '/ingresar/'
#

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('admin', 'admin@wawared.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env('DB_NAME'),
        'USER': get_env('DB_USER'),
        'PASSWORD': get_env('DB_PASSWORD'),
        'HOST': get_env('DB_HOST'),
        'PORT': get_env('DB_PORT'),
    }
}

PAGE_SIZE = 15

ALLOWED_HOSTS = ['*']

TIME_ZONE = 'America/Lima'

LANGUAGE_CODE = 'es-PE'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = False

MEDIA_ROOT = path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = path.join(BASE_DIR, 'static')

STATIC_URL = environ.get('STATIC_URL', '/static/')

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = get_env('SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'popup_messages.middleware.CheckMessagesMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
)

ROOT_URLCONF = 'wawared.urls'

WSGI_APPLICATION = 'wawared.wsgi.application'

TEMPLATE_DIRS = (
    path.join(BASE_DIR, 'apps/dashboard/templates'),
    path.join(BASE_DIR, 'apps/pacientes/templates'),
    path.join(BASE_DIR, 'apps/embarazos/templates'),
    path.join(BASE_DIR, 'apps/controles/templates'),
    path.join(BASE_DIR, 'apps/citas/templates'),
    path.join(BASE_DIR, 'apps/perfiles/templates'),
    path.join(BASE_DIR, 'apps/popup_messages/templates'),
    path.join(BASE_DIR, 'apps/partos/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'common.context_processors.boolean_variables',
    'common.context_processors.capacitacion',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'minsalogin',
    'flat',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'common',
    'gestantes',
    'ubigeo',
    'cie',
    'establecimientos',
    'perfiles',
    'pacientes',
    'embarazos',
    'controles',
    'dashboard',
    'citas',
    'indicadores',
    'api',
    'popup_messages',
    'gunicorn',
    'djcelery',
    'easy_thumbnails',
    'session_security',
    'import_export',
    'mensajes',
    'cpt',
    'partos',
    'firma',
    'puerperio'
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

DOMAIN = get_env('DOMAIN')

# Email credentials
MAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True

EMAIL_HOST = get_env('EMAIL_HOST')

EMAIL_HOST_USER = get_env('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD')

EMAIL_PORT = get_env('EMAIL_HOST_PORT')

API_SYNCHRONIZE_MIRTH = get_env('API_SYNCHRONIZE_MIRTH')

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

"""
# Cache en disco
CACHE_BACKEND = 'file:///home/mario21ic/repo/app_wawared/cache'
CACHE_MIDDLEWARE_SECONDS = 5
CACHE_MIDDLEWARE_KEY_PREFIX = 'xD'
"""

LOGIN_REDIRECT_URL = '/hce/reportes/'

djcelery.setup_loader()

CELERY_TIMEZONE = 'America/Lima'

BROKER_URL = get_env('BROKER_URL')

CELERY_RESULT_BACKEND = get_env('BROKER_RESULT_BACKEND')

# jasper reports
JASPER_URL = get_env('JASPER_URL')

JASPER_USER = get_env('JASPER_USER')

JASPER_PASSWORD = get_env('JASPER_PASSWORD')

JASPER_PATH = get_env('JASPER_PATH')

CITA_API_URL = get_env('CITA_API_URL')

MPI_API_URL = get_env('MPI_API_HOST')

MPI_API_TOKEN = get_env('MPI_API_TOKEN')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

CAPACITACION = eval(environ.get('CAPACITACION', 'False'))

EXSER_HOST = environ.get('EXSER_HOST')
EXSER_TOKEN = environ.get('EXSER_TOKEN')
CLAVE_SIS_TRAMA = get_env('CLAVE_SIS_TRAMA')
FIRMA_JS_URL = get_env('FIRMA_JS_URL')
