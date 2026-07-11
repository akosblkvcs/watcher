"""Django settings for the watcher project.

All configuration comes from environment variables and is required.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import dj_database_url
import django_stubs_ext
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def _env_str(name: str) -> str:
    """Read a required environment variable, raising if it is missing."""
    value = os.environ.get(name)

    if value is None:
        raise ImproperlyConfigured(f"Missing required environment variable: {name}")

    return value


def _env_bool(name: str) -> bool:
    """Read a required boolean environment variable."""
    return _env_str(name).strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str) -> int:
    """Read a required integer environment variable."""
    value = _env_str(name)

    try:
        return int(value)
    except ValueError as ex:
        raise ImproperlyConfigured(f"{name} must be an integer, got {value!r}") from ex


def _env_list(name: str) -> list[str]:
    """Read a required comma-separated environment variable as a list."""
    return [item.strip() for item in _env_str(name).split(",") if item.strip()]


# Core

SECRET_KEY = _env_str("SECRET_KEY")
DEBUG = _env_bool("DEBUG")
ALLOWED_HOSTS = _env_list("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "watch",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# Database

DATABASES = {
    "default": dj_database_url.parse(_env_str("DATABASE_URL")),
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# I18n

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (served by WhiteNoise)

STATIC_URL = "static/"
STATICFILES_DIRS = [d for d in [BASE_DIR / "static"] if d.is_dir()]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Hashed + compressed static files only in production; the manifest
# requires collectstatic, which dev servers and tests don't run.
if not DEBUG:
    STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # TLS terminates at the reverse proxy (Traefik); trust its
    # forwarded-proto header so is_secure() works and the SSL redirect
    # below doesn't loop.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = [r"^healthz$"]

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Logging

LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": _env_str("LOG_LEVEL"),
    },
}

# Watcher

WATCHER_HTTP_TIMEOUT_SECONDS = _env_int("HTTP_TIMEOUT_SECONDS")
WATCHER_HTTP_RETRIES = _env_int("HTTP_RETRIES")
WATCHER_USER_AGENT = _env_str("USER_AGENT")
