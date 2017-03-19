import os
import sys


TEST = 'test' in sys.argv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(*a):
    return os.path.join(BASE_DIR, *a)


# This trick allows to import apps without that prefixes
sys.path.insert(0, path('apps'))
sys.path.insert(0, path('lib'))
sys.path.insert(1, path('.'))


ROOT_URLCONF = 'service_plus.urls'
WSGI_APPLICATION = 'service_plus.wsgi.application'

ALLOWED_HOSTS = ['www.site.ru']

ADMINS = [
    ('Pavel Alekin', 'minidron@yandex.ru')
]

INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.gis',
    'django.contrib.staticfiles',
    'django_extensions',
    'djangobower',
    'pipeline',
    'reversion',
    'rest_framework',
    'adminsortable2',
    'lib',
    'crm',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGIN_URL = '/admin/login/'
# -----------------------------------------------------------------------------


# TEMPLATES -------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [path('templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# -----------------------------------------------------------------------------


# INTERNATIONALIZATION --------------------------------------------------------
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# -----------------------------------------------------------------------------


# STATIC AND MEDIA FILES ------------------------------------------------------
STATICFILES_DIRS = [
    path('static'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

STATIC_URL = '/static/'
STATIC_ROOT = path('../../static')

MEDIA_URL = '/media/'
MEDIA_ROOT = path('../media')
# -----------------------------------------------------------------------------


# BOWER SETTINGS --------------------------------------------------------------
STATICFILES_FINDERS += (
    'djangobower.finders.BowerFinder',
)

BOWER_COMPONENTS_ROOT = path('static')

BOWER_INSTALLED_APPS = (
    'backbone#1.3',
    'font-awesome#4.7',
    'include-media#1.4',
    'marionette#3.2.0',
    'normalize-scss#3',
    'underscore#1.8',
)

# './manage.py bower_install' - install bower apps
# -----------------------------------------------------------------------------


# REST FRAMEWORK SETTINGS -----------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
# -----------------------------------------------------------------------------


# PIPELINE SETTINGS -----------------------------------------------------------
STATICFILES_FINDERS += (
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'CSS_COMPRESSOR': None,
    'DISABLE_WRAPPER': True,
    'JS_COMPRESSOR': None,
    'SASS_ARGUMENTS': '--include-path %s' % path('static'),
    'SASS_BINARY': 'sassc',
    'COFFEE_SCRIPT_ARGUMENTS': '-b',
    'STYLESHEETS': {
        'fontawesome': {
            'source_filenames': (
                'crm/admin/scss/fontawesome.scss',
            ),
            'output_filename': 'admin/css/fontawesome.css',
        },
    },
    'JAVASCRIPT': {
        'marionette': {
            'source_filenames': (
                'bower_components/underscore/underscore-min.js',
                'bower_components/backbone/backbone-min.js',
                'bower_components/backbone.radio/build/backbone.radio.min.js',
                'bower_components/backbone.marionette/lib/backbone.marionette.min.js',  # NOQA
            ),
            'output_filename': 'admin/js/marionette.js',
        },
        'jobs': {
            'source_filenames': (
                'crm/admin/coffee/jobs/app.coffee',
                'crm/admin/coffee/jobs/models.coffee',
                'crm/admin/coffee/jobs/views.coffee',
                'crm/admin/coffee/jobs/start.coffee',
            ),
            'output_filename': 'admin/js/jobs.js',
        },
        'spare_part': {
            'source_filenames': (
                'crm/admin/coffee/spare_part/app.coffee',
                'crm/admin/coffee/spare_part/models.coffee',
                'crm/admin/coffee/spare_part/views.coffee',
                'crm/admin/coffee/spare_part/start.coffee',
            ),
            'output_filename': 'admin/js/spare_part.js',
        },
    },
    'COMPILERS': (
        'pipeline.compilers.coffee.CoffeeScriptCompiler',
        'pipeline.compilers.sass.SASSCompiler',
    ),
}
# -----------------------------------------------------------------------------


# IPYTHON NOTEBOOK ------------------------------------------------------------
IPYTHON_ARGUMENTS = [
    '--ext', 'django_extensions.management.notebook_extension',
]

NOTEBOOK_ARGUMENTS = [
    '--ip=0.0.0.0',
    '--no-browser',
]
# -----------------------------------------------------------------------------
