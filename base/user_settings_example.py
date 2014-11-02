# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

ADMINS = (
    ('Your Name', 'email address'),
)

APP_DIR = '/home/bart/dev/care/'

ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = '/home/bartromgens/webapps/carestatic/'
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = 'http://www.computerautomatedremoteexchange.com/carestatic/'
STATIC_URL = APP_DIR + 'static/'

# password used for outgoing smtp
MAILPASSWORD = ''
# username used for outgoing smtp
MAILUSERNAME = ''
# SMTP url and port
MAILSMTPSERVER = 'smtp.domain.com:587'