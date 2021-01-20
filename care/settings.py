# encoding: utf-8
# Django settings for Care project.

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

INSTALLED_APPS = (
    'bootstrap3',
    'bootstrap3_datetime',
    'bootstrap_pagination',
    'registration',  #django-registration-redux
    'django_cron',  # for job scheduling (for example, sending mails)
    'recurrence',  # recurrent event field
    'care',
    'care.base',
    'care.userprofile',
    'care.groupaccount',
    'care.transaction',
    'care.groupaccountinvite',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
)

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'care.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'care.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'care/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False


#########
# LOGIN #
#########

# redirect here when used is not logged in and logged in is required
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

##############################
# django-dual-authentication #
##############################

# django-dual-authentication settings
AUTHENTICATION_BACKENDS = ['django-dual-authentication.backends.DualAuthentication']
# You can authenticate your users by 'username', 'email', 'both'. Default: 'both'.
AUTHENTICATION_METHOD = 'both'

##############################
# django-cron #
##############################

CRON_CLASSES = [
    'care.base.cronjobs.DailyBackup',
    'care.base.cronjobs.DailyEmails',
    'care.base.cronjobs.WeeklyEmails',
    'care.base.cronjobs.MonthlyEmails',
    'care.base.cronjobs.CreateRecurrentShareOccurrence',
    # 'care.base.cronjobs.TestEmails',
]

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
from care.local_settings import *


###########
# LOGGING #
###########

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename':os.path.join(BASE_DIR, 'care.log'),
            'formatter':'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['mail_admins'],
            'level':'ERROR',
            'propagate':True,
        },
        'django': {
            'handlers':['file'],
            'propagate':True,
            'level':'ERROR',
        },
        '': {
            'handlers':['file'],
            'level':'DEBUG',
        },
    },
    'formatters': {
        'verbose': {
            'format':"[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s - %(funcName)20s()]: %(message)s",
            'datefmt':"%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format':'%(levelname)s %(message)s'
        },
    },
}


##############
# Bootstrap3 #
##############

BOOTSTRAP3 = {
    'base_url': STATIC_URL + 'bootstrap/',  #'//netdna.bootstrapcdn.com/bootstrap/3.0.3/'
    'css_url': STATIC_URL + 'bootstrap/css/bootstrap_flatly.min.css',
    'theme_url': None,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-4',
}
