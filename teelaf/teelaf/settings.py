"""
Django settings for teelaf project.
"""

import os
from pathlib import Path

# --- BASE PATH ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- SECURITY ---
SECRET_KEY = 'django-insecure-w+o^!gp4l1x^%&$4lj(tib^aj=pjuru=jmh4)91g!yrp0u=1_5'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'teelaf.pythonanywhere.com']

# --- APPLICATIONS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps du projet
    'dashboard',
    'members',
    'learners',
    'Suivi_des_apprenants',
    'Grille_evaluation',
    'clients',
    'Suivi_projects',
    # Pour les formulaires stylés
    'crispy_forms',
    'crispy_bootstrap5',
    'Depenses',
    'django.contrib.humanize',
    'widget_tweaks',  # Pour les filtres de widgets dans les templates
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- URLS ---
ROOT_URLCONF = 'teelaf.urls'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'teelaf/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

# --- WSGI ---
WSGI_APPLICATION = 'teelaf.wsgi.application'

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --- STATIC FILES ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'teelaf/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# --- MEDIA FILES ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- DEFAULT PRIMARY KEY ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- EMAIL (développement) ---
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- CRISPY FORMS (Bootstrap 5) ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# --- LOGIN REDIRECT (après connexion) ---
LOGIN_REDIRECT_URL = '/learners/'

# --- CUSTOM SETTINGS ---
TEELAF_CONFIG = {
    'SITE_NAME': 'TEELAF',
    'PRIMARY_COLOR': '#1d4d8e',
    'SECONDARY_COLOR': '#3f98b0',
}