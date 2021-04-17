from .base import *
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ['https://kiwioptics.herokuapp.com/']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PROD_DB_NAME'),
        'USER': config('PROD_DB_USER'),
        'PASSWORD': config('PROD_DB_PASSWORD'),
        'HOST': config('PROD_DB_HOST'),
        'PORT': config('PROD_DB_PORT'),
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.RequestMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
STATIC_URL = '/static/'
