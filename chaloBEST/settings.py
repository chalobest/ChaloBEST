# Django settings for chaloBEST project.
import os
from os.path import join

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(__file__)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

SITENAME = "ChaloBEST"

LOCAL_DEVELOPMENT = True
JSON_DEBUG = True

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': join(PROJECT_ROOT, 'chalobest.db'),                      # Or path to database file if using sqlite3.
        'USER': 'sanj',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = join(PROJECT_ROOT, 'static')
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_ROOT, 'mumbai/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
try:
    SECRET_KEY
except NameError:
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            SECRET_KEY = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)



# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'userena.middleware.UserenaLocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'minidetector.Middleware',
)

ROOT_URLCONF = 'chaloBEST.urls'

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),    
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.gis',
    'django_extensions',
    'debug_toolbar',
    'mumbai',
    'mumbaitrains',
    # 'django.contrib.admindocs',
   # 'socialregistration',
    #'socialregistration.contrib.openid',
    #'socialregistration.contrib.facebook',
    'emailconfirmation',
   # 'uni_form',
   # 'allauth',
   # 'allauth.account',
   # 'allauth.socialaccount',
   # 'allauth.socialaccount.providers.twitter',
   # 'allauth.socialaccount.providers.openid',
   # 'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.google',
    'users',
    'profiles',
    'userena',
    'guardian',
    'easy_thumbnails',
    'south',
    'django_extensions',
    'userena.contrib.umessages',

)
TEMPLATE_CONTEXT_PROCESSORS = (
   'django.core.context_processors.request',
   'django.contrib.auth.context_processors.auth',
   #"allauth.context_processors.allauth",
   #"allauth.account.context_processors.account",
   "django.contrib.messages.context_processors.messages"

)
AUTHENTICATION_BACKENDS = (
#	"allauth.account.auth_backends.AuthenticationBackend",
	"userena.backends.UserenaAuthenticationBackend",
        "guardian.backends.ObjectPermissionBackend",
        "django.contrib.auth.backends.ModelBackend",

)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='smtp.gmail.com'
EMAIL_HOST_USER = 'abc@abc.com'
EMAIL_HOST_PASSWORD ='somepassword'
EMAIL_PORT =587
EMAIL_USE_TLS =True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER
AUTH_PROFILE_MODULE = "users.UserProfile"
#AUTH_PROFILE_MODULE = 'profiles.Profile'
LOGIN_REDIRECT_URL ='/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
#LOGIN_REDIRECT_URL = '/profiles/profile/'
#USERENA_DISABLE_PROFILE_LIST = False
USERENA_DISABLE_PROFILE_LIST = True
USERENA_MUGSHOT_SIZE = 140
USERENA_MUGSHOT_GRAVATAR=True
USERENA_USE_MESSAGES = True
USERENA_MUGSHOT_DEFAULT='monsterid'
ANONYMOUS_USER_ID = -1
	

BING_API_KEY = 'please over-ride this in local_settings.py'

try:
    from local_settings import *
except:
    pass
