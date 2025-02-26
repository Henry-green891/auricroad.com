from .base import *
import secrets

# Generate a secure random key if not provided in .env
default_key = secrets.token_urlsafe(50)
env.read_env(repo_root(".env"))
if not env("SECRET_KEY", default=None):
    env.ENVIRON["SECRET_KEY"] = default_key

ALLOWED_HOSTS = [u"127.0.0.1", "localhost"]
DEBUG = True

DATABASES = {"default": env.db()}
DATABASES["salesforce"] = {
    "ENGINE": "salesforce.backend",
    "CONSUMER_KEY": env("SALESFORCE_CONSUMER_KEY"),
    "CONSUMER_SECRET": env("SALESFORCE_CONSUMER_SECRET"),
    "USER": env("SALESFORCE_USER"),
    "PASSWORD": env("SALESFORCE_PASSWORD"),
    "HOST": env("SALESFORCE_HOST", default="https://test.salesforce.com"),
}
DATABASE_ROUTERS = ["salesforce.router.ModelRouter"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        #"KEY_PREFIX": "wagtailcache",
        #"TIMEOUT": 3600,
    }
}

MEDIA_ROOT = root("media")
MEDIA_URL = "/media/"

STATIC_ROOT = root("static")


INSTALLED_APPS += ("debug_toolbar", "template_debug")

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

INTERNAL_IPS = ("127.0.0.1",)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


class InvalidVariable(str):
    def __bool__(self):
        return False


TEMPLATES[0]["OPTIONS"]["debug"] = True
TEMPLATES[1]["OPTIONS"]["debug"] = True
TEMPLATES[1]["OPTIONS"]["string_if_invalid"] = InvalidVariable(
    "BAD TEMPLATE VARIABLE: %s"
)


CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
