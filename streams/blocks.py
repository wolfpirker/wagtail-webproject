"""Streamfield live in here."""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""

# just replace models with blocks, replace fields with block
    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"

class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Full RichText"

class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)"""
    title = blocks.CharBlock(required=True, help_text="Add your title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=48)),
                ("text", blocks.TextBlock(required=True, max_length=256)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False, help_text="if the button page above is selected, that will be used first")), 
            ]
        ))

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Staff cards"