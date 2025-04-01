import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


# --- Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tailwind',
    'theme',
    'users',
]

# Optional: only in development
if DEBUG:
    INSTALLED_APPS.append("django_browser_reload")

# --- Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Optional: only in development
if DEBUG:
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

# --- Tailwind settings
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = 'core.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# DATABASE: SQLite (default), switch to MySQL by uncommenting the next block
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'data/db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    },
    "mirzabot": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MIRZABOT_DB_NAME"),
        "USER": os.getenv("MIRZABOT_DB_USER"),
        "PASSWORD": os.getenv("MIRZABOT_DB_PASSWORD"),
        "HOST": os.getenv("MIRZABOT_DB_HOST", "localhost"),
        "PORT": os.getenv("MIRZABOT_DB_PORT", "3306"),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# LANGUAGE_CODE = os.getenv('LANG', 'en-us')
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
# USE_I18N = True
# USE_TZ = True

# --- Static / Media
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # For local static files (like app.js)
STATIC_ROOT = BASE_DIR / "staticfiles"    # For collected static in Docker

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Auto-create dirs (optional)
os.makedirs(STATICFILES_DIRS[0], exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
LOGGING_DIR = BASE_DIR / "logs"
os.makedirs(LOGGING_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOGGING_DIR / "django_errors.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}


# urls.py check if debug_toolbar is activated

# if DEBUG:
#     MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Optional: enable debug toolbar in dev
# if DEBUG:
#     INSTALLED_APPS.append("debug_toolbar")

# Extra production security (applies when DEBUG=False)
# --- Optional: security for production
# if not DEBUG:
#     SECURE_BROWSER_XSS_FILTER = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     X_FRAME_OPTIONS = "DENY"
#     SECURE_HSTS_SECONDS = 31536000
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
