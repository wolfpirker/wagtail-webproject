from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel

class HomePage(Page):
    """Home page model."""

    templates = "templates/home_page.html"
    max_count = 1 # only one webpage instance

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
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        ImageChooserPanel("banner_image"),
        PageChooserPanel("banner_cta")
    ]

    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
