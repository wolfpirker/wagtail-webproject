"""Our team page"""

from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel

from wagtail.core.fields import RichTextField
from wagtail.search import index


from modelcluster.fields import ParentalKey
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from streams import blocks

class GuideToursOrderable(Orderable):
    page = ParentalKey("ourteam.TourGuidePage", related_name="guide_tours")
    tours_pages = models.ForeignKey(
        "tours.TourPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    def __str__(self):
        return self.page.title

class OurteamPage(Page):
    """our Team page"""

    template = "ourteam/ourteam_page.html"

    subtitle = models.CharField(max_length=100, null=True, blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("cards", blocks.CardBlock()),
        ],
        null=True,
        blank=True

    )

    # body = RichTextField(help_text='Add your main text, you can embed images')

    search_fields = Page.search_fields + [
        index.SearchField('subtitle'),
    #    index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content")
    ]

    class Meta:
        verbose_name = "Our Team Page"
        verbose_name_plural = "Our Team Pages"

class TourGuidePage(Page):
    template = "ourteam/tourguide_page.html"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    body = RichTextField(blank=True)
    include_contact_form = models.BooleanField()
    contact_email = models.CharField(max_length=100)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    allow_direct_guide_booking = models.BooleanField(help_text="wether this guide agrees to be booked for the hourly rate plus additional charge")
    hourly_rate_low_season = models.IntegerField(help_text="hourly rate low season")
    hourly_rate_high_season = models.IntegerField(help_text="hourly rate high season")
    additional_charge_per_tour = models.IntegerField(help_text="added charge per group for each tour")

    main_province = models.ForeignKey(
        'tours.TourProvince',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
            FieldPanel('contact_email'),
            FieldPanel('include_contact_form'),
            ImageChooserPanel("image"),
            SnippetChooserPanel("main_province"),
        ], heading="Guide general information"),
        MultiFieldPanel([
            InlinePanel("guide_tours", label="Tours", min_num=0, max_num=10), 
            FieldPanel('allow_direct_guide_booking'),
            FieldPanel('hourly_rate_low_season'),
            FieldPanel('hourly_rate_high_season'),
            FieldPanel('additional_charge_per_tour'),
        ], heading="Tours Specification"),
        FieldPanel('body'),
    ]