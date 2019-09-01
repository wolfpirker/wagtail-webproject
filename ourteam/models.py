"""Our team page"""

from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel


class OurteamPage(Page):
    """our Team page"""

    template = "ourteam/ourteam_page.html"

    # @TODO add streamfields
    # content = StreamField()

    subtitle = models.CharField(max_length=100, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]

class Meta:
    verbose_name = "Our Team Page"
    verbose_name_plural = "Our Team Pages"