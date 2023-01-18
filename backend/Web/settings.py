import os
import sys
import datetime
import posixpath
from .constant import *
from pathlib import Path

sys.path.insert(0, 'apps')


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-hc)9+$0zv1558gns6m4gl+#&298i&n-_x7cv*0pvtbik+q=l!)'


ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'user',
    'role'
]

if DEBUG:
    INSTALLED_APPS += [
        'drf_yasg',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Web.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DATABASE,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTH_USER_MODEL='user.User'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# JWT
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':  'utils.drf.page.APIPage',
    'DEFAULT_FILTER_BACKENDS': (
        'utils.drf.filters.DateTimeFilterSet',
        'django_filters.rest_framework.DjangoFilterBackend'
    ),
    'EXCEPTION_HANDLER': 'utils.drf.handle_exception.exception_handler',
}
JWT_AGE = SESSION_COOKIE_AGE / 60 / 60
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=JWT_AGE),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=JWT_AGE),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'user.utils.jwt_response_payload_handler',
    'JWT_AUTH_COOKIE': 'JWT'
}

APP_MIGRATIONS_PATH = 'migrations'
MIGRATION_MODULES = {}

for i in INSTALLED_APPS:
    label = i.split('.')[-1]
    if label not in os.listdir(APP_MIGRATIONS_PATH):
        os.mkdir(posixpath.join(APP_MIGRATIONS_PATH, label))
        init_file = open(posixpath.join(APP_MIGRATIONS_PATH, label, '__init__.py'), 'w')
        init_file.close()
    MIGRATION_MODULES[label] = '.'.join([APP_MIGRATIONS_PATH, label])