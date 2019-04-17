from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Hotel


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


modeladmin_register(HotelAdmin)
