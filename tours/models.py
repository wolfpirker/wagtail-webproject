from django.db import models
from django import forms
from django.utils import dateparse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

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

from ourteam.models import GuideToursOrderable

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

class TourDestinationOrderable(Orderable):

    page = ParentalKey("tours.TourPage", related_name="tour_destinations")
    destination_pages = models.ForeignKey(
        "destinations.DestinationPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    def __str__(self):
        return self.page.title

#class TourProvincesOrderable(Orderable):
#    """This allows us to select one or more tour provinces from Snippets."""
#
#    page = ParentalKey("tours.TourPage", related_name="tour_provinces")
#    province = models.ForeignKey(
#        "tours.TourProvince",
#        on_delete=models.CASCADE,
#    )

#    panels = [
#        SnippetChooserPanel("province"),
#    ]

@register_snippet
class TourProvince(models.Model):
    """Tour provinces for snippets."""
    province_name = models.CharField(max_length=31)

    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=31,
        help_text='A slug to identify tours by this category',
    )
    
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
                FieldPanel("slug"),
                ImageChooserPanel("map_image"),
            ],
            heading="Province",
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
        all_tourpages = self.get_children().live().order_by('-first_published_at')
        paginator = Paginator(all_tourpages, 5)
        page = request.GET.get("page")
        try:
            tourpages = paginator.page(page)
        except PageNotAnInteger:
            tourpages = paginator.page(1)
        except EmptyPage:
            tourpages = paginator.page(paginator.num_pages)
        context['tourpages'] = tourpages
        
        context['categories'] = TourCategory.objects.all()
        context['provinces'] = TourProvince.objects.all()
        category = request.GET.get('category')
        province = request.GET.get('province')
        tourpages_filtered = []
        if category is not None:
            category = category.lower()        
            tourpages_filtered = TourPage.objects.filter(categories__slug=category)
        if province is not None:
            province = province.lower()
            if category is None:
                #tourpages_filtered = TourPage.objects.filter(tour_provinces__province=province)
                tourpages_filtered = TourPage.objects.filter(provinces__slug=province)
            else:
                tourpages_filtered = TourPage.objects.filter(categories__slug=category, provinces__slug=province)            
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
    body = RichTextField(blank=True)
    tour_duration = models.DurationField(blank=True,null=True,help_text="duration usual for this tour - type as 'DD HH:MM:SS' or 'HH:MM:SS'")
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

    def get_guide(self):
        '''return tours which include this destination'''
        all_guides = GuideToursOrderable.objects.filter(tours_pages__title=self.title)
        return all_guides

    def save(self, *args, **kwargs):
        """Create a template fragment key.
        Then delete the key."""
        key = make_template_fragment_key(
            "tour_preview",  # Matches the name of our template fragment in the blog_listing_page.html
            [self.id]  # Matches the post.id in the template for loop (shown below)
        )
        cache.delete(key)
        return super().save(*args, **kwargs)

    def get_readable_tour_duration(self):
        duration = dateparse.parse_duration(str(self.tour_duration))
        minutes = duration.seconds / 60
        if duration.days > 0:
            # assumes that it just whole days, without added hours
            return str(duration.days) + " days"
        elif minutes >= 60:            
            # assume that each tour duration is at least an hour
            hours = minutes / 60
            if int(hours)*60 == minutes:
                # full hours
                return str(int(hours)) + " hours"
            else:
                rest_min = minutes - int(hours)*60
                if rest_min == 30:
                    return str(int(hours)) + " 1/2 hours"
                else:
                    return str(int(hours)) + " hours, " + str(rest_min) + " minutes"
            return 
        else:
            return None

    categories = ParentalManyToManyField("tours.TourCategory", blank=True)
    provinces = ParentalManyToManyField("tours.TourProvince", blank=True)

    def destinations_exist(self):
        if len(self.tour_destinations.all()) == 0:
            return False
        return True       

    def get_destination_page(self):
        destinations = [
            n.destination_pages for n in self.tour_destinations.all()
        ]
        return destinations
    
    def get_province_names(self):
        p = [
            n.province.province_name for n in self.provinces.all()
        ]
        return p

    def get_province_names_as_string(self):
        '''Tour could take place in several provinces, 
        so I need a method to get it...'''
        provinces_str = ''
        for province in self.get_province_names():
            provinces_str += province + ', ' 
        provinces_str = provinces_str[:-2]
        return provinces_str

 # neu!

    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            ImageChooserPanel("image"),
            #InlinePanel("provinces", label="Province", min_num=1, max_num=3),                        
        ], heading="Tour general information"),
        MultiFieldPanel(
            [
                FieldPanel("provinces", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Provinces"
        ),
        MultiFieldPanel([
            InlinePanel("tour_destinations", label="Destinations", min_num=0, max_num=6), 
        ], heading="Tour Destinations"),
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