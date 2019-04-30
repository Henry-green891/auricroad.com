from django.db import models  # NOQA

from autoslug import AutoSlugField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtailmodelchooser import register_model_chooser

from .blocks import (ActivitySection, FloorPlanSection, Hero,
                     HotelDetailSection, HotelIntro, HotelsDestinations,
                     HotelsDevelopment, HotelsList, ImageSection)
from .constants import ENVIRONMENT_CHOICES

from wagtailmedia.models import AbstractMedia  # isort:skip



@register_model_chooser
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", null=True, default=None, unique=True)
    location = models.CharField(max_length=255)
    environment = models.CharField(
        max_length=50, choices=ENVIRONMENT_CHOICES, default=""
    )
    background_image = models.ForeignKey(
        "home.CustomImage",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("location"),
        FieldPanel("environment"),
        FieldPanel("background_image"),
    ]


class CustomImage(AbstractImage):
    # Add any extra fields to image here

    # eg. To add a caption field:
    # caption = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        # 'caption',
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class CustomMedia(AbstractMedia):
    admin_form_fields = (
        "title",
        "file",
        "collection",
        "duration",
        "width",
        "height",
        "thumbnail",
        "tags",
    )


class HomePage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [FieldPanel("body", classname="full")]


class HotelsPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("hotels", HotelsList()),
            ("development", HotelsDevelopment()),
            ("destinations", HotelsDestinations()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]

    parent_page_types = [HomePage]


class HotelDetailPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("intro", HotelIntro()),
            ("image_section", ImageSection()),
            ("activity_section", ActivitySection()),
            ("floor_plan_section", FloorPlanSection()),
            ("detail_section", HotelDetailSection()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]

    parent_page_types = [HotelsPage]
