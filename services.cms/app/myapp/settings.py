"""
Django settings for myapp project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import datetime
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# print('os.environ', os.environ)
# print('type(os.environ)', type(os.environ))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-w6zog=x*7)^l2qg&nc)crrpc(3@9jrv%9#+r$98pzw7iapsi85'
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-w6zog=x*7)^l2qg&nc)crrpc(3@9jrv%9#+r$98pzw7iapsi85')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = int(os.environ.get("DEBUG", 1))

# ALLOWED_HOSTS = []
# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", 'localhost 127.0.0.1 [::1]').split(" ")
ALLOWED_HOSTS = ['*']

# strftime format
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DOB_FORMAT = '%Y-%m-%d'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Cors
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt', # JWT
    'django_apscheduler',
    'shared',
    # firebase
    'fcm_django',
    'uploads.apps.UploadsConfig', # upload image
    'user.apps.UserConfig', # User module
    'doctor.apps.DoctorConfig',
    'treatment.apps.TreatmentConfig',
    'patient.apps.PatientConfig',
    'health_record.apps.HealthRecordConfig',
    'appointment.apps.AppointmentConfig',
    'disease.apps.DiseaseConfig',
    'specialist.apps.SpecialistConfig',
    'schedule.apps.ScheduleConfig',
    'medicine.apps.MedicineConfig',
    'prescription.apps.PrescriptionConfig',
    'instruction.apps.InstructionConfig',
    'transaction.apps.TransactionConfig',
    'service.apps.ServiceConfig',
    'slot.apps.SlotConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'auth.middlewares.authentication_middleware',
]

ROOT_URLCONF = 'myapp.urls'

REST_FRAMEWORK = {
    # global authentication classes
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'shared.authenticate_backends.CustomAuthenication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # global permission classes
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'EXCEPTION_HANDLER': 'shared.exception_handler.custom_exception_handler'
}

PAGE_SIZE = 10

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
# print(TEMPLATE_PATH)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH],
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

WSGI_APPLICATION = 'myapp.wsgi.application'

# Set up firebase
from firebase_admin import initialize_app, credentials

GOOGLE_APPLICATION_CREDENTIALS = './capstone-firebase-pk.json'
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
FIREBASE_APP = initialize_app(cred)

FCM_DJANGO_SETTINGS = {
    # an instance of firebase_admin.App to be used as default for all fcm-django requests
    # default: None (the default Firebase app)
    "DEFAULT_FIREBASE_APP": None,
    # default: _('FCM Django')
    "APP_VERBOSE_NAME": "FCM Django",
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": False,
    # Transform create of an existing Device (based on registration id) into
                # an update. See the section
    # "Update of device with duplicate registration ID" for more details.
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.mysql"),
        "NAME": os.environ.get("SQL_DATABASE", "capstone_dev"),
        "USER": os.environ.get("SQL_USER", "admin"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "jAnquNq3PBYS6HdwtEW6"),
        "HOST": os.environ.get("SQL_HOST", "capstone.czjd9ym4s3b2.ap-southeast-1.rds.amazonaws.com"),
        "PORT": os.environ.get("SQL_PORT", "3306")
    },
    # "default": {
    #     "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.mysql"),
    #     "NAME": os.environ.get("SQL_DATABASE", "capstone_dev"),
    #     "USER":"root",
    #     "PASSWORD": "123456",
    #     "HOST": 'localhost',
    #     "PORT": os.environ.get("SQL_PORT", "3306")
    # },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# LOGGING
LOGGING = {
    'version': 1,
    # The version number of our log
    'disable_existing_loggers': False,
    # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        },
    },
    # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log
    # DEBUG < INFO < WARNING < ERROR < CRITICAL
    #  10   <  20  <   30    <  40   <   50
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / f'warning-{str(datetime.datetime.utcnow().date())}.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'console2': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
    'loggers': {
        # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
        '': {
            'handlers': ['file', 'console'], #notice how file variable is called in handler which has been defined above
            'level': 'INFO',
            'propagate': True,
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console2'],
        # }
    },
}
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

EXPIRY_TIME_IN_MINUTES = 5
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Use custom user to login
AUTH_USER_MODEL = 'user.User'

# CORS configuration
CORS_ALLOW_ALL_ORIGINS = True # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days = 1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(weeks = 2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': SECRET_KEY,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}

# print('os.environ.get("AWS_REGION")', os.environ.get('AWS_REGION'))
# print("os.environ.get('AWS_STORAGE_BUCKET_NAME')", os.environ.get('AWS_STORAGE_BUCKET_NAME'))
# print("os.environ.get('AWS_ACCESS_KEY_ID')", os.environ.get('AWS_ACCESS_KEY_ID'))
# Set up for S3
AWS_REGION = os.environ.get('AWS_REGION') or 'ap-southeast-1'
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME') or 'cuu-be'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') or 'AKIAS4HJIVKTTA3HPKPC'
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') or '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'

# Email configuration
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND') or 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST') or 'smtp.gmail.com'
EMAIL_PORT = os.environ.get('EMAIL_PORT') or 587
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') or True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') or 'huypc2410@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') or 'yuhadnmqkpuxjqdv'
# print(os.environ)

GOOGLE_MAP_API_KEY = 'AIzaSyDL7tGkbZXsclmbIx9KkguDOBehoHOKugo'

TESSDATA_CONFIG = r'--tessdata-dir "/usr/share/tessdata/"'

# AGORA config
AGORA_CONFIG = {
    'app_id': '2379244a079c45098b6d9040bb37aa85',
    'app_certificate': 'e65713f9be08465293657ce6efaed640',
    'token_expiration_in_seconds': 3600,
    'privilege_expiration_in_seconds': 7200
}

VNPAY_CONFIG = {
    'vnp_TmnCode': 'IZC396TJ',
    'vnp_HashSecret': 'CQCQNOCFNKEQYSFXWPOJHOPXWGUJUZYF',
}