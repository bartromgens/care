# user settings, included in settings.py

DEBUG = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'm_8q98w3($Ep1&g04+oroUzppx1IME1.>?R~RpXLs(&<+Z(p|5'

ADMINS = (
    ('Your Name', 'email address'),
)

APP_DIR = '/home/bart/dev/care-dev/'

ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Amsterdam'

#STATIC_ROOT = '/home/username/webapps/carestatic/'
STATIC_ROOT = ''

# URL prefix for static files.
#STATIC_URL = 'http://www.computerautomatedremoteexchange.com/carestatic/'
STATIC_URL = APP_DIR + 'static/'

REGISTRATION_OPEN = True

# email server settings for outgoing mails
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.domain.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

DEFAULT_FROM_EMAIL = 'info@domain.com'
SERVER_EMAIL = 'info@domain.com'
