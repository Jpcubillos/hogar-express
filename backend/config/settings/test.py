from .base import *
import os

DEBUG = False

SECRET_KEY = 'django-test-secret-key-hogar-express'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'hogar_express_test'),
        'USER': os.getenv('POSTGRES_USER', 'hogar_express'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'change_me'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Speed up password hashing in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
