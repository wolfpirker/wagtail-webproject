from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.search import index

from tours.models import TourDestinationOrderable

#from tours import models as tours_model

# Create your models here.

class DestinationPageCarouselImages(Orderable):
    """ 1 to 4 images for the destination page carousel """
    page = ParentalKey("destinations.DestinationPage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image", 
        # classname of the image, see wagtail documentation
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    panels = [
        ImageChooserPanel("carousel_image"),
    ]

class DestinationsIndexPage(Page):
    template = "destinations/destinations_index_page.html"    
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        all_destinationpages = self.get_children().live().order_by('-first_published_at')
        paginator = Paginator(all_destinationpages, 5)
        page = request.GET.get("page")
        try:
            destinationpages = paginator.page(page)
        except PageNotAnInteger:
            destinationpages = paginator.page(1)
        except EmptyPage:
            destinationpages = paginator.page(paginator.num_pages)
        context['destinationpages'] = destinationpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    
    class Meta:  # noqa
        verbose_name = "Destination Index Page"
        verbose_name_plural = "Destination Index Pages"


class DestinationPage(Page):
    """Destination page model."""

    templates = "destinations/destination_page.html"

    destination_name = models.CharField(max_length=127,blank=False,null=False,help_text="enter the full location name")

    province = models.ForeignKey(
        'tours.TourProvince',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = RichTextField(blank=True)
    use_destination_name_as_map_location = models.BooleanField(default=True,help_text="instead of coordinates use the location name for the map")
    lat_long = models.CharField(blank=True,null=True,
        max_length=36,
        help_text="Comma separated lat/long. (Ex. 64.144367, -21.939182) \
                   Right click Google Maps and select 'What\'s Here'",
        validators=[
            RegexValidator(
                regex='^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$',
                message='Lat Long must be a comma-separated numeric lat and long',
                code='invalid_lat_long'
            ),
        ]
    )

    def get_tours(self):
        '''return tours which include this destination'''
        all_tours = TourDestinationOrderable.objects.filter(destination_pages__title=self.title)
        return all_tours

    # Makes additional context available to the template so that we can access
    # the latitude, longitude and map API key to render the map
    def get_context(self, request):
        context = super(DestinationPage, self).get_context(request)
        if self.use_destination_name_as_map_location:
            context['map_location'] = self.title
        else:
            context['map_location'] = self.lat_long
        return context
    
    def main_image(self):
        carousel_item = self.carousel_images.first()
        if carousel_item:
            return carousel_item.carousel_image
        else: 
            return None

    search_fields = Page.search_fields + [
        index.SearchField('destination_name'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [        
        FieldPanel('destination_name'),
        FieldPanel('body'),
        SnippetChooserPanel('province'),
        FieldPanel('use_destination_name_as_map_location'),
        FieldPanel('lat_long'),
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=4, min_num=1, label="Image"),
        ], heading="Caroursel images")
    ]

    class Meta:

        verbose_name = "Destination Page"
        verbose_name_plural = "Destination Pages"