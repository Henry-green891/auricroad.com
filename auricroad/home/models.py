from django.db import models  # NOQA

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.models import AbstractImage, AbstractRendition, Image

from wagtailmedia.models import AbstractMedia

from .blocks import Hero
from .constants import ENVIRONMENT_CHOICES


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    environment = models.CharField(
        max_length=50, choices=ENVIRONMENT_CHOICES, default=""
    )


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
    body = StreamField([("hero", Hero())], null=True, blank=True)

    content_panels = Page.content_panels + [StreamFieldPanel("body")]

    parent_page_types = [HomePage]
