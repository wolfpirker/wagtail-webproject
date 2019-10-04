from django.db import models
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

#from streams import blocks

""" Snippets """
from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

"""Blog listing and blog detail pages."""
from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

class TourCategory(models.Model):
    """Tour category for a snippet"""

    name = models.CharField(max_length=127)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=127,
        help_text='A slug to identify tours by this category',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Tour Category"
        verbose_name_plural = "Tour Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

register_snippet(TourCategory)

class TourProvincesOrderable(Orderable):
    """This allows us to select one or more tour provinces from Snippets."""

    page = ParentalKey("tours.TourPage", related_name="tour_provinces")
    province = models.ForeignKey(
        "tours.TourProvince",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("province"),
    ]

@register_snippet
class TourProvince(models.Model):
    """Tour provinces for snippets."""
    province_name = models.CharField(max_length=31)
    province_website = models.URLField(blank=True, null=True)
    map_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("province_name"),
                ImageChooserPanel("map_image"),
            ],
            heading="Province",
        ),
        MultiFieldPanel(
            [
                FieldPanel("province_website"),
            ],
            heading="Links"
        )
    ]

    def __str__(self):
        """String repr of this class."""
        return self.province_name

    class Meta:  # noqa
        verbose_name = "Province"
        verbose_name_plural = "Provinces"


register_snippet(TourProvince)

class ToursIndexPage(Page):
    template = "tours/tours_index_page.html"
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        tourpages = self.get_children().live().order_by('-first_published_at')
        context['tourpages'] = tourpages
        context['categories'] = TourCategory.objects.all()
        category = request.GET.get('category')
        if category is not None:
            category = category.capitalize()
            tourpages_filtered = TourPage.objects.filter(categories__name=category)
            context['tourpages_filtered'] = tourpages_filtered
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    class Meta:  # noqa
        verbose_name = "Tours Index Page"
        verbose_name_plural = "Tours Index Pages"


class TourPage(Page):
    template = "tours/tour_page.html"

    date = models.DateField("Post date")
    short_description = models.CharField(max_length=255)
    #author = models.CharField(max_length=64)
    body = RichTextField(blank=True)
    tour_duration = models.DurationField(blank=True,null=True,help_text="enter the approximate duration usual for this tour")
    price_low_season = models.IntegerField(blank=True,null=True,help_text="enter the price for the group on low season time [$]")
    price_high_season = models.IntegerField(blank=True,null=True,help_text="enter the price for the group on high season time [$]")
    max_num_people = models.IntegerField(blank=True,null=True,help_text="enter the maximum group size of people")
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    categories = ParentalManyToManyField("tours.TourCategory", blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            ImageChooserPanel("image"),
            InlinePanel("tour_provinces", label="Province", min_num=1, max_num=3),                        
        ], heading="Tour general information"),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        ),
        MultiFieldPanel([
            FieldPanel('tour_duration'),
            FieldPanel('price_low_season'),
            FieldPanel('price_high_season'),
            FieldPanel('max_num_people'),
        ], heading="additional Tour information"),
        FieldPanel('short_description'),
        FieldPanel('body'),
    ]

    class Meta:  # noqa
        verbose_name = "Tour information Page"
        verbose_name_plural = "Tour information Pages"