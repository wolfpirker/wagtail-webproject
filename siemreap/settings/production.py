from __future__ import absolute_import, unicode_literals
# Note: __future__ always imported first!

from .base import *
import dj_database_url
import os

env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']

# NOTE: switch to FALSE later!!! before making this webpage public!
DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# useful command for deploying:
# ./manage.py check --deploy


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
	'compressor.filters.c#ss_default.CssAbsoluteFilter',
	'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-PRoto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers

ALLOWED_HOSTS = ['tourguidecambodia.herokuapp.com', '127.0.0.1', 'localhost']

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

#CACHES = {
#    "default": {
#        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
#        "LOCATION": "./cache"
#        }
#}

try:
    from .local import *
except ImportError:
    pass
