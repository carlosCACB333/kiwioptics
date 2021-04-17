from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['kiwioptics.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
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
STATICFILES_DIRS = (
    BASE_DIR.joinpath('static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
