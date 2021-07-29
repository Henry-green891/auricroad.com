from django.contrib.auth.decorators import login_required
from django.db import models  # NOQA
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from djqscsv import render_to_csv_response
from wagtail.admin.rich_text.converters.html_to_contentstate import \
    InlineStyleElementHandler
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import hooks

from .models import Contact, Footer, Hotel, NavBar


class HotelAdmin(ModelAdmin):
    model = Hotel
    menu_label = "Hotels"
    menu_icon = "home"
    menu_order = 203
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "slug", "location", "environment")
    list_filter = ("name",)
    search_fields = ("name",)


class NavBarAdmin(ModelAdmin):
    model = NavBar
    menu_label = "Nav Bars"
    menu_icon = "link"
    menu_order = 204
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "slug")
    list_filter = ("name",)
    search_fields = ("name",)


class FooterAdmin(ModelAdmin):
    model = Footer
    menu_label = "Footers"
    menu_icon = "link"
    menu_order = 205
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "slug")
    list_filter = ("name",)
    search_fields = ("name",)


class ExportButtonHelper(ButtonHelper):
    export_button_classnames = ["icon", "icon-download"]

    def export_button(self, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []

        classnames = self.export_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        text = _("Export {} to CSV".format(self.verbose_name_plural.title()))

        return {
            "url": self.url_helper.get_action_url(
                "export", query_params=self.request.GET
            ),
            "label": text,
            "classname": cn,
            "title": text,
        }


class ExportAdminURLHelper(AdminURLHelper):
    non_object_specific_actions = ("create", "choose_parent", "index", "export")

    def get_action_url(self, action, *args, **kwargs):
        query_params = kwargs.pop("query_params", None)

        url_name = self.get_action_url_name(action)
        if action in self.non_object_specific_actions:
            url = reverse(url_name)
        else:
            url = reverse(url_name, args=args, kwargs=kwargs)

        if query_params:
            url = f"{url}?{query_params.urlencode()}"

        return url

    def get_action_url_pattern(self, action):
        if action in self.non_object_specific_actions:
            return self._get_action_url_pattern(action)

        return self._get_object_specific_action_url_pattern(action)


class ExportView(IndexView):
    model_admin = None

    def export_csv(self):
        if (self.model_admin is None) or not hasattr(
            self.model_admin, "csv_export_fields"
        ):
            data = self.queryset.all().values()
        else:
            data = self.queryset.all().values(*self.model_admin.csv_export_fields)
        return render_to_csv_response(data)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        return self.export_csv()


class ExportModelAdminMixin:
    button_helper_class = ExportButtonHelper
    url_helper_class = ExportAdminURLHelper
    export_view_class = ExportView

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            path(
                self.url_helper.get_action_url_pattern("export"),
                self.export_view,
                name=self.url_helper.get_action_url_name("export"),
            ),
        )
        return urls

    def export_view(self, request):
        kwargs = {"model_admin": self}
        view_class = self.export_view_class
        return view_class.as_view(**kwargs)(request)


class FooterContactAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "../templates/export_csv.html"
    model = Contact
    menu_label = "Footer Contacts"
    menu_icon = "group"
    menu_order = 206
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")


modeladmin_register(HotelAdmin)
modeladmin_register(NavBarAdmin)
modeladmin_register(FooterAdmin)
modeladmin_register(FooterContactAdmin)


@register_setting
class ContactFormSettings(BaseSetting):
    to_address = models.CharField(
        verbose_name=_("to address"),
        max_length=255,
        blank=True,
        help_text=_(
            "Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma."
        ),
    )
    from_address = models.CharField(
        verbose_name=_("from address"), max_length=255, blank=True
    )
    subject = models.CharField(verbose_name=_("subject"), max_length=255, blank=True)


@hooks.register("register_rich_text_features")
def register_strikethrough_feature(features):
    """
    Registering the `strikethrough` feature, which uses the `STRIKETHROUGH` Draft.js inline style type,
    and is stored as HTML with an `<s>` tag.
    """
    feature_name = "underline"
    type_ = "UNDERLINE"
    tag = "u"

    control = {
        "type": type_,
        "label": "U",
        "description": "Underline",
        "style": {"textDecoration": "underline"},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: tag}},
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append("underline")
