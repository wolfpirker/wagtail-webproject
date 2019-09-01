"""Streamfield live in here."""

from wagtail.core import blocks

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""

# just replace models with blocks, replace fields with block
    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta: # noqa
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"

class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Full RichText"