import json
from collections import OrderedDict
from django.core.serializers.json import DjangoJSONEncoder
# from django import forms
from django.db import models  # NOQA
from django.forms import Field, FileField, HiddenInput
from django.forms.fields import CharField, EmailField
from django.utils.decorators import method_decorator
from django.utils.six import text_type
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from modelcluster.fields import ParentalKey
from salesforce import models as SFModels
from unidecode import unidecode
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         StreamFieldPanel)
from wagtail.contrib.forms.forms import BaseForm
from wagtail.contrib.forms.forms import FormBuilder as WagtailFormBuilder
from wagtail.contrib.forms.models import FORM_FIELD_CHOICES, AbstractEmailForm
from wagtail.contrib.forms.models import AbstractFormField as WagtailFormField
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtailcache.cache import WagtailCacheMixin, cache_page
from wagtailmodelchooser import register_model_chooser

from .constants import CACHE_STRING, ENVIRONMENT_CHOICES

from .blocks import (  # isort:skip
    ActionCardSection,
    ActivitySection,
    BlockQuote,
    BlockQuoteFooter,
    ButtonBlock,
    ContactCardRow,
    EmbedVideoBlock,
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
    ResortThingsToKnow,
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
    on_scroll_image_2 = models.ForeignKey(
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
    on_load_mobile_image_2 = models.ForeignKey(
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
        ImageChooserPanel("on_load_mobile_image_2"),
        ImageChooserPanel("on_scroll_image"),
        ImageChooserPanel("on_scroll_image_2"),
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


class FormBuilder(WagtailFormBuilder):
    def create_singleline_field(self, field, options):
        options["max_length"] = field.max_length
        return CharField(**options)

    def create_multiline_field(self, field, options):
        options["max_length"] = field.max_length
        return super(FormBuilder, self).create_multiline_field(field, options)

    def create_email_field(self, field, options):
        options["max_length"] = field.max_length
        return EmailField(**options)

    def create_blank_field(self, field, options):
        return Field(label="Blank", widget=HiddenInput, required=False)

    def create_file_field(self, field, options):
        return FileField(**options)

    def create_phone_field(self, field, options):
        options["max_length"] = field.max_length
        return CharField(**options)

    def create_header_field(self, field, options):
        options.pop("required")
        field = Field(widget=HiddenInput, required=False, **options)
        field.is_header = True
        return field

    def create_file_upload_field(self, field, options):
        return FileField(**options)

    def get_form_class(self):
        new_formfields = OrderedDict()
        for key in self.formfields:
            for field in self.fields:
                if key == field.clean_name:
                    formfield = self.formfields[key]
                    if field.display_label:
                        formfield.display_label = field.display_label
                    if field.italic_help:
                        formfield.italic_help = field.italic_help
                    if field.full_width:
                        formfield.full_width = field.full_width
                    if field.half_width:
                        formfield.half_width = field.half_width
                    new_formfields[key] = formfield
        return type(str("WagtailForm"), (BaseForm,), new_formfields)


class AbstractFormField(WagtailFormField):
    """
    Database Fields required for building a Django Form field.
    """

    label = models.CharField(
        verbose_name=_("label"),
        max_length=255,
        help_text=_(
            "MUST BE UNIQUE. The label that will be associated with the data on the back-end."
        ),
    )
    field_type = models.CharField(
        verbose_name=_("field type"), max_length=16, choices=FORM_FIELD_CHOICES
    )
    display_label = models.CharField(
        verbose_name=_("display label"),
        max_length=255,
        blank=True,
        help_text=_(
            "The label that the user will see. Does not need to be unique. If left blank, Label will be displayed to the user."
        ),
    )
    italic_help = models.BooleanField(
        default=False, help_text="Should the help text for the field show up in italics"
    )
    full_width = models.BooleanField(default=False)
    half_width = models.BooleanField(default=False)
    max_length = models.IntegerField(
        default=255,
        help_text="IMPORTANT!! Typically should be set to '255', but if the field is a comment text area set this to '131072'.",
    )
    # '131072' is the character count for a 'Text Field (Long)' in SalesForce

    @property
    def clean_name(self):
        # unidecode will return an ascii string while slugify wants a
        # unicode string on the other hand, slugify returns a safe-string
        # which will be converted to a normal str
        return str(slugify(text_type(unidecode(self.label))))

    panels = WagtailFormField.panels + [
        FieldPanel("display_label"),
        FieldPanel("italic_help"),
        FieldPanel("full_width"),
        FieldPanel("half_width"),
        FieldPanel("max_length"),
    ]

    class Meta:
        abstract = True
        ordering = ["sort_order"]


class FormField(AbstractFormField):
    FORM_FIELD_CHOICES = list(FORM_FIELD_CHOICES) + [("file", "Upload File")]
    field_type = models.CharField(
        verbose_name=_("field type"), max_length=16, choices=FORM_FIELD_CHOICES
    )
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
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class SalesForceFile(models.Model):
    file_upload = models.FileField(upload_to="uploads/%Y/%m/%d/")


class FormPage(AbstractEmailForm):
    form_builder = FormBuilder

    def process_form_submission(self, form):
        """
        Processes the form submission, if an Image upload is found, pull out the
        files data, create an actual Wgtail Image and reference its ID only in the
        stored form response.
        """

        cleaned_data = form.cleaned_data
        for name, field in form.fields.items():
            if isinstance(field, FileField):
                file_data = cleaned_data[name]
                if file_data:

                    new_file_upload = SalesForceFile.objects.create(
                        file_upload=file_data
                    )

                    cleaned_data.update({name: new_file_upload.file_upload.url})

                else:
                    del cleaned_data[name]

        submission = self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder), page=self,
        )
        return submission

    body = StreamField(
        [
            ("hero", Hero()),
            ("contact_row", ContactCardRow()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
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


class EventsFormPage(FormPage):
    def process_form_submission(self, form):
        """
        Accepts form instance with submitted data, user and page.
        Creates submission instance.
        You can override this method if you want to have custom creation logic.
        For example, if you want to save reference to a user.
        """
        # import ipdb

        # ipdb.set_trace()
        submission = super().process_form_submission(form)
        EventResponses.objects.create(**form.cleaned_data)
        return submission

    events_body = StreamField(
        [("things_to_know", ResortThingsToKnow()),], null=True, blank=True
    )

    content_panels = FormPage.content_panels + [StreamFieldPanel("events_body")]


class GuestProfileFormPage(FormPage):
    def process_form_submission(self, form):
        """
        Accepts form instance with submitted data, user and page.
        Creates submission instance.
        You can override this method if you want to have custom creation logic.
        For example, if you want to save reference to a user.
        """

        submission = super().process_form_submission(form)

        for key, value in form.cleaned_data.items():
            if isinstance(value, list):
                form.cleaned_data[key] = ", ".join(value)

        GuestProfileResponses.objects.create(**form.cleaned_data)
        return submission


class Contact(models.Model):
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(_("email address"))

    def process_contact_footer_form_submission(self, form):
        """
        Processes the form submission, if an Image upload is found, pull out the
        files data, create an actual Wgtail Image and reference its ID only in the
        stored form response.
        """
        """
        Accepts form instance with submitted data, user and page.
        Creates submission instance.
        You can override this method if you want to have custom creation logic.
        For example, if you want to save reference to a user.
        """

        cleaned_data = form.cleaned_data
        for name, field in form.fields.items():
            if isinstance(field, FileField):
                file_data = cleaned_data[name]
                if file_data:
                    new_file_upload = SalesForceFile.objects.create(
                        file_upload=file_data
                    )
                    cleaned_data.update({name: new_file_upload.file_upload.url})
                else:
                    del cleaned_data[name]
        FooterContactResponses.objects.create(**form.cleaned_data)

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.email)

@method_decorator(cache_page, name="serve")
class HotelsPage(WagtailCacheMixin, Page):
    cache_control = CACHE_STRING


@method_decorator(cache_page, name="serve")
class HotelsPage(WagtailCacheMixin, Page):
    cache_control = CACHE_STRING

    body = StreamField(
        [
            ("hero", Hero()),
            ("hotels", ImageCardList()),
            ("development", HotelsDevelopment()),
            ("destinations", HotelsDestinations()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


hotel_base_blocks = [
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
    ("button_block", ButtonBlock()),
    ("rich_text_section", blocks.RichTextBlock()),
    ("video_section", EmbedVideoBlock()),
]

@method_decorator(cache_page, name="serve")
class HotelDetailPage(Page):
    cache_control = CACHE_STRING

    body = StreamField(hotel_base_blocks, null=True, blank=True,)
    content_panels = Page.content_panels + [StreamFieldPanel("body")]
    parent_page_types = [HotelsPage]


class HotelEventsPage(Page):
    body = StreamField(
        hotel_base_blocks + [("events_footer", EventsFooter())], null=True, blank=True,
    )
    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class EventsPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("image_section", ImageSection()),
            ("split_image_text_card_section", SplitImageTextCardSection()),
            ("static_text_section", StaticTextSection()),
            ("events_list", ImageCardList()),
            ("events_footer", EventsFooter()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class BrochuresPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("action_cards", ActionCardSection()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class ExperiencesPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("experiences_list", ImageCardList()),
            ("experiences_footer", FadeInFooter()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class ExperiencePage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("intro", HotelIntro()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]

    parent_page_types = [ExperiencesPage]


class PressPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("image_logo_link_card_section", ImageLogoLinkCardSection()),
            ("block_quote", BlockQuote()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]

@method_decorator(cache_page, name='serve')
class MissionPage(WagtailCacheMixin, Page):
    cache_control = CACHE_STRING


@method_decorator(cache_page, name="serve")
class MissionPage(WagtailCacheMixin, Page):
    cache_control = CACHE_STRING

    body = StreamField(
        [
            ("hero", Hero()),
            ("split_image_text_card_section", SplitImageTextCardSection()),
            ("full_width_image", FullWidthImage()),
            ("mission_footer", BlockQuoteFooter()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
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
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class CareersPage(Page):
    body = StreamField(
        [
            ("hero", Hero()),
            ("intro", HotelIntro()),
            ("jobs_list", JobsList()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
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
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class BasicInfoPage(Page):
    body = StreamField(
        [
            ("header", PageHeaderText()),
            ("body_section", HeaderTextParagraph()),
            ("rich_text_section", blocks.RichTextBlock()),
            ("video_section", EmbedVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]


class EventResponses(SFModels.Model):
    """This is pulled directly from salesforce after creating it there. This should
    only be edited if the salesforce form changes."""

    company = models.CharField(
        db_column="company__c",
        max_length=255,
        verbose_name="company",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        db_column="last_name__c",
        max_length=255,
        verbose_name="last_name",
        blank=True,
        null=True,
    )
    city = models.CharField(
        db_column="city__c", max_length=255, verbose_name="city", blank=True, null=True
    )
    phone = models.CharField(
        db_column="phone__c", max_length=25, verbose_name="phone", blank=True, null=True
    )
    salutation = models.CharField(
        db_column="salutation__c",
        max_length=255,
        verbose_name="salutation",
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        db_column="first_name__c",
        max_length=255,
        verbose_name="first_name",
        blank=True,
        null=True,
    )
    preferred_date = models.DateField(
        db_column="preferred_date__c",
        verbose_name="preferred_date",
        blank=True,
        null=True,
    )
    flexible_dates = models.BooleanField(
        db_column="flexible_dates__c",
        verbose_name="flexible_dates",
        default=SFModels.DefaultedOnCreate(False),
    )
    state = models.CharField(
        db_column="state__c",
        max_length=255,
        verbose_name="state",
        blank=True,
        null=True,
    )
    alternate_date = models.DateField(
        db_column="alternate_date__c",
        verbose_name="alternate_date",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        db_column="email__c", verbose_name="email", blank=True, null=True
    )
    additional_comments = models.CharField(
        db_column="additional_comments__c",
        max_length=131072,
        verbose_name="additional_comments",
        blank=True,
        null=True,
    )
    # '131072' is the character count for a 'Text Field (Long)' in SalesForce
    referral = models.CharField(
        db_column="referral__c",
        max_length=255,
        verbose_name="referral",
        blank=True,
        null=True,
    )
    petite_resort = models.CharField(
        db_column="petite_resort__c",
        max_length=255,
        verbose_name="petite_resort",
        blank=True,
        null=True,
    )
    number_of_guests = models.DecimalField(
        db_column="number_of_guests__c",
        max_digits=18,
        decimal_places=0,
        verbose_name="number_of_guests",
        blank=True,
        null=True,
    )
    number_of_guest_rooms = models.DecimalField(
        db_column="number_of_guest_rooms__c",
        max_digits=18,
        decimal_places=0,
        verbose_name="number_of_guest_rooms",
        blank=True,
        null=True,
    )
    number_of_nights = models.DecimalField(
        db_column="number_of_nights__c",
        max_digits=18,
        decimal_places=0,
        verbose_name="number_of_nights",
        blank=True,
        null=True,
    )
    address = models.CharField(
        db_column="address__c",
        max_length=255,
        verbose_name="address",
        blank=True,
        null=True,
    )
    zip_code = models.CharField(
        db_column="zip_code__c",
        max_length=255,
        verbose_name="zip_code",
        blank=True,
        null=True,
    )
    event_type = models.CharField(
        db_column="event_type__c",
        max_length=255,
        verbose_name="event_type",
        blank=True,
        null=True,
    )
    country = models.CharField(
        db_column="country__c",
        max_length=255,
        verbose_name="country",
        blank=True,
        null=True,
    )
    contact_method = models.CharField(
        db_column="contact_method__c",
        max_length=255,
        verbose_name="contact_method",
        blank=True,
        null=True,
    )
    file_upload = models.URLField(
        db_column="file_upload__c",
        max_length=255,
        verbose_name="file_upload",
        blank=True,
        null=True,
    )
    submission_date = models.DateTimeField(
        db_column="Submission_date__c",
        verbose_name="Submission date",
        blank=True,
        null=True,
    )

    class Meta(SFModels.Model.Meta):
        db_table = "eventresponses__c"
        verbose_name = "Event Response"
        verbose_name_plural = "Event Responses"
        # keyPrefix = 'a0I'


class GuestProfileResponses(SFModels.Model):
    """This is pulled directly from salesforce after creating it there. This should
    only be edited if the salesforce form changes."""

    additional_comments = models.CharField(
        db_column="additional_comments__c",
        max_length=32768,
        verbose_name="additional_comments",
        blank=True,
        null=True,
    )
    allergies = models.CharField(
        db_column="allergies__c",
        max_length=255,
        verbose_name="allergies",
        blank=True,
        null=True,
    )
    dining_time = models.CharField(
        db_column="dining_time__c",
        max_length=255,
        verbose_name="dining_time",
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        db_column="first_name__c",
        max_length=255,
        verbose_name="first_name",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        db_column="last_name__c",
        max_length=255,
        verbose_name="last_name",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        db_column="email__c",
        max_length=255,
        verbose_name="email",
        blank=True,
        null=True,
    )
    number_of_adults = models.CharField(
        db_column="number_of_adults__c",
        max_length=255,
        verbose_name="number_of_adults",
        blank=True,
        null=True,
    )
    number_of_children = models.CharField(
        db_column="number_of_children__c",
        max_length=255,
        verbose_name="number_of_children",
        blank=True,
        null=True,
    )
    adult_first_1 = models.CharField(
        db_column="adult_first_1__c",
        max_length=255,
        verbose_name="adult_first_1",
        blank=True,
        null=True,
    )
    adult_first_2 = models.CharField(
        db_column="adult_first_2__c",
        max_length=255,
        verbose_name="adult_first_2",
        blank=True,
        null=True,
    )
    adult_first_3 = models.CharField(
        db_column="adult_first_3__c",
        max_length=255,
        verbose_name="adult_first_3",
        blank=True,
        null=True,
    )
    adult_first_4 = models.CharField(
        db_column="adult_first_4__c",
        max_length=255,
        verbose_name="adult_first_4",
        blank=True,
        null=True,
    )
    adult_first_5 = models.CharField(
        db_column="adult_first_5__c",
        max_length=255,
        verbose_name="adult_first_5",
        blank=True,
        null=True,
    )
    adult_first_6 = models.CharField(
        db_column="adult_first_6__c",
        max_length=255,
        verbose_name="adult_first_6",
        blank=True,
        null=True,
    )
    adult_first_7 = models.CharField(
        db_column="adult_first_7__c",
        max_length=255,
        verbose_name="adult_first_7",
        blank=True,
        null=True,
    )
    adult_first_8 = models.CharField(
        db_column="adult_first_8__c",
        max_length=255,
        verbose_name="adult_first_8",
        blank=True,
        null=True,
    )
    adult_first_9 = models.CharField(
        db_column="adult_first_9__c",
        max_length=255,
        verbose_name="adult_first_9",
        blank=True,
        null=True,
    )
    adult_first_10 = models.CharField(
        db_column="adult_first_10__c",
        max_length=255,
        verbose_name="adult_first_10",
        blank=True,
        null=True,
    )
    adult_last_1 = models.CharField(
        db_column="adult_last_1__c",
        max_length=255,
        verbose_name="adult_last_1",
        blank=True,
        null=True,
    )
    adult_last_2 = models.CharField(
        db_column="adult_last_2__c",
        max_length=255,
        verbose_name="adult_last_2",
        blank=True,
        null=True,
    )
    adult_last_3 = models.CharField(
        db_column="adult_last_3__c",
        max_length=255,
        verbose_name="adult_last_3",
        blank=True,
        null=True,
    )
    adult_last_4 = models.CharField(
        db_column="adult_last_4__c",
        max_length=255,
        verbose_name="adult_last_4",
        blank=True,
        null=True,
    )
    adult_last_5 = models.CharField(
        db_column="adult_last_5__c",
        max_length=255,
        verbose_name="adult_last_5",
        blank=True,
        null=True,
    )
    adult_last_6 = models.CharField(
        db_column="adult_last_6__c",
        max_length=255,
        verbose_name="adult_last_6",
        blank=True,
        null=True,
    )
    adult_last_7 = models.CharField(
        db_column="adult_last_7__c",
        max_length=255,
        verbose_name="adult_last_7",
        blank=True,
        null=True,
    )
    adult_last_8 = models.CharField(
        db_column="adult_last_8__c",
        max_length=255,
        verbose_name="adult_last_8",
        blank=True,
        null=True,
    )
    adult_last_9 = models.CharField(
        db_column="adult_last_9__c",
        max_length=255,
        verbose_name="adult_last_9",
        blank=True,
        null=True,
    )
    adult_last_10 = models.CharField(
        db_column="adult_last_10__c",
        max_length=255,
        verbose_name="adult_last_10",
        blank=True,
        null=True,
    )
    adult_bday_1 = models.CharField(
        db_column="adult_bday_1__c",
        max_length=255,
        verbose_name="adult_bday_1",
        blank=True,
        null=True,
    )
    adult_bday_2 = models.CharField(
        db_column="adult_bday_2__c",
        max_length=255,
        verbose_name="adult_bday_2",
        blank=True,
        null=True,
    )
    adult_bday_3 = models.CharField(
        db_column="adult_bday_3__c",
        max_length=255,
        verbose_name="adult_bday_3",
        blank=True,
        null=True,
    )
    adult_bday_4 = models.CharField(
        db_column="adult_bday_4__c",
        max_length=255,
        verbose_name="adult_bday_4",
        blank=True,
        null=True,
    )
    adult_bday_5 = models.CharField(
        db_column="adult_bday_5__c",
        max_length=255,
        verbose_name="adult_bday_5",
        blank=True,
        null=True,
    )
    adult_bday_6 = models.CharField(
        db_column="adult_bday_6__c",
        max_length=255,
        verbose_name="adult_bday_6",
        blank=True,
        null=True,
    )
    adult_bday_7 = models.CharField(
        db_column="adult_bday_7__c",
        max_length=255,
        verbose_name="adult_bday_7",
        blank=True,
        null=True,
    )
    adult_bday_8 = models.CharField(
        db_column="adult_bday_8__c",
        max_length=255,
        verbose_name="adult_bday_8",
        blank=True,
        null=True,
    )
    adult_bday_9 = models.CharField(
        db_column="adult_bday_9__c",
        max_length=255,
        verbose_name="adult_bday_9",
        blank=True,
        null=True,
    )
    adult_bday_10 = models.CharField(
        db_column="adult_bday_10__c",
        max_length=255,
        verbose_name="adult_bday_10",
        blank=True,
        null=True,
    )
    adult_shoe_1 = models.CharField(
        db_column="adult_shoe_1__c",
        max_length=255,
        verbose_name="adult_shoe_1",
        blank=True,
        null=True,
    )
    adult_shoe_2 = models.CharField(
        db_column="adult_shoe_2__c",
        max_length=255,
        verbose_name="adult_shoe_2",
        blank=True,
        null=True,
    )
    adult_shoe_3 = models.CharField(
        db_column="adult_shoe_3__c",
        max_length=255,
        verbose_name="adult_shoe_3",
        blank=True,
        null=True,
    )
    adult_shoe_4 = models.CharField(
        db_column="adult_shoe_4__c",
        max_length=255,
        verbose_name="adult_shoe_4",
        blank=True,
        null=True,
    )
    adult_shoe_5 = models.CharField(
        db_column="adult_shoe_5__c",
        max_length=255,
        verbose_name="adult_shoe_5",
        blank=True,
        null=True,
    )
    adult_shoe_6 = models.CharField(
        db_column="adult_shoe_6__c",
        max_length=255,
        verbose_name="adult_shoe_6",
        blank=True,
        null=True,
    )
    adult_shoe_7 = models.CharField(
        db_column="adult_shoe_7__c",
        max_length=255,
        verbose_name="adult_shoe_7",
        blank=True,
        null=True,
    )
    adult_shoe_8 = models.CharField(
        db_column="adult_shoe_8__c",
        max_length=255,
        verbose_name="adult_shoe_8",
        blank=True,
        null=True,
    )
    adult_shoe_9 = models.CharField(
        db_column="adult_shoe_9__c",
        max_length=255,
        verbose_name="adult_shoe_9",
        blank=True,
        null=True,
    )
    adult_shoe_10 = models.CharField(
        db_column="adult_shoe_10__c",
        max_length=255,
        verbose_name="adult_shoe_10",
        blank=True,
        null=True,
    )
    adult_height_1 = models.CharField(
        db_column="adult_height_1__c",
        max_length=255,
        verbose_name="adult_height_1",
        blank=True,
        null=True,
    )
    adult_height_2 = models.CharField(
        db_column="adult_height_2__c",
        max_length=255,
        verbose_name="adult_height_2",
        blank=True,
        null=True,
    )
    adult_height_3 = models.CharField(
        db_column="adult_height_3__c",
        max_length=255,
        verbose_name="adult_height_3",
        blank=True,
        null=True,
    )
    adult_height_4 = models.CharField(
        db_column="adult_height_4__c",
        max_length=255,
        verbose_name="adult_height_4",
        blank=True,
        null=True,
    )
    adult_height_5 = models.CharField(
        db_column="adult_height_5__c",
        max_length=255,
        verbose_name="adult_height_5",
        blank=True,
        null=True,
    )
    adult_height_6 = models.CharField(
        db_column="adult_height_6__c",
        max_length=255,
        verbose_name="adult_height_6",
        blank=True,
        null=True,
    )
    adult_height_7 = models.CharField(
        db_column="adult_height_7__c",
        max_length=255,
        verbose_name="adult_height_7",
        blank=True,
        null=True,
    )
    adult_height_8 = models.CharField(
        db_column="adult_height_8__c",
        max_length=255,
        verbose_name="adult_height_8",
        blank=True,
        null=True,
    )
    adult_height_9 = models.CharField(
        db_column="adult_height_9__c",
        max_length=255,
        verbose_name="adult_height_9",
        blank=True,
        null=True,
    )
    adult_height_10 = models.CharField(
        db_column="adult_height_10__c",
        max_length=255,
        verbose_name="adult_height_10",
        blank=True,
        null=True,
    )
    adult_weight_1 = models.CharField(
        db_column="adult_weight_1__c",
        max_length=255,
        verbose_name="adult_weight_1",
        blank=True,
        null=True,
    )
    adult_weight_2 = models.CharField(
        db_column="adult_weight_2__c",
        max_length=255,
        verbose_name="adult_weight_2",
        blank=True,
        null=True,
    )
    adult_weight_3 = models.CharField(
        db_column="adult_weight_3__c",
        max_length=255,
        verbose_name="adult_weight_3",
        blank=True,
        null=True,
    )
    adult_weight_4 = models.CharField(
        db_column="adult_weight_4__c",
        max_length=255,
        verbose_name="adult_weight_4",
        blank=True,
        null=True,
    )
    adult_weight_5 = models.CharField(
        db_column="adult_weight_5__c",
        max_length=255,
        verbose_name="adult_weight_5",
        blank=True,
        null=True,
    )
    adult_weight_6 = models.CharField(
        db_column="adult_weight_6__c",
        max_length=255,
        verbose_name="adult_weight_6",
        blank=True,
        null=True,
    )
    adult_weight_7 = models.CharField(
        db_column="adult_weight_7__c",
        max_length=255,
        verbose_name="adult_weight_7",
        blank=True,
        null=True,
    )
    adult_weight_8 = models.CharField(
        db_column="adult_weight_8__c",
        max_length=255,
        verbose_name="adult_weight_8",
        blank=True,
        null=True,
    )
    adult_weight_9 = models.CharField(
        db_column="adult_weight_9__c",
        max_length=255,
        verbose_name="adult_weight_9",
        blank=True,
        null=True,
    )
    adult_weight_10 = models.CharField(
        db_column="adult_weight_10__c",
        max_length=255,
        verbose_name="adult_weight_10",
        blank=True,
        null=True,
    )
    child_first_1 = models.CharField(
        db_column="child_first_1__c",
        max_length=255,
        verbose_name="child_first_1",
        blank=True,
        null=True,
    )
    child_first_2 = models.CharField(
        db_column="child_first_2__c",
        max_length=255,
        verbose_name="child_first_2",
        blank=True,
        null=True,
    )
    child_first_3 = models.CharField(
        db_column="child_first_3__c",
        max_length=255,
        verbose_name="child_first_3",
        blank=True,
        null=True,
    )
    child_first_4 = models.CharField(
        db_column="child_first_4__c",
        max_length=255,
        verbose_name="child_first_4",
        blank=True,
        null=True,
    )
    child_first_5 = models.CharField(
        db_column="child_first_5__c",
        max_length=255,
        verbose_name="child_first_5",
        blank=True,
        null=True,
    )
    child_first_6 = models.CharField(
        db_column="child_first_6__c",
        max_length=255,
        verbose_name="child_first_6",
        blank=True,
        null=True,
    )
    child_first_7 = models.CharField(
        db_column="child_first_7__c",
        max_length=255,
        verbose_name="child_first_7",
        blank=True,
        null=True,
    )
    child_first_8 = models.CharField(
        db_column="child_first_8__c",
        max_length=255,
        verbose_name="child_first_8",
        blank=True,
        null=True,
    )
    child_first_9 = models.CharField(
        db_column="child_first_9__c",
        max_length=255,
        verbose_name="child_first_9",
        blank=True,
        null=True,
    )
    child_first_10 = models.CharField(
        db_column="child_first_10__c",
        max_length=255,
        verbose_name="child_first_10",
        blank=True,
        null=True,
    )
    child_last_1 = models.CharField(
        db_column="child_last_1__c",
        max_length=255,
        verbose_name="child_last_1",
        blank=True,
        null=True,
    )
    child_last_2 = models.CharField(
        db_column="child_last_2__c",
        max_length=255,
        verbose_name="child_last_2",
        blank=True,
        null=True,
    )
    child_last_3 = models.CharField(
        db_column="child_last_3__c",
        max_length=255,
        verbose_name="child_last_3",
        blank=True,
        null=True,
    )
    child_last_4 = models.CharField(
        db_column="child_last_4__c",
        max_length=255,
        verbose_name="child_last_4",
        blank=True,
        null=True,
    )
    child_last_5 = models.CharField(
        db_column="child_last_5__c",
        max_length=255,
        verbose_name="child_last_5",
        blank=True,
        null=True,
    )
    child_last_6 = models.CharField(
        db_column="child_last_6__c",
        max_length=255,
        verbose_name="child_last_6",
        blank=True,
        null=True,
    )
    child_last_7 = models.CharField(
        db_column="child_last_7__c",
        max_length=255,
        verbose_name="child_last_7",
        blank=True,
        null=True,
    )
    child_last_8 = models.CharField(
        db_column="child_last_8__c",
        max_length=255,
        verbose_name="child_last_8",
        blank=True,
        null=True,
    )
    child_last_9 = models.CharField(
        db_column="child_last_9__c",
        max_length=255,
        verbose_name="child_last_9",
        blank=True,
        null=True,
    )
    child_last_10 = models.CharField(
        db_column="child_last_10__c",
        max_length=255,
        verbose_name="child_last_10",
        blank=True,
        null=True,
    )
    child_bday_1 = models.CharField(
        db_column="child_bday_1__c",
        max_length=255,
        verbose_name="child_bday_1",
        blank=True,
        null=True,
    )
    child_bday_2 = models.CharField(
        db_column="child_bday_2__c",
        max_length=255,
        verbose_name="child_bday_2",
        blank=True,
        null=True,
    )
    child_bday_3 = models.CharField(
        db_column="child_bday_3__c",
        max_length=255,
        verbose_name="child_bday_3",
        blank=True,
        null=True,
    )
    child_bday_4 = models.CharField(
        db_column="child_bday_4__c",
        max_length=255,
        verbose_name="child_bday_4",
        blank=True,
        null=True,
    )
    child_bday_5 = models.CharField(
        db_column="child_bday_5__c",
        max_length=255,
        verbose_name="child_bday_5",
        blank=True,
        null=True,
    )
    child_bday_6 = models.CharField(
        db_column="child_bday_6__c",
        max_length=255,
        verbose_name="child_bday_6",
        blank=True,
        null=True,
    )
    child_bday_7 = models.CharField(
        db_column="child_bday_7__c",
        max_length=255,
        verbose_name="child_bday_7",
        blank=True,
        null=True,
    )
    child_bday_8 = models.CharField(
        db_column="child_bday_8__c",
        max_length=255,
        verbose_name="child_bday_8",
        blank=True,
        null=True,
    )
    child_bday_9 = models.CharField(
        db_column="child_bday_9__c",
        max_length=255,
        verbose_name="child_bday_9",
        blank=True,
        null=True,
    )
    child_bday_10 = models.CharField(
        db_column="child_bday_10__c",
        max_length=255,
        verbose_name="child_bday_10",
        blank=True,
        null=True,
    )
    child_shoe_1 = models.CharField(
        db_column="child_shoe_1__c",
        max_length=255,
        verbose_name="child_shoe_1",
        blank=True,
        null=True,
    )
    child_shoe_2 = models.CharField(
        db_column="child_shoe_2__c",
        max_length=255,
        verbose_name="child_shoe_2",
        blank=True,
        null=True,
    )
    child_shoe_3 = models.CharField(
        db_column="child_shoe_3__c",
        max_length=255,
        verbose_name="child_shoe_3",
        blank=True,
        null=True,
    )
    child_shoe_4 = models.CharField(
        db_column="child_shoe_4__c",
        max_length=255,
        verbose_name="child_shoe_4",
        blank=True,
        null=True,
    )
    child_shoe_5 = models.CharField(
        db_column="child_shoe_5__c",
        max_length=255,
        verbose_name="child_shoe_5",
        blank=True,
        null=True,
    )
    child_shoe_6 = models.CharField(
        db_column="child_shoe_6__c",
        max_length=255,
        verbose_name="child_shoe_6",
        blank=True,
        null=True,
    )
    child_shoe_7 = models.CharField(
        db_column="child_shoe_7__c",
        max_length=255,
        verbose_name="child_shoe_7",
        blank=True,
        null=True,
    )
    child_shoe_8 = models.CharField(
        db_column="child_shoe_8__c",
        max_length=255,
        verbose_name="child_shoe_8",
        blank=True,
        null=True,
    )
    child_shoe_9 = models.CharField(
        db_column="child_shoe_9__c",
        max_length=255,
        verbose_name="child_shoe_9",
        blank=True,
        null=True,
    )
    child_shoe_10 = models.CharField(
        db_column="child_shoe_10__c",
        max_length=255,
        verbose_name="child_shoe_10",
        blank=True,
        null=True,
    )
    child_height_1 = models.CharField(
        db_column="child_height_1__c",
        max_length=255,
        verbose_name="child_height_1",
        blank=True,
        null=True,
    )
    child_height_2 = models.CharField(
        db_column="child_height_2__c",
        max_length=255,
        verbose_name="child_height_2",
        blank=True,
        null=True,
    )
    child_height_3 = models.CharField(
        db_column="child_height_3__c",
        max_length=255,
        verbose_name="child_height_3",
        blank=True,
        null=True,
    )
    child_height_4 = models.CharField(
        db_column="child_height_4__c",
        max_length=255,
        verbose_name="child_height_4",
        blank=True,
        null=True,
    )
    child_height_5 = models.CharField(
        db_column="child_height_5__c",
        max_length=255,
        verbose_name="child_height_5",
        blank=True,
        null=True,
    )
    child_height_6 = models.CharField(
        db_column="child_height_6__c",
        max_length=255,
        verbose_name="child_height_6",
        blank=True,
        null=True,
    )
    child_height_7 = models.CharField(
        db_column="child_height_7__c",
        max_length=255,
        verbose_name="child_height_7",
        blank=True,
        null=True,
    )
    child_height_8 = models.CharField(
        db_column="child_height_8__c",
        max_length=255,
        verbose_name="child_height_8",
        blank=True,
        null=True,
    )
    child_height_9 = models.CharField(
        db_column="child_height_9__c",
        max_length=255,
        verbose_name="child_height_9",
        blank=True,
        null=True,
    )
    child_height_10 = models.CharField(
        db_column="child_height_10__c",
        max_length=255,
        verbose_name="child_height_10",
        blank=True,
        null=True,
    )
    child_weight_1 = models.CharField(
        db_column="child_weight_1__c",
        max_length=255,
        verbose_name="child_weight_1",
        blank=True,
        null=True,
    )
    child_weight_2 = models.CharField(
        db_column="child_weight_2__c",
        max_length=255,
        verbose_name="child_weight_2",
        blank=True,
        null=True,
    )
    child_weight_3 = models.CharField(
        db_column="child_weight_3__c",
        max_length=255,
        verbose_name="child_weight_3",
        blank=True,
        null=True,
    )
    child_weight_4 = models.CharField(
        db_column="child_weight_4__c",
        max_length=255,
        verbose_name="child_weight_4",
        blank=True,
        null=True,
    )
    child_weight_5 = models.CharField(
        db_column="child_weight_5__c",
        max_length=255,
        verbose_name="child_weight_5",
        blank=True,
        null=True,
    )
    child_weight_6 = models.CharField(
        db_column="child_weight_6__c",
        max_length=255,
        verbose_name="child_weight_6",
        blank=True,
        null=True,
    )
    child_weight_7 = models.CharField(
        db_column="child_weight_7__c",
        max_length=255,
        verbose_name="child_weight_7",
        blank=True,
        null=True,
    )
    child_weight_8 = models.CharField(
        db_column="child_weight_8__c",
        max_length=255,
        verbose_name="child_weight_8",
        blank=True,
        null=True,
    )
    child_weight_9 = models.CharField(
        db_column="child_weight_9__c",
        max_length=255,
        verbose_name="child_weight_9",
        blank=True,
        null=True,
    )
    child_weight_10 = models.CharField(
        db_column="child_weight_10__c",
        max_length=255,
        verbose_name="child_weight_10",
        blank=True,
        null=True,
    )
    off_ranch_add_on_activities = models.CharField(
        db_column="off_ranch_add_on_activities__c",
        max_length=32768,
        verbose_name="off_ranch_add_on_activities",
        blank=True,
        null=True,
    )
    on_ranch_add_on_activities = models.CharField(
        db_column="on_ranch_add_on_activities__c",
        max_length=32768,
        verbose_name="on_ranch_add_on_activities",
        blank=True,
        null=True,
    )
    coffee_preference = models.CharField(
        db_column="coffee_preference__c",
        max_length=255,
        verbose_name="coffee_preference",
        blank=True,
        null=True,
    )
    music_preference = models.CharField(
        db_column="music_preference__c",
        max_length=255,
        verbose_name="music_preference",
        blank=True,
        null=True,
    )
    wine_preference = models.CharField(
        db_column="wine_preference__c",
        max_length=255,
        verbose_name="wine_preference",
        blank=True,
        null=True,
    )
    phone = models.CharField(
        db_column="phone__c",
        max_length=255,
        verbose_name="phone",
        blank=True,
        null=True,
    )
    reservation = models.CharField(
        db_column="reservation__c",
        max_length=255,
        verbose_name="reservation",
        blank=True,
        null=True,
    )
    spa_activities = models.CharField(
        db_column="spa_activities__c",
        max_length=255,
        verbose_name="spa_activities",
        blank=True,
        null=True,
    )
    special_occasions = models.CharField(
        db_column="special_occasions__c",
        max_length=32768,
        verbose_name="special_occasions",
        blank=True,
        null=True,
    )
    transportation = models.CharField(
        db_column="transportation__c",
        max_length=255,
        verbose_name="transportation",
        blank=True,
        null=True,
    )
    renting_car = models.CharField(
        db_column="renting_car__c",
        max_length=255,
        verbose_name="renting_car",
        blank=True,
        null=True,
    )
    booked_car = models.CharField(
        db_column="booked_car__c",
        max_length=255,
        verbose_name="booked_car",
        blank=True,
        null=True,
    )
    party_eta = models.CharField(
        db_column="party_eta__c",
        max_length=255,
        verbose_name="party_eta",
        blank=True,
        null=True,
    )
    arrival_location = models.CharField(
        db_column="arrival_location__c",
        max_length=255,
        verbose_name="arrival_location",
        blank=True,
        null=True,
    )
    arrival_flight_date = models.CharField(
        db_column="arrival_flight_date__c",
        max_length=255,
        verbose_name="arrival_flight_date",
        blank=True,
        null=True,
    )
    arrival_flight_time = models.CharField(
        db_column="arrival_flight_time__c",
        max_length=255,
        verbose_name="arrival_flight_time",
        blank=True,
        null=True,
    )
    arrival_airline = models.CharField(
        db_column="arrival_airline__c",
        max_length=255,
        verbose_name="arrival_airline",
        blank=True,
        null=True,
    )
    arrival_flight_number = models.CharField(
        db_column="arrival_flight_number__c",
        max_length=255,
        verbose_name="arrival_flight_number",
        blank=True,
        null=True,
    )
    departure_location = models.CharField(
        db_column="departure_location__c",
        max_length=255,
        verbose_name="departure_location",
        blank=True,
        null=True,
    )
    departure_flight_date = models.CharField(
        db_column="departure_flight_date__c",
        max_length=255,
        verbose_name="departure_flight_date",
        blank=True,
        null=True,
    )
    departure_flight_time = models.CharField(
        db_column="departure_flight_time__c",
        max_length=255,
        verbose_name="departure_flight_time",
        blank=True,
        null=True,
    )
    departure_airline = models.CharField(
        db_column="departure_airline__c",
        max_length=255,
        verbose_name="departure_airline",
        blank=True,
        null=True,
    )
    departure_flight_number = models.CharField(
        db_column="departure_flight_number__c",
        max_length=255,
        verbose_name="departure_flight_number",
        blank=True,
        null=True,
    )
    transportation_details = models.CharField(
        db_column="transportation_details__c",
        max_length=32768,
        verbose_name="transportation_details",
        blank=True,
        null=True,
    )
    package_activites = models.CharField(
        db_column="package_activites__c",
        max_length=32768,
        verbose_name="package_activites",
        blank=True,
        null=True,
    )
    submission_date = models.DateTimeField(
        db_column="Submission_date__c",
        verbose_name="Submission date",
        blank=True,
        null=True,
    )

    class Meta(SFModels.Model.Meta):
        db_table = "guestprofileresponses__c"
        verbose_name = "Guest Profile Response"
        verbose_name_plural = "Guest Profile Responses"
        # keyPrefix = 'a0I'


class FooterContactResponses(SFModels.Model):
    """This is pulled directly from salesforce after creating it there. This should
    only be edited if the salesforce form changes."""

    first_name = models.CharField(
        db_column="first_name__c",
        max_length=255,
        verbose_name="first_name",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        db_column="last_name__c",
        max_length=255,
        verbose_name="last_name",
        blank=True,
        null=True,
    )
    email = models.EmailField(db_column="email__c", verbose_name="email",)

    class Meta(SFModels.Model.Meta):
        db_table = "AR_footer_contact__c"
        verbose_name = "AR Footer Contact Response"
        verbose_name_plural = "AR Footer Contact Responses"
