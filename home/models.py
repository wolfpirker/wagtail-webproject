from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel, 
    FieldRowPanel,
    PageChooserPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
    InlinePanel,    
)
from wagtail.snippets.models import register_snippet

from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from .blocks import BaseStreamBlock

class HomePageCarouselImages(Orderable):
    """ 1 to 5 images for the home page carousel """
    page = ParentalKey("home.HomePage", related_name="carousel_images")
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

class HomePage(Page):
    """Home page model."""

    templates = "templates/home_page.html"
    # max_count = 1 # only one webpage instance

    # fields cannot be blank in the form, but in database null is OK
    banner_title = models.CharField(max_length=100, blank=False, null=True)
        # Note: models is specific to Django, django.db := models
    banner_subtitle = RichTextField(features=["bold", "italic"]) # wagtail specific
    banner_image = models.ForeignKey(
        "wagtailimages.Image", 
        # classname of the image, see wagtail documentation
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    # cta: banner call to action, link to another page 
    # link to another wagtail page we have not created yet
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            ImageChooserPanel("banner_image"),
            PageChooserPanel("banner_cta"),  
        ], heading="Banner Options"),             
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=6, min_num=0, label="Image"),
        ], heading="Caroursel images")
    ]

    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

#from bakerydemo
@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Footer Text'

#from bakerydemo
class StandardPage(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = RichTextField(features=["bold", "italic"])

    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
]

# from bakerydemo:
class FormField(AbstractFormField):
    """
    Wagtailforms is a module to introduce simple forms on a Wagtail site. It
    isn't intended as a replacement to Django's form support but as a quick way
    to generate a general purpose data-collection form or contact form
    without having to write code. We use it on the site for a contact form. You
    can read more about Wagtail forms at:
    http://docs.wagtail.io/en/latest/reference/contrib/forms/index.html
    """
    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)

class FormPage(AbstractEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    body = StreamField(BaseStreamBlock())
    thank_you_text = RichTextField(blank=True)

    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
