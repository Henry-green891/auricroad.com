from django.utils.html import format_html

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import AbstractMediaChooserBlock
from wagtailmodelchooser.blocks import ModelChooserBlock


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
