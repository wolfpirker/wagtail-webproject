from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd6$x07i%oo6af$d0*ug&_r7=x2c70x3(qb98!7e_$3g1v17+&^'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['127.0.0.1', 'localhost'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#SECURE_HSTS_SECONDS=0
#SECURE_HSTS_INCLUDE_SUBDOMAINS=True
#SECURE_SSL_REDIRECT=False
#SESSION_COOKIE_SECURE=False
#CSRF_COOKIE_SECURE=False
#SECURE_HSTS_PRELOAD=False

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "./cache"
        }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './messages.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
