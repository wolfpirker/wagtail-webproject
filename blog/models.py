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

"""Blog Author Snippet."""
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

class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("blog.BlogPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
    	# Use a SnippetChooserPanel because blog.BlogAuthor is registered as a snippet
        SnippetChooserPanel("author"),
    ]

@register_snippet
class BlogAuthor(models.Model):
    """Blog author for snippets."""
    # from learning wagtail lesson "Registering snippets"
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading="Name and Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        )
    ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:  # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


register_snippet(BlogAuthor)

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogTagIndexPage(Page):
    
    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    #author = models.CharField(max_length=64)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]