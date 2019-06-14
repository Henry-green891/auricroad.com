from django.conf import settings as django_settings

from jinja2 import Environment

from auricroad.home.models import NavBar  # noqa


def settings(request):
    settings = {"settings": django_settings}

    return settings


def jinja_environment(**options):
    env = Environment(**options)  # nosec
    return env


def global_header(request):
    global_nav_filter = NavBar.objects.filter(name="Global Nav Bar")
    return {
        "global_nav_exists": global_nav_filter.exists(),
        "global_nav_obj": global_nav_filter.first(),
    }
