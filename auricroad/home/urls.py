from django.urls import path

from .views import ExampleFormView, error

urlpatterns = [
    path(r"error/", error, name="error"),
    path(r"form/", ExampleFormView.as_view(), name="Example Form"),
]
