# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, ModelFormMixin

# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
from .context_processors import global_header
from .forms import UserForm
from .models import Contact
from .utils import form_send_mail
from .wagtail_hooks import ContactFormSettings


@method_decorator(login_required, name="dispatch")
class ExampleFormView(FormView):
    form_class = UserForm
    template_name = "example_form.html"
    success_url = "/form"

    def form_valid(self, form):
        form.good_to_go()
        return super(ExampleFormView, self).form_valid(form)


def error(request):
    """Generate an exception. Useful for e.g. configuing Sentry"""
    raise Exception


def handler404(request, exception, template_name="404.html"):
    context = {"request": request}
    context.update(global_header(request))
    response = render_to_response(template_name, context=context)
    response.status_code = 404
    return response


def handler500(request, template_name="500.html"):
    context = {"request": request}
    context.update(global_header(request))
    response = render_to_response(template_name, context=context)
    response.status_code = 500
    return response


class ContactFormView(FormView, ModelFormMixin):
    model = Contact
    fields = ["first_name", "last_name", "email"]
    http_method_names = ["post"]

    def form_valid(self, form):
        form.save()
        contact_form_settings = ContactFormSettings.for_site(self.request.site)
        if contact_form_settings.to_address:
            form_send_mail(
                form,
                contact_form_settings.to_address,
                contact_form_settings.from_address,
                contact_form_settings.subject,
            )
        return_url = self.request.POST.get("return_url", "/")
        return redirect(return_url)

    def form_invalid(self, form):
        return_url = self.request.POST.get("return_url", "/")
        return redirect(return_url)
