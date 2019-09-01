"""Our team page"""

from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

from wagtail.core.fields import RichTextField
from wagtail.search import index

from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from streams import blocks

class OurteamPage(Page):
    """our Team page"""

    template = "ourteam/ourteam_page.html"

    subtitle = models.CharField(max_length=100, null=True, blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock())
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