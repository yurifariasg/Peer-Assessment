"""
Django settings for peerassessment project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(bmiu8_&2m*h@vcdp$c_hwne(ni=f660$*_2@4cenohia8mu7%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HEROKU = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Peer-Assessment Specific Options

JOB_UPDATER_TIMER = 1
if HEROKU:
    JOB_UPDATER_TIMER = 10

FORCE_5_STUDENTS_MINIMUM_ALLOCATION = False


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # We disabled the Csrf Middleware to easily use AJAX Requests
    # This shall be enabled later on to avoid Cross-site request forgery
    # This has been registered as Issue #8
    # https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
    #'django.middleware.csrf.CsrfViewMiddleware',
)

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/"
LOGOUT_URL = "/logout"

ROOT_URLCONF = 'peerassessment.urls'

WSGI_APPLICATION = 'peerassessment.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'app.backends.EmailAuthBackend',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# The Date format to be shown on Templates (when not overriden)
DATETIME_FORMAT = "j \d\e N \d\e Y G\h i\m" # "G:i - j/n \d\e Y"
# DATE_FORMAT = "N Y"

# Logging configuration
# https://docs.djangoproject.com/en/dev/topics/logging/
# This is a simple Debug logging configuration
# It shall be used like: logger.debug(debug info)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class':'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'filters': [],
            'propagate': True,
            'level': 'DEBUG',
        },
        'apscheduler.scheduler': {
            'handlers': ['console'],
            'filters': [],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


if not HEROKU:

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/
    STATIC_ROOT = os.path.join(BASE_DIR,'static')
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(BASE_DIR, 'staticfiles'),
    )

else:

    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    # Static asset configuration
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, '../app/static'),
    )
