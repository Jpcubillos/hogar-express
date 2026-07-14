from .base import *
import os

DEBUG = True

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key-hogar-express')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,backend').split(',')

CSRF_TRUSTED_ORIGINS = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', 'http://localhost:5173,http://localhost:8000').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'hogar_express'),
        'USER': os.getenv('POSTGRES_USER', 'hogar_express'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'change_me'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5173').split(',')
CORS_ALLOW_CREDENTIALS = True

# Development email backend (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
