from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


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
    background_image = ImageChooserBlock()
    cards = blocks.StreamBlock(
        [("card", HeroCard())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/hero_block.html"
