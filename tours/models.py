from django.db import models

from modelcluster.fields import ParentalKey
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
    province_name = models.CharField(max_length=32)
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
    short_description = models.CharField(max_length=256)
    #author = models.CharField(max_length=64)
    body = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            ImageChooserPanel("image"),
            InlinePanel("tour_provinces", label="Province", min_num=1, max_num=3),            
        ], heading="Tour information"),
        FieldPanel('short_description'),
        FieldPanel('body'),
    ]

    class Meta:  # noqa
        verbose_name = "Tour information Page"
        verbose_name_plural = "Tour information Pages"