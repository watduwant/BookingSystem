"""
Django settings for starter_template project.

Generated by 'django-admin startproject' using Django 2.1.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from decouple import config, Csv
import django_heroku
from django.contrib.messages import constants as messages
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Email-host config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

AUTH_USER_MODEL = 'users_auth_api.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Third Party apps
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'fcm_django',
    'storages',
    'widget_tweaks',
    'multiselectfield',

    # Pre existing
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'allauth.socialaccount.providers.google',

    #Local apps
    'users_auth_api',
    'notificationsapi',
    'pathological_test',
    'api',
    'store',
    'customer',
]



# Application definition

SITE_ID = 1

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAPdPqtII:APA91bHs4uMdnG8Ml6yT3gco5XbfIR-LXR6YEyLKOgYrGJTzIPryxiJBlwAtJfHX5Dsh8F_09N5_lOI3kacZV4EQxyMOE9k862GlLEG6YD51eUOae6DB_fl7LJhMNVpllEVrAVXAZgv1",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": False,
 }


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:7600',
    'http://127.0.0.1:9000',
    'http://localhost:4200',
    'http://localhost:8101',
    'http://localhost:8102',
    'http://localhost:8103',
    'http://localhost:8104',
    'http://localhost:8105',
    'http://localhost:8109',
    'http://localhost:8100',
    'http://localhost:8300',
    'http://103.68.10.122',
    'http://10.0.2.2:8105',
    'http://10.0.2.2:8105',
    'http://10.0.2.2:8103',
    'http://10.0.2.2:8109',
    'http://69.0.3497.100',
    'http://localhost',
    'http://127.0.0.1:8101',


    # existing code
    "http://localhost:3000",
]


ROOT_URLCONF = 'starter_template.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


WSGI_APPLICATION = 'starter_template.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG:
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
    }
else:
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
        # 'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination'
    }

JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'users_auth_api.custom_jwt.jwt_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users_auth_api.custom_jwt.jwt_response_payload_handler',
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_VERIFY_EXPIRATION': False
}

REST_USE_JWT = True


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# if DEBUG:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# else:
#     DATABASES = {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': config('DB_NAME'),
#                 'USER': config('DB_USER'),
#                 'PASSWORD': config('DB_PASSWORD'),
#                 'HOST': config('DB_HOST'),
#                 'PORT': config('DB_PORT'),
#                 'OPTIONS': {
#                     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#                     'charset': 'utf8mb4',
#                 }
#             }
#         }



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False



#AWS S3 Settings

# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_DEFAULT_ACL = None

# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }

# AWS_LOCATION = 'static'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

# DEFAULT_FILE_STORAGE = 'mybackend.storage_backends.MediaStorage'


# existing code


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# SITE_ID = 2
LOGIN_REDIRECT_URL = "/"

# # Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '539609373036-aucng4mt95c0d2gu693r3m8ebqi0fhl3.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = os.path.join(BASE_DIR,'static_root')


MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Activate Django-Heroku.
django_heroku.settings(locals())