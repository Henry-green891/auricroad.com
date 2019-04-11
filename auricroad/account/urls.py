from django.urls import path, include
urlpatterns = []
from .views import LoginView, RegistrationView # NOQA
from django.contrib.auth import urls as auth_urls # NOQA

urlpatterns.extend([
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'member/register/',
         RegistrationView.as_view(),
         name='register'),
    path(r'', include(auth_urls)),
])
