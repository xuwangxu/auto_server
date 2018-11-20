"""
Django settings for auto_server project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*lc9gx5pq^5605lz)=f9@--exy0tc7_8qzza@g_1rid0y$#)+6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.56.11',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'stark.apps.StarkConfig',
    'api.apps.ApiConfig',
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

ROOT_URLCONF = 'auto_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'auto_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test3',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'192.168.56.11',
        'PORT':'3306'

    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


######################自定义的配置##############
URL_AUTH_KEY = 'kgjghgh857538yy'
PRIV_KEY = b'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDWHdJQkFBS0JnUUM1TDBKYm0zRDJUR0R0bzFrODVzTmdoVmdEWGtyR29SU2VQc2srNTdLK1hEVWJNSTZZClBVa2F1VGxvbkFSUjBrZXFSb0hCblQrSEhSUHA0VENETDE5SXlhMU4yTXRyWnc3ZnJoZUphLzFnc2lZV2UwREEKd0MybS9hS1FQY2dVKytRWVhNeEpxeVZXZTgzQnptMlRyYzhxVkJoakJRTGFFWityS3dtVGxmSHROUUlEQVFBQgpBb0dBUjZUMERGTUFDaG9VcWZ1M2k2dFB6V2pwV3l4QXk4WUlId3oxZVFQVkVIYkdDUVhwTlJjSTBIRDJ0L1VjCmFyZHJDSUtNc3VadWJJeWdacXk3ZTFhZHZhQUZFbXJhbWVoK0krbDMzS0MzQk5oUzN5Zi9UNGEyZVJON0xsSnAKMUR5ZWU2VEpQSVp2Y0IxSm5GUFA2bERwb3BRRHZxWjVtYkhyUG9GR2FNYi96WUVDUlFDNWNYNkZWdlpPOGJsVgpJNm4vQWlpaGxUcWI2MHN2Mm9FNkVDay9KaDVPWU9ITkhkZ0ZZMG9YS29RcTJySlErS0gzeTc0Rk1kY0Z3eEZLCmgva1h5UnF3VVdhbEZRSTlBUCtra0c1TEwxVkJFU3hpUXJGdDM2S2svTUJvTDRRb2hrSkR1U1dWN05rL1RGYnEKRGZPZEMwTy9WWVc4WjYvRG9wc3VyTzNObXNTWHE1QnZvUUpFZGREaVpncVM0Q0w0OFZ1QU5IQ0ZxZXJxV29jSgp0TFJvNTUrKzVNenQ4alBoSVhUMWVxN1RNcGFqYzZxUUladGxJODZBd2tJZzd4czRrQmFGTGhScGJWMjZEZVVDClBGVnFIWnZNWVNkQ0UwUGFIT0I5anBBZ1FoYmplS1RXaVcxUWhXY0tmZFZrY2RSRVpaNzA1Tk9nOVNrMjl3bmgKK3MyUXZkVENzcWhtNkxyY29RSkVkR2gvU3hJbmU4RDlwMWR5QmxlN0U5MnBReHdWVlRxWXAxdHY4RkpvMTc3Ywp3c2JRQmVyZXFlMFl4V2p4TmVSSE5XTjFDSDZQN1VYSkF4bVM5TTROTEhKSTBGTT0KLS0tLS1FTkQgUlNBIFBSSVZBVEUgS0VZLS0tLS0K'

