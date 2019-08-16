from django.db import models  # NOQA
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         StreamFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtailmodelchooser import register_model_chooser

from .constants import ENVIRONMENT_CHOICES

from .blocks import (  # isort:skip
    ActionCardSection,
    ActivitySection,
    BlockQuote,
    BlockQuoteFooter,
    ContactCardRow,
    EventsFooter,
    FadeInFooter,
    FloorPlanSection,
    FooterLegalBar,
    FooterLinkColumn,
    FullWidthImage,
    FullWidthImageCardSection,
    HeaderLinkBlock,
    HeaderTextParagraph,
    Hero,
    HotelDetailSection,
    HotelIntro,
    HotelsDestinations,
    HotelsDevelopment,
    ImageCardList,
    ImageLogoLinkCardSection,
    ImageSection,
    JobsList,
    PageHeaderText,
    SocialIconLink,
    SplitImageTextCardSection,
    StaticTextSection,
    SectionHeader,
)

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
    events_background_image = models.ForeignKey(
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


@register_model_chooser
class NavBar(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", null=True, default=None, unique=True)
    on_load_image = models.ForeignKey(
        "home.CustomImage",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    on_scroll_image = models.ForeignKey(
        "home.CustomImage",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    on_load_mobile_image = models.ForeignKey(
        "home.CustomImage",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    desktop_links = StreamField([("links", HeaderLinkBlock())], null=True, blank=True)
    mobile_top_nav_links = StreamField(
        [("links", HeaderLinkBlock())], null=True, blank=True
    )
    mobile_links = StreamField([("links", HeaderLinkBlock())], null=True, blank=True)
    social_icons = StreamField([("icons", SocialIconLink())], null=True, blank=True)

    panels = [
        FieldPanel("name"),
        ImageChooserPanel("on_load_image"),
        ImageChooserPanel("on_load_mobile_image"),
        ImageChooserPanel("on_scroll_image"),
        StreamFieldPanel("desktop_links"),
        StreamFieldPanel("mobile_top_nav_links"),
        StreamFieldPanel("mobile_links"),
        StreamFieldPanel("social_icons"),
    ]

    def __str__(self):
        return self.name


@register_model_chooser
class Footer(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", null=True, default=None, unique=True)

    form_section_name = models.CharField(max_length=50)
    form_section_caption = models.CharField(max_length=250)
    form_section_social_link = StreamField(
        [("icons", SocialIconLink())], null=True, blank=True
    )

    link_columns = StreamField(
        [("link_column", FooterLinkColumn())], null=True, blank=True
    )

    legal_bar_links = StreamField(
        [("legal_bar", FooterLegalBar())], null=True, blank=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("form_section_name"),
        FieldPanel("form_section_caption"),
        StreamFieldPanel("form_section_social_link"),
        StreamFieldPanel("link_columns"),
        StreamFieldPanel("legal_bar_links"),
    ]

    def __str__(self):
        return self.name


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


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


class HomePage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("intro", HotelIntro()),
            ("image_section", ImageSection()),
            ("split_image_text_card_section", SplitImageTextCardSection()),
            ("full_width_image_card_section", FullWidthImageCardSection()),
            ("home_page_footer", FadeInFooter()),
            ("rich_text_section", blocks.RichTextBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class FormPage(AbstractEmailForm):
    body = StreamField(
        [("hero", Hero()), ("contact_row", ContactCardRow())], null=True, blank=True
    )
    tagline = models.CharField(max_length=50, blank=True)
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    form_intro_image = models.ForeignKey(
        "home.CustomImage",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    content_panels = AbstractEmailForm.content_panels + [
        StreamFieldPanel("body"),
        FieldPanel("to_address"),
        FieldPanel("from_address"),
        FieldPanel("subject"),
        FieldPanel("tagline"),
        FieldPanel("intro"),
        ImageChooserPanel("form_intro_image"),
        InlinePanel("form_fields", label="Form Fields"),
        FieldPanel("thank_you_text"),
    ]


class Contact(models.Model):
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(_("email address"))

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.email)


class HotelsPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("hotels", ImageCardList()),
            ("development", HotelsDevelopment()),
            ("destinations", HotelsDestinations()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class HotelDetailPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("intro", HotelIntro()),
            ("image_section", ImageSection()),
            ("static_text_section", StaticTextSection()),
            ("section_header", SectionHeader()),
            ("block_quote", BlockQuote()),
            ("activity_section", ActivitySection()),
            ("floor_plan_section", FloorPlanSection()),
            ("detail_section", HotelDetailSection()),
            ("fade_in_footer", FadeInFooter()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]

    parent_page_types = [HotelsPage]


class EventsPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("image_section", ImageSection()),
            ("split_image_text_card_section", SplitImageTextCardSection()),
            ("static_text_section", StaticTextSection()),
            ("events_list", ImageCardList()),
            ("events_footer", EventsFooter()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class BrochuresPage(Page):
    body = StreamField(
        [("hero", Hero()), ("action_cards", ActionCardSection())], null=True, blank=True
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class ExperiencesPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("experiences_list", ImageCardList()),
            ("experiences_footer", FadeInFooter()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class ExperiencePage(Page):
    body = StreamField(
        [("hero", Hero()), ("intro", HotelIntro())], null=True, blank=True
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]

    parent_page_types = [ExperiencesPage]


class PressPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("image_logo_link_card_section", ImageLogoLinkCardSection()),
            ("block_quote", BlockQuote()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class MissionPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("split_image_text_card_section", SplitImageTextCardSection()),
            ("full_width_image", FullWidthImage()),
            ("mission_footer", BlockQuoteFooter()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class ReservePage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("hotels", ImageCardList()),
            ("footer", HotelsDestinations()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class CareersPage(Page):
    body = StreamField(
        [("hero", Hero()), ("intro", HotelIntro()), ("jobs_list", JobsList())],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class FoundationPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("intro", HotelIntro()),
            ("image_section", ImageSection()),
            ("events_footer", EventsFooter()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class BasicInfoPage(Page):
    body = StreamField(
        [("header", PageHeaderText()), ("body_section", HeaderTextParagraph())],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]
