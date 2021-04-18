from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['*']

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
AWS_STORAGE_BUCKET_NAME = 'kiwioptics'
AWS_ACCESS_KEY_ID = 'AKIASLIJ76VBKZERZK47'
AWS_SECRET_ACCESS_KEY = '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'
S3_BUCKET_NAME = 'kiwioptics'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
