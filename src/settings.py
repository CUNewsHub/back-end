"""
Django settings for newshub project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from secret_data import *
from pipeline import SOCIAL_AUTH_PIPELINE

import os
import secret_data

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


SOCIAL_AUTH_PIPELINE = SOCIAL_AUTH_PIPELINE
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_SLUGIFY_USERNAMES = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGS_FILE = 'tags_categories.json'
FEEDBACK_FILE = 'feedback_options.json'
COLLEGES_SUBJECTS_FILE = 'colleges_subjects.json'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the set key used in production secret!
SECRET_KEY = secret_data.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = secret_data.DEBUG

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',

    # 3rd party apps
    'tinymce',
    'redactor',
    'fontawesome',
    'widget_tweaks',
    'django_select2',
    'sorl.thumbnail',

    'newshub',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/login/'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

LOGIN_URL = '/login/'

ROOT_URLCONF = 'src.urls'

if DEBUG:
    if secret_data.DEVELOPMENT:
        FRONTEND_BASE = os.path.abspath(os.path.join(
            BASE_DIR, '..', 'front-end'))

        STATICFILES_DIRS = (
            os.path.abspath(os.path.join(FRONTEND_BASE, 'static')),
        )

        STATIC_URL = '/static/'
        MEDIA_URL = '/media/'
        STATIC_ROOT = os.path.abspath(os.path.join(
            FRONTEND_BASE, 'static-only'))
        MEDIA_ROOT = os.path.abspath(os.path.join(FRONTEND_BASE, 'media'))

    else:
        FRONTEND_BASE = '/home/newshub/webapps/newshub_static/current'

        STATIC_URL = '/static/current/static/'
        MEDIA_URL = '/static/current/media/'
        MEDIA_ROOT = '/home/newshub/webapps/newshub_static/shared/media'
        STATIC_ROOT = os.path.abspath(os.path.join(FRONTEND_BASE, 'static'))


# TINYMCE CONFIG
TINYMCE_JS_URL = os.path.join(STATIC_URL, "tiny_mce/tiny_mce.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, "tiny_mce")
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'theme_advanced_resizing': 'true',
    'width': '600'
}


TEMPLATE_D = os.path.abspath(os.path.join(FRONTEND_BASE, 'templates'))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_D],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.static',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'src.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secret_data.MYSQL_DB,
        'USER': secret_data.MYSQL_USER,
        'PASSWORD': secret_data.MYSQL_PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
