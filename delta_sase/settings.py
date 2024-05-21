# Django settings for delta_sase project.
import sys
import os
from dotenv import load_dotenv
from django.conf import settings

MACHINE_ID = '1234'
DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_DIR = os.path.join(BASE_DIR, os.pardir)

TENANT_APPS_DIR = os.path.join(PROJECT_DIR, os.pardir)
sys.path.insert(0, TENANT_APPS_DIR)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django_tenants.postgresql_backend',  # Add 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'delta98',
#         'USER': 'admin',
#         'PASSWORD': 'admin',
#         'HOST': '192.168.172.71',
#         'PORT': '5433',
#     }
# }
load_dotenv() 

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',  # Add 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('DATABASE_DB', 'postgres'),
        'USER': os.environ.get('DATABASE_USER', 'admin'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'admin'),
        'HOST': os.environ.get('DATABASE_HOST', '10.1.1.21'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'as-%*_93v=r5*p_7cu8-%o6b&x^g+q$#*e*fl)k)x0-t=%q0qa'

# List of callables that know how to import templates from various sources.

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MIDDLEWARE = [
    'django_tenants.middleware.TenantSubfolderMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'tenants_app.middleware.JWTAuthenticationMiddleware',
    'tenants_app.middleware.ExceptionHandlingMiddleware',
    'tenants_app.middleware.LoggingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')

        ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'delta_sase.context_processors.settings',
            ],
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ),

        },
    },
]
ROOT_URLCONF = 'delta_sase.urls_tenants'
PUBLIC_SCHEMA_URLCONF = 'delta_sase.urls_public'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'delta_sase.wsgi.application'

SHARED_APPS = (
    'django_tenants',  # mandatory
    'tenants_app',  # you must list the app where your tenant model resides in
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'rest_framework',
    'celery',
    'polymorphic',
    # 'staging_app',
    # 'tenants_app.apps.TenantsAppConfig',
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'base',
    'resources_app',
    'settings_app',
    'config',
    # 'sites_app',
    # 'devices_app',
    # 'interfaces_app',
    # 'routes_app',
    # 'templates_app',
    # 'profiles_app',
    # 'security_policies_app',
    # 'routing_policies_app',
    # 'qos_policies_app',
    # 'nat_policies_app',
    # 'events_app',
    # 'remote_access_app',
    # 'general_settings_app',
    # 'auth_settings_app',
    # 'config_manager_app',
    # 'monitor_app',
    # 'objects_app',
    # 'custom_vpn_app',
    # 'dashboard_app',
    # 'cli_app',
    # 'network_app',
    # 'vpn_app',
    # 'auth_policies_app',
)

TENANT_MODEL = "tenants_app.Tenant"  # app.Model

TENANT_DOMAIN_MODEL = "tenants_app.Domain"  # app.Model

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

AUTO_DROP_SCHEMA= True

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_SUBFOLDER_PREFIX = "tenants"

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'debug.log'),
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins', 'file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         '': {  # The empty string catches everything not specified above
#             'handlers': ['file'],
#             'level': 'INFO',
#         },
#     }
# }
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'tenant_context': {
            '()': 'django_tenants.log.TenantContextFilter'
        },
    },
    'formatters': {
        'tenant_context': {
            'format': '[%(schema_name)s:%(domain_url)s] '
            '%(levelname)-7s %(asctime)s %(message)s',
        },
        'detailed': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'tenant_context'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'debug.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'detailed',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true', 'tenant_context'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {  # The empty string catches everything not specified above
            'handlers': ['file', 'console'],
            'level': 'INFO',  # Or use DEBUG to see more details during development
            'propagate': False,
        },
    }
}
# SHared Schemas between all tenants 
PG_EXTRA_SEARCH_PATHS = ['extensions', 'delta']
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True


DEFAULT_FILE_STORAGE = "django_tenants.files.storage.TenantFileSystemStorage"
MULTITENANT_RELATIVE_MEDIA_ROOT = "uploaded_files"
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# CELERY_BROKER_URL = 'redis://localhost:6379/0'


CELERY_BROKER_URL = os.environ.get('CELERY_URL', 'redis://localhost:6379/0'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'delta_sase')

#Keycloak and JWT token Environment variables
DEFAULT_PUB_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAly2mtHbJdSB4umYogMBO
obeYjEK6yq4jQzkFfTVYH1qKcL/4Qw/nLsBkAXL3CCb7eYKq4vqFrHE3g/KKbYsB
gkRePAZDensddFBDviFOxAyRn7WuH3d15KCm9SvyiWIC9JQlJJSk/1oHD0H/WP8S
RmPXZ4dL3tCu6sTT6VcLXOPdSR5N22tuUSlY2cMLYzVvDacOhvrvGZIN5ALPfRqv
NtCTH2dXznNt+9ZHwJE3O3tlTrp1Pl2QBkb8xMv87sMYGUDLFLbAxhJEmXhenlGP
vMzYVWcSMvj5JPpez6FNXlBb7MegCVLl+pPBlryHB2H9JrELK4qG3V0QhnlHXr5V
/QIDAQAB
-----END PUBLIC KEY-----
"""
KEYCLOAK_PUBLIC_KEY = os.getenv('KEYCLOAK_PUBLIC_KEY', DEFAULT_PUB_KEY)
JWT_AUDIENCE = os.getenv('JWT_AUDIENCE', 'default-audience-if-not-set')
