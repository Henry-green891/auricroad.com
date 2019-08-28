from django.db import models  # NOQA
from django.utils.translation import ugettext_lazy as _

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import \
    InlineStyleElementHandler
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
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


class FooterContactAdmin(ModelAdmin):
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
