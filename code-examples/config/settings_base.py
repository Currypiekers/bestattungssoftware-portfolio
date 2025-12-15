"""
Django base settings file for dev and prod. ////
"""
from datetime import timedelta
import os
from pathlib import Path
from django.urls import reverse_lazy


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

########################################
# APPS
########################################
SHARED_APPS = [
    'tenant_schemas',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    "tenant_users.permissions",
    "tenant_users.tenants",
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_htmx',
    'allauth',
    'allauth.account',
    'users',
    'djstripe',
    'captcha',
    'django_select2',
    'crispy_forms',
    'webpack_loader',
    'platzhalter',
]

TENANT_APPS = [
    'tenant_schemas',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    'django.contrib.admin',
    "tenant_users.permissions",
    "webpack_loader",
    'produkte',
    'vorsorgen',
    'kontakte',
    'sterbefall',
    'dokumente',
    'trauermusik',
    'rechnung',   
    'kalender', 
]

INSTALLED_APPS = SHARED_APPS + [ app for app in TENANT_APPS if app not in SHARED_APPS]


########################################
# MIDDLEWARE
########################################
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'tenant_schemas.middleware.TenantMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'users.middleware.TenantMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'users.middleware.AutoLogoutMiddleware',
]

########################################
# SECURITY
########################################

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = bool(os.getenv("DJANGO_DEBUG", "False").lower() in ["true", "1"])
ALLOWED_HOSTS = ['*']

########################################
# OTHER
########################################
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
SITE_ID = 1

########################################
# TEMPLATES
########################################
CRISPY_TEMPLATE_PACK = 'bootstrap4'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'context_processors.plan_context',
                'context_processors.base_url_context',
                'context_processors.stripe_context',
            ],
        },
    },
]

########################################
# DATABASE
########################################

DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASE_ROUTERS = [
    'tenant_schemas.routers.TenantSyncRouter',
]


########################################
# PASSWORD VALIDATION
########################################
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

########################################
# INTERNATIONALISATION
########################################


########################################
# EMAIL SETTINGS
########################################

DEFAULT_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_EMAIL_HOST = ''
DEFAULT_EMAIL_PORT = 587
DEFAULT_EMAIL_HOST_USER = ''
DEFAULT_EMAIL_HOST_PASSWORD = ''
DEFAULT_EMAIL_USE_TLS = True
DEFAULT_EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'default@example.com'

# Internationalisierung
LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Format für Datum und Zeit
DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y H:i'
TIME_FORMAT = 'H:i'

# Eingabeformate für Datum
DATE_INPUT_FORMATS = ['%d.%m.%Y']
DATETIME_INPUT_FORMATS = ['%d.%m.%Y %H:%M']

########################################
# STATIC SETTINGS
########################################
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

########################################
# AUTHENTICATION
########################################

AUTH_USER_MODEL = 'users.CustomUser'

TENANT_MODEL = "users.Company"
TENANT_DOMAIN_MODEL = 'users.Domain'

AUTHENTICATION_BACKENDS = ( 
    "users.backends.TenantAuthenticationBackend",
)


########################################
# SITE SETTINGS
########################################
# todo: set your site name, your country and your support email here
SITE_NAME = "Cover"
SITE_LOCATION = "Germany"
SUPPORT_EMAIL = "support@example.com"

# In settings.py hinzufügen:
AUTO_LOGOUT_DELAY = 18000  # 30 Minuten Inaktivität


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_SCHEMA_GENERATOR_CLASS': 'rest_framework.schemas.generators.SchemaGenerator',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    #'DEFAULT_PERMISSION_CLASSES': [
    #    'rest_framework.permissions.IsAuthenticated',
    #],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Token',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
import logging

CORS_LOG_LEVEL = logging.DEBUG
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:5001',  # React development server
#     'http://thanatorium.localhost:8000',
#     'http://localhost:8000',
#     'http://127.0.0.1:8000',
#     'http://127.0.0.1:5001',
#     'http://<your_laptop_ip>:5001',  # Access from phone
#     'http://<your_laptop_ip>:8000',  # Access from phone
# ]


CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


########################################
# PAYMENTS
########################################
TRIAL_PLAN_STRIPE_ID = None
DJSTRIPE_USE_NATIVE_JSONFIELD = True
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

# Add the following line to specify the Stripe API version
STRIPE_API_VERSION = "2023-10-16"  # or another supported version
# todo: set your trial length here
TRIAL_DAYS = 14
# todo: update your plans here
# To configure payments, take a look at: https://getlaunchr.com/docs/payments/
PLANS = {
    # this is the plans unique key. if you change the key here,
    # you also need to change the key in your environment settings (settings/dev.py &
    # settings/prod.py) to correctly attach the plan on stripe.
    "starter": {
        # the name, as it is displayed to end users
        "name": "Starter",
        # the stripe_id attached to this plan
        # note: when configuring plans, leave the stripe_id set
        # to None here and set it in the settings file for your
        # current environment (app/settings/dev.py & app/settings/prod.py).
        # This makes sure that the correct stripe id is used for the environment.
        "stripe_id": None,
        # plans that are set to be available are shown to end users
        # on the pricing and subscription page.
        "available": True,
        # the recurring price for this plan
        "price": "4.99",
        # the features this plan has are listed here.
        "features": [
            {
                # if the feature is enabled, a green checkmark
                # is displayed
                "enabled": True,
                # the text as it is displayed for end users
                "text": "Feature 1",
                # the unique key this feature has. For a user which is
                # subscribed to a plan, we can call the user.can_use_feature('feature_1')
                # function to determine if the user can use this feature.
                "key": "feature_1"
            },
            {
                "enabled": False,
                "text": "Feature 2",
                "key": "feature_2"
            },
            {
                "enabled": False,
                "text": "Feature 3",
                "key": "feature_3"
            },
            {
                "enabled": False,
                "text": "Feature 4",
                "key": "feature_4"
            },
        ]
    },
    "basic": {
        "name": "Basic",
        "stripe_id": None,
        "available": True,
        "price": "9.99",
        "features": [
            {
                "enabled": True,
                "text": "Feature 1",
                "key": "feature_1"
            },
            {
                "enabled": True,
                "text": "Feature 2",
                "key": "feature_2"
            },
            {
                "enabled": False,
                "text": "Feature 3",
                "key": "feature_3"
            },
            {
                "enabled": False,
                "text": "Feature 4",
                "key": "feature_4"
            },
        ]
    },
    "pro": {
        "name": "Pro",
        "stripe_id": None,
        "available": True,
        "price": "19.99",
        "features": [
            {
                "enabled": True,
                "text": "Feature 1",
                "key": "feature_1"
            },
            {
                "enabled": True,
                "text": "Feature 2",
                "key": "feature_2"
            },
            {
                "enabled": True,
                "text": "Feature 3",
                "key": "feature_3"
            },
            {
                "enabled": True,
                "text": "Feature 4",
                "key": "feature_4"
            },
        ]
    }
}
# Bypassing Stripe allows us to test the app without setting
# up Stripe for every development environment. Don't use this
# in production.
BYPASS_STRIPE = False
