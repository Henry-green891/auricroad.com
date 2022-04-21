from .base import *

# if you want to test with debug off
env.read_env(repo_root(".env"), SECRET_KEY="changeme")

ALLOWED_HOSTS = [u"127.0.0.1", "localhost"]
DEBUG = True


DATABASES = {"default": env.db()}
DATABASES["salesforce"] = {
    "ENGINE": "salesforce.backend",
    "CONSUMER_KEY": env("SALESFORCE_CONSUMER_KEY", default=""),
    "CONSUMER_SECRET": env("SALESFORCE_CONSUMER_SECRET", default=""),
    "USER": env("SALESFORCE_USER", default=""),
    "PASSWORD": env("SALESFORCE_PASSWORD", default=""),
    "HOST": env("SALESFORCE_HOST", default="https://test.salesforce.com"),
}
DATABASE_ROUTERS = ["salesforce.router.ModelRouter"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "KEY_PREFIX": "wagtailcache",
        "TIMEOUT": 3600,
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


SECRET_KEY = env("SECRET_KEY")
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
