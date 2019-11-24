"""Our team page"""

from django.db import models
from django import forms

# django contact form
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse # Add this
from .forms import ContactForm

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel

from wagtail.core.fields import RichTextField
from wagtail.search import index

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    StreamFieldPanel, 
    FieldPanel, 
    InlinePanel, 
    FieldRowPanel,
    MultiFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from streams import blocks
from django.utils.text import slugify

class GuideQualification(models.Model):
    """Guide qualification for a snippet"""

    qualification = models.CharField(max_length=127)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=127,
        help_text='A slug to identify guides by this qualification',
    )

    panels = [
        FieldPanel("qualification"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Guide Qualification"
        verbose_name_plural = "Guide Qualifications"
        ordering = ["qualification"]

    def __str__(self):
        return self.qualification

register_snippet(GuideQualification)

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
    intro = models.CharField(max_length=254, null=True, blank=True)
    body = RichTextField(blank=True)
    qualifications = ParentalManyToManyField("ourteam.GuideQualification", blank=True)
    include_contact_form = models.BooleanField()
    contact_email = models.CharField(max_length=100)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    allow_direct_guide_booking = models.BooleanField(help_text="wether this guide agrees to be booked for an hourly rate plus additional charge")
    hourly_rate_low_season = models.DecimalField(max_digits=4, decimal_places=2,help_text="hourly rate low season")
    hourly_rate_high_season = models.DecimalField(max_digits=4, decimal_places=2,help_text="hourly rate high season")
    additional_charge_per_tour = models.IntegerField(help_text="added charge per group for each tour")
    form = ContactForm()

    main_province = models.ForeignKey(
        'tours.TourProvince',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def clean(self):
        """Override the values of title and slug before saving."""
        super(TourGuidePage, self).clean()
        self.title = "%s %s" % (self.first_name, self.last_name)
        self.slug = slugify(self.title)    

    def contact_us(self, request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                # send email code goes here
                return HttpResponse('Thanks for contacting us!')
        else:
            form = ContactForm()

        return render(request, 'contact-landing.html', {'form': form})

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('qualifications'),
        index.SearchField('guide_tours'),
    ]

    #content_panels = Page.content_panels + [
    content_panels = [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
            FieldPanel('contact_email'),
            FieldPanel('include_contact_form'),
            ImageChooserPanel("image"),
            SnippetChooserPanel("main_province"),
        ], heading="Guide general information"),
        MultiFieldPanel(
            [
                FieldPanel("qualifications", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Guide Qualifications"
        ),
        MultiFieldPanel([
            InlinePanel("guide_tours", label="Tours", min_num=0, max_num=10), 
            FieldPanel('allow_direct_guide_booking'),
            FieldPanel('hourly_rate_low_season'),
            FieldPanel('hourly_rate_high_season'),
            FieldPanel('additional_charge_per_tour'),
        ], heading="Tours Specification"),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

TourGuidePage._meta.get_field('slug').default = 'blank-slug'