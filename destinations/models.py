from django.db import models
from django.core.validators import RegexValidator

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.search import index


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
    lat_long = models.CharField(
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
    
    def main_image(self):
        carousel_item = self.carousel_images.first()
        if carousel_item:
            return carousel_item.image
        else:
            return None
    
    content_panels = Page.content_panels + [
        FieldPanel('destination_name'),
        FieldPanel('body'),
        SnippetChooserPanel('province'),
        FieldPanel('lat_long'),
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=4, min_num=1, label="Image"),
        ], heading="Caroursel images")
    ]

    class Meta:

        verbose_name = "Destination Page"
        verbose_name_plural = "Destination Pages"