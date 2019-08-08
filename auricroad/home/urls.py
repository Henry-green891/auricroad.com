from django.urls import path

from .views import ContactFormView, ExampleFormView, error

urlpatterns = [
    path(r"error/", error, name="error"),
    path(r"form/", ExampleFormView.as_view(), name="Example Form"),
    path(r"contact_form/", ContactFormView.as_view(), name="contact_form"),
]
