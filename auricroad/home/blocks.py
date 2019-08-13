from django.utils.html import format_html

from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from .constants import (  # isort:skip
    ACCENT_BAR_CHOICES,
    CUSTOM_TEXT_FUNCTIONS,
    FONT_CHOICES,
    FONT_STYLE_CHOICES,
    FONT_SIZE_CHOICES,
    IMAGE_GROUP_LAYOUTS,
    LAYOUT_CHOICES,
    SOCIAL_TYPES,
    X_POSITIONS,
    Y_POSITIONS,
)

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


class LinkBlock(blocks.StructBlock):
    text = blocks.CharBlock(max_length=50)
    internal_page = blocks.PageChooserBlock(required=False)
    external_link = blocks.CharBlock(max_length=250, required=False)


class HeaderLinkBlock(LinkBlock):
    orange_accent_text = blocks.BooleanBlock(required=False)

    class Meta:
        template = "blocks/header_link_block.html"


class FooterLinkBlock(LinkBlock):
    social_type = blocks.ChoiceBlock(choices=SOCIAL_TYPES, required=False)

    class Meta:
        template = "blocks/footer_link_block.html"


class FooterLinkColumn(blocks.StructBlock):
    column_header = blocks.CharBlock(max_length=50)
    links = blocks.StreamBlock(
        [("link", FooterLinkBlock())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/footer_link_column.html"


class FooterLegalBar(blocks.StructBlock):
    copyright_text = blocks.CharBlock(max_length=255)
    links = blocks.StreamBlock(
        [("link", LinkBlock(template="blocks/footer_legal_link.html"))],
        null=True,
        blank=True,
        required=False,
    )

    class Meta:
        template = "blocks/footer_legal_bar.html"


class SocialIconLink(blocks.StructBlock):
    link_url = blocks.CharBlock(max_length=500, required=False)
    social_type = blocks.ChoiceBlock(choices=SOCIAL_TYPES, required=True)

    class Meta:
        template = "blocks/social_icon_link.html"


class HeroCard(blocks.StructBlock):
    icon = ImageChooserBlock()
    header = blocks.CharBlock(max_length=50)
    subheader = blocks.CharBlock(max_length=50, required=False)
    body = blocks.CharBlock(max_length=200)

    class Meta:
        template = "blocks/hero_card_block.html"


class Hero(blocks.StructBlock):
    static_header = blocks.CharBlock(max_length=100, required=False)
    static_tagline = blocks.CharBlock(max_length=50, required=False)
    static_body = blocks.RichTextBlock(required=False)
    body_font = blocks.ChoiceBlock(choices=FONT_CHOICES, default="e")
    body_size = blocks.ChoiceBlock(choices=FONT_SIZE_CHOICES, default=2)
    background_image = ImageChooserBlock(required=False)
    background_image_x_position = blocks.ChoiceBlock(
        choices=X_POSITIONS, default="center"
    )
    background_image_y_position = blocks.ChoiceBlock(choices=Y_POSITIONS, default="top")
    show_diamond_overlay = blocks.BooleanBlock(required=False)
    reduced_padding = blocks.BooleanBlock(required=False)
    extended_bottom_padding = blocks.BooleanBlock(required=False)
    wider_desktop_layout = blocks.BooleanBlock(required=False)
    cards = blocks.StreamBlock(
        [("card", HeroCard())], null=True, blank=True, required=False
    )
    hero_video_url = blocks.CharBlock(max_length=500, required=False)
    replacement_video_load_background = ImageChooserBlock(required=False)
    hero_video_play_icon = ImageChooserBlock(required=False)
    video_only_hero = blocks.BooleanBlock(required=False)

    class Meta:
        template = "blocks/hero_block.html"


class FullWidthImageCardSection(blocks.StructBlock):
    background_image = ImageChooserBlock(required=False)
    header = blocks.RichTextBlock(required=False)
    text_accent_color = blocks.CharBlock(max_length=50, required=False)
    body = blocks.RichTextBlock(required=False)
    accent_image = ImageChooserBlock()
    button_text = blocks.CharBlock(max_length=50, required=False)
    internal_page = blocks.PageChooserBlock(required=False)
    external_link = blocks.CharBlock(max_length=250, required=False)

    class Meta:
        template = "blocks/full_width_image_card_section.html"


class BlockQuote(blocks.StructBlock):
    body = blocks.RichTextBlock()
    name = blocks.CharBlock(max_length=100, required=False)
    name_font_style = blocks.ChoiceBlock(choices=FONT_STYLE_CHOICES, required=False)
    title = blocks.CharBlock(max_length=100, required=False)
    background_text = blocks.CharBlock(max_length=10, required=False)
    accent_image = ImageChooserBlock()

    class Meta:
        template = "blocks/block_quote.html"


class BlockQuoteFooter(blocks.StructBlock):
    block_quote = BlockQuote()
    background_image = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/block_quote_footer.html"


class StaticTextSection(blocks.StructBlock):
    static_header = blocks.CharBlock(max_length=100, required=False)
    static_tagline = blocks.CharBlock(max_length=50, required=False)
    static_body = blocks.RichTextBlock(required=False)
    body_font = blocks.ChoiceBlock(choices=FONT_CHOICES, required=False)
    body_size = blocks.ChoiceBlock(choices=FONT_SIZE_CHOICES, required=False)
    background_color = blocks.CharBlock(max_length=50, required=False)
    should_have_top_accent = blocks.BooleanBlock(required=False)

    class Meta:
        template = "blocks/static_text_section.html"


class ImageCard(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50)
    tagline_2 = blocks.CharBlock(max_length=50, required=False)
    header = blocks.CharBlock(max_length=100)
    header_size = blocks.ChoiceBlock(
        choices=FONT_SIZE_CHOICES, required=True, default=3
    )
    subheader = blocks.CharBlock(max_length=50, required=False)
    body = blocks.RichTextBlock(required=False)
    background_image = ImageChooserBlock(required=False)
    arrow_color = blocks.CharBlock(max_length=50, required=False)
    detail_link_text = blocks.CharBlock(max_length=50, required=False)

    class Meta:
        template = "blocks/image_card.html"


class HotelImageCard(ImageCard):
    detail_link = blocks.PageChooserBlock(
        target_model="home.HotelDetailPage", required=False
    )


class BookNowImageCard(ImageCard):
    detail_link = blocks.PageChooserBlock(
        target_model="home.HotelDetailPage", required=False
    )
    detail_link_external_url = blocks.CharBlock(max_length=500, required=False)
    additional_link_text = blocks.CharBlock(max_length=50, required=False)
    additional_detail_link = blocks.PageChooserBlock(
        target_model="home.HotelDetailPage", required=False
    )
    additional_link_url = blocks.CharBlock(max_length=500, required=False)


class EventImageCard(ImageCard):
    detail_link = blocks.PageChooserBlock(
        target_model=("home.BrochuresPage", "home.HotelDetailPage"), required=False
    )


class ExperienceImageCard(ImageCard):
    detail_link = blocks.PageChooserBlock(
        target_model="home.ExperiencePage", required=False
    )


class ImageCardList(blocks.StructBlock):
    hotels = blocks.StreamBlock(
        [
            ("hotel_image_card", HotelImageCard()),
            ("event_image_card", EventImageCard()),
            ("experience_image_card", ExperienceImageCard()),
            ("book_now_image_card", BookNowImageCard()),
        ],
        null=True,
        blank=True,
        required=False,
    )

    class Meta:
        template = "blocks/image_card_list.html"


class FullWidthImage(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        template = "blocks/full_width_image.html"


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


class ImageRow(blocks.StructBlock):
    layout = blocks.ChoiceBlock(choices=IMAGE_GROUP_LAYOUTS, required=True)
    images = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        template = "blocks/image_row.html"


class ImageSection(blocks.StructBlock):
    rows = blocks.ListBlock(ImageRow())

    class Meta:
        template = "blocks/image_section.html"


class HotelIntro(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50, required=False)
    tagline_bar_style = blocks.ChoiceBlock(choices=ACCENT_BAR_CHOICES, required=False)
    tagline_maintain_horizontal = blocks.BooleanBlock(required=False)
    header = blocks.CharBlock(max_length=250)
    header_size = blocks.ChoiceBlock(choices=FONT_SIZE_CHOICES, required=False)
    text_accent_color = blocks.CharBlock(max_length=50, required=False)
    subheader = blocks.CharBlock(max_length=50, required=False)
    subheader_2 = blocks.CharBlock(max_length=50, required=False)
    body = blocks.RichTextBlock()
    second_body = blocks.RichTextBlock(required=False)
    accent_image = ImageChooserBlock(required=False)
    bottom_right_image = ImageChooserBlock(required=False)
    intro_video = MediaBlock(icon="media", required=False)
    images = blocks.StreamBlock(
        [("image_row", ImageSection()), ("full_image", FullWidthImage())],
        null=True,
        blank=True,
        required=False,
    )
    finer_points_header = blocks.CharBlock(max_length=50, required=False)
    finer_points_body = blocks.RichTextBlock(required=False)
    button_text = blocks.CharBlock(max_length=50, required=False)
    internal_page = blocks.PageChooserBlock(required=False)
    external_link = blocks.CharBlock(max_length=250, required=False)

    class Meta:
        template = "blocks/hotel_intro.html"


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


class DetailRow(blocks.StructBlock):
    key = blocks.CharBlock(max_length=250)
    value = blocks.CharBlock(max_length=250)
    remove_row_bottom_padding = blocks.BooleanBlock(
        required=False, help_text="(will be applied by default within detail groups)"
    )

    class Meta:
        template = "blocks/detail_row.html"


class DetailGroup(blocks.StructBlock):
    section_header = blocks.CharBlock(max_length=250)
    detail_rows = blocks.StreamBlock(
        [("detail", DetailRow())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/detail_group.html"


class FloorPlanSlide(blocks.StructBlock):
    room_name = blocks.CharBlock(max_length=50)
    room_description = blocks.RichTextBlock(required=False)
    details = blocks.StreamBlock(
        [("detail", DetailRow()), ("detail_group", DetailGroup())],
        null=True,
        blank=True,
        required=False,
    )
    floor_plan_document_text = blocks.CharBlock(max_length=50, required=False)
    floor_plan_document = DocumentChooserBlock(required=False)
    floor_plan_image = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/floor_plan_slide.html"


class FloorPlanSection(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50)
    header = blocks.CharBlock(max_length=50)
    body = blocks.RichTextBlock()
    rooms = blocks.StreamBlock(
        [("card", FloorPlanSlide())], null=True, blank=True, required=False
    )
    more_info = blocks.RichTextBlock(required=False)
    additional_document_text = blocks.CharBlock(max_length=50, required=False)
    additional_document = DocumentChooserBlock(required=False)
    additional_document_two_text = blocks.CharBlock(max_length=50, required=False)
    additional_document_two = DocumentChooserBlock(required=False)

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
    action_text_type = blocks.ChoiceBlock(choices=CUSTOM_TEXT_FUNCTIONS, required=False)
    action_text_two_type = blocks.ChoiceBlock(
        choices=CUSTOM_TEXT_FUNCTIONS, required=False
    )
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


class SplitImageTextCardSection(blocks.StructBlock):
    layout_style = blocks.ChoiceBlock(choices=LAYOUT_CHOICES, required=True)
    image = ImageChooserBlock()
    header = blocks.RichTextBlock(required=False)
    body = blocks.RichTextBlock()
    button_text = blocks.CharBlock(max_length=50, required=False)
    internal_page = blocks.PageChooserBlock(required=False)
    external_link = blocks.CharBlock(max_length=250, required=False)
    arrow_color = blocks.CharBlock(max_length=50, required=False)
    text_accent_color = blocks.CharBlock(max_length=50, required=False)

    class Meta:
        template = "blocks/split_image_text_card_section.html"


class EventsFooter(blocks.StructBlock):
    tagline = blocks.CharBlock(max_length=50)
    header = blocks.CharBlock(max_length=50)
    body = blocks.RichTextBlock()
    background_image = ImageChooserBlock(required=False)
    button_text = blocks.CharBlock(max_length=50, required=False)
    internal_page = blocks.PageChooserBlock(required=False)
    external_link = blocks.CharBlock(max_length=250, required=False)
    button_text_two = blocks.CharBlock(max_length=50, required=False)
    internal_page_two = blocks.PageChooserBlock(required=False)
    external_link_two = blocks.CharBlock(max_length=250, required=False)

    class Meta:
        template = "blocks/events_footer.html"


class FadeInFooter(blocks.StructBlock):
    background_image = ImageChooserBlock(required=False)
    background_text = blocks.CharBlock(max_length=10, required=False)
    button_text = blocks.CharBlock(max_length=50, required=False)
    internal_page = blocks.PageChooserBlock(required=False)
    external_link = blocks.CharBlock(max_length=250, required=False)

    class Meta:
        template = "blocks/fade_out_footer.html"


class ImageLogoLinkCard(blocks.StructBlock):
    main_image = ImageChooserBlock(required=False)
    logo_image = ImageChooserBlock(required=False)
    header = blocks.CharBlock(max_length=200)
    tagline = blocks.CharBlock(max_length=50)
    tagline_2 = blocks.CharBlock(max_length=50, required=False)
    link_url = blocks.CharBlock(max_length=500)

    class Meta:
        template = "blocks/image_logo_link_card.html"


class ImageLogoLinkCardSection(blocks.StructBlock):
    cards = blocks.StreamBlock(
        [("card", ImageLogoLinkCard())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/image_logo_link_section.html"


class JobRow(blocks.StructBlock):
    department = blocks.CharBlock(max_length=200, required=False)
    job_title = blocks.CharBlock(max_length=200, required=False)
    location = blocks.CharBlock(max_length=200, required=False)
    job_document = DocumentChooserBlock()

    class Meta:
        template = "blocks/job_row.html"


class JobsList(blocks.StructBlock):
    info_text = blocks.RichTextBlock(required=False)

    jobs = blocks.StreamBlock(
        [("job", JobRow())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/jobs_list.html"


class ActionCard(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200)
    image = ImageChooserBlock()
    download_file = DocumentChooserBlock(required=False)

    class Meta:
        template = "blocks/action_card.html"


class ActionCardSection(blocks.StructBlock):
    cards = blocks.StreamBlock(
        [("card", ActionCard())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/action_card_section.html"


class ContactCard(blocks.StructBlock):
    detail_icon = ImageChooserBlock(required=False)
    action_header = blocks.CharBlock(max_length=50)
    action_text = blocks.CharBlock(max_length=250, required=False)
    action_text_two = blocks.CharBlock(max_length=250, required=False)
    action_text_type = blocks.ChoiceBlock(choices=CUSTOM_TEXT_FUNCTIONS, required=False)
    action_text_two_type = blocks.ChoiceBlock(
        choices=CUSTOM_TEXT_FUNCTIONS, required=False
    )
    facebook = blocks.CharBlock(max_length=50, required=False)
    instagram = blocks.CharBlock(max_length=50, required=False)
    twitter = blocks.CharBlock(max_length=50, required=False)

    class Meta:
        template = "blocks/contact_card.html"


class ContactCardRow(blocks.StructBlock):
    cards = blocks.StreamBlock(
        [("card", ContactCard())], null=True, blank=True, required=False
    )

    class Meta:
        template = "blocks/contact_card_section.html"


class PageHeaderText(blocks.StructBlock):
    header = blocks.CharBlock(max_length=500)

    class Meta:
        template = "blocks/page_header_text.html"


class SectionHeader(blocks.StructBlock):
    header = blocks.CharBlock(max_length=500)

    class Meta:
        template = "blocks/section_header.html"


class HeaderTextParagraph(blocks.StructBlock):
    header = blocks.CharBlock(max_length=500, required=False)
    text = blocks.RichTextBlock(required=False)

    class Meta:
        template = "blocks/header_text_paragraph.html"
