from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from auricroad.home import views as home_views  # NOQA

urlpatterns = [
    path(
        r"favicon.ico",
        RedirectView.as_view(url="/static/img/favicon.ico", permanent=True),
    ),
    path(r"account/", include("auricroad.account.urls")),
    path(r"admin/", admin.site.urls),
    path(r"cms/", include(wagtailadmin_urls)),
    path(r"documents/", include(wagtaildocs_urls)),
    path("", include("social_django.urls", namespace="social")),
    path(r"", include("auricroad.home.urls")),
    path(r"", include(wagtail_urls)),
]

handler404 = home_views.handler404
handler500 = home_views.handler500

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [path(r"__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += [
#    
#]