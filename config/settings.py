import os
from pathlib import Path
from datetime import timedelta
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

print(f"[DEBUG] BASE_DIR: {BASE_DIR}")
print(f"[DEBUG] ENV_PATH exists: {ENV_PATH.exists()}")

# Initialize environ
env = environ.Env()

if ENV_PATH.exists():
    env.read_env(str(ENV_PATH))
    print("[DEBUG] .env loaded successfully")
else:
    print(f"WARNING: .env file not found at {ENV_PATH}")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure--d@#u_95*ldt_yn)(*fqxkzx7n^eck-fxz=az&)o+_5@%9^op2",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

# Build ALLOWED_HOSTS - read from env or use safe defaults
allowed_env = env.str("ALLOWED_HOSTS", default="")
if allowed_env:
    ALLOWED_HOSTS = [h.strip() for h in allowed_env.split(",") if h.strip()]
else:
    # Allow all in production when no ALLOWED_HOSTS specified - safer for container deployments
    ALLOWED_HOSTS = ["*"]

print(f"[DEBUG] ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# Application definition
INSTALLED_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",  # Added for JWT support
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api",
]

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database - PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="kompra_db"),
        "USER": env("DB_USER", default="raidevs"),
        "PASSWORD": env("DB_PASSWORD", default="Rightech777"),
        "HOST": env("DB_HOST", default="72.60.233.51"),
        "PORT": env("DB_PORT", default="5434"),
    }
}


# Custom User Model
AUTH_USER_MODEL = "api.User"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files (Business Permits, Supplier Catalogs, etc.)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "rai.jedkerk@gmail.com"
EMAIL_HOST_PASSWORD = "dhpjekrgiaokcpqc"
DEFAULT_FROM_EMAIL = "rai.jedkerk@gmail.com"

# Django Rest Framework Configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# SimpleJWT Configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
