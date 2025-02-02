"""
Django settings for BloodBridge project.
"""

import dj_database_url
from pathlib import Path
import environ
import os

env = environ.Env()
environ.Env.read_env()  # Load .env file

# Cloudinary Configuration
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": env("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": env("CLOUDINARY_API_KEY"),
    "API_SECRET": env("CLOUDINARY_API_SECRET"),
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = env("DB_SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = ["*"]

# CORS Settings (Corrected)
CORS_ALLOW_ALL_ORIGINS = False  # More secure than True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",  # Local frontend
]
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5500",

]
CORS_ALLOW_CREDENTIALS = True  
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["Authorization", "Content-Type", "X-CSRFToken"]

# Database (Using PostgreSQL on Render)
DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://bloodbridge_user:EZg3I1jXIrnI6ZzPLqVaXVvKZ8QZSVlJ@dpg-cuds8a56l47c73aiiti0-a.oregon-postgres.render.com/bloodbridge",
    )
}

# Middleware (CORS must be at the top)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Installed Apps
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "account",
    "event",
    "donation",
    "user_profile",
]

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

# Templates
ROOT_URLCONF = "BloodBridge.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = "BloodBridge.wsgi.application"

# Media files (Cloudinary will handle them)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Static files
STATIC_URL = "/static/"

# Default AutoField
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email Settings (Load from .env)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("DB_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("DB_EMAIL_HOST_PASSWORD")

# Allow serving media files in production (for testing)
if not DEBUG:
    import mimetypes
    mimetypes.add_type("image/png", ".png", True)
    mimetypes.add_type("image/jpeg", ".jpg", True)
