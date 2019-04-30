from django.utils.html import format_html

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmodelchooser.blocks import ModelChooserBlock

from .constants import (ACCENT_BAR_CHOICES, FONT_CHOICES, FONT_SIZE_CHOICES,
                        IMAGE_GROUP_LAYOUTS)

from wagtailmedia.blocks import AbstractMediaChooserBlock  # isort:skip



class MediaBlock(AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        if not value:
            return ""
        player_code = """
            <div class="media-wrapper">
                <video width="320" height="240" controls>
                    <source src="{0}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            """

        return format_html(player_code, value.file.url)


class HeroCard(blocks.StructBlock):
    icon = ImageChooserBlock()
    header = blocks.CharBlock(max_length=50)
    subheader = blocks.CharBlock(max_length=50)
    body = blocks.CharBlock(max_length=200)

    class Meta:
        template = "blocks/hero_card_block.html"


class Hero(blocks.StructBlock):
    static_header = blocks.CharBlock(max_length=100)
    static_tagline = blocks.CharBlock(max_length=50)
    static_body = blocks.RichTextBlock()
    body_font = blocks.ChoiceBlock(choices=FONT_CHOICES, required=True)
    body_size = blocks.ChoiceBlock(choices=FONT_SIZE_CHOICES, required=True)
    background_image = ImageChooserBlock(required=False)
    cards = blocks.StreamBlock(
        [("card", HeroCard())], null=True, blank=True, required=False
    )
    hero_video = MediaBlock(icon="media", required=False)

    class Meta:
        template = "blocks/hero_block.html"


class HotelsList(blocks.StructBlock):
    hotels = blocks.ListBlock(ModelChooserBlock("home.Hotel"))

    class Meta:
        template = "blocks/hotels_list.html"


class HotelsDevelopmentCard(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50)
    header = blocks.CharBlock(max_length=50)
    background_image = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/development_card.html"


class HotelsDevelopment(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50)
    header = blocks.CharBlock(max_length=50)
    body = blocks.RichTextBlock()
    cards = blocks.StreamBlock(
        [("card", HotelsDevelopmentCard())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/hotels_development.html"


class HotelsDestinations(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50)
    header = blocks.CharBlock(max_length=50)
    body = blocks.RichTextBlock()
    background_image = ImageChooserBlock(required=False)
    foreground_image = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/hotels_destinations.html"


class HotelIntro(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50)
    tagline_bar_style = blocks.ChoiceBlock(choices=ACCENT_BAR_CHOICES, required=True)
    header = blocks.CharBlock(max_length=50)
    body = blocks.RichTextBlock()
    accent_image = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/hotel_intro.html"


class ImageRow(blocks.StructBlock):
    layout = blocks.ChoiceBlock(choices=IMAGE_GROUP_LAYOUTS, required=True)
    images = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        template = "blocks/image_row.html"


class ImageSection(blocks.StructBlock):
    rows = blocks.ListBlock(ImageRow())

    class Meta:
        template = "blocks/image_section.html"


class HotelActivityCard(blocks.StructBlock):
    activity_image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=50)

    class Meta:
        template = "blocks/activity_card.html"


class ActivitySection(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50)
    header = blocks.CharBlock(max_length=50)
    cards = blocks.StreamBlock(
        [("card", HotelActivityCard())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/activity_section.html"


class FloorPlanSection(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50)
    header = blocks.CharBlock(max_length=50)
    body = blocks.RichTextBlock()

    class Meta:
        template = "blocks/floor_plan_section.html"


class HotelDetailCard(blocks.StructBlock):
    header = blocks.CharBlock(max_length=50)
    subheader = blocks.CharBlock(max_length=50)
    body = blocks.RichTextBlock()
    detail_icon = ImageChooserBlock(required=False)
    action_header = blocks.CharBlock(max_length=50)
    action_text = blocks.CharBlock(max_length=250, required=False)
    action_text_two = blocks.CharBlock(max_length=250, required=False)
    facebook = blocks.CharBlock(max_length=50, required=False)
    instagram = blocks.CharBlock(max_length=50, required=False)
    twitter = blocks.CharBlock(max_length=50, required=False)

    class Meta:
        template = "blocks/hotel_detail_card.html"


class HotelDetailSection(blocks.StructBlock):
    cards = blocks.StreamBlock(
        [("card", HotelDetailCard())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/hotel_detail_section.html"
