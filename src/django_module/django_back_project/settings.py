import os

import dj_database_url
import dotenv

from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load env variables from file
dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    'x%#3&%giwv8f0+%r946en7z&d@9*rc$sl0qoql56xr%bh^w2mj',
)

if os.environ.get('DJANGO_DEBUG', default=False) in ['True', 'true', '1', True]:
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ["*", ]  # since Telegram uses a lot of IPs for webhooks

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    # 'django_celery_beat',

    # local apps
    'django_module.apps.vpn.apps.VpnConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'django_module.django_back_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'django_module.django_back_project.wsgi.application'
ASGI_APPLICATION = 'django_module.django_back_project.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600),
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')


def _get_env_variable(var_name: str, default=None):
    """Get the environment variable or raise an error."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        raise ImproperlyConfigured(f"Set the {var_name} environment variable")


# -----> VPN Service
VPN_SERVICE_URL = _get_env_variable("VPN_SERVICE_URL")
VPN_SERVICE_SECRET_KEY = _get_env_variable("VPN_SERVICE_SECRET_KEY")

# -----> TELEGRAM
TELEGRAM_TOKEN = _get_env_variable("TELEGRAM_TOKEN")
TELEGRAM_LOGS_CHAT_ID = os.getenv("TELEGRAM_LOGS_CHAT_ID", None)

# -----> ENV variable
env_values = ('local', 'test', 'prod')
ENV = _get_env_variable("ENV")
if ENV not in env_values:
    raise ImproperlyConfigured(f"ENV variable has invalid value. Choose from {env_values}.")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s',
            'style': '%',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'level': os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            'handlers': ['console'],
            'propagate': False,
        },
        'tg_bot': {
            'level': os.getenv("APP_LOG_LEVEL", "DEBUG"),
            'handlers': ['console'],
            'propagate': False,
        },
    },
}


# -----> SENTRY
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# from sentry_sdk.integrations.celery import CeleryIntegration
# from sentry_sdk.integrations.redis import RedisIntegration

# sentry_sdk.init(
#     dsn="INPUT ...ingest.sentry.io/ LINK",
#     integrations=[
#         DjangoIntegration(),
#         CeleryIntegration(),
#         RedisIntegration(),
#     ],
#     traces_sample_rate=0.1,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )
