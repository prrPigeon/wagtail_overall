from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from streams import blocks 


class BlogListingPage(Page):
    """List all the blog detail pages"""
    template = "blog/blog_listing_page.html"
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Default Title"
    )

    content_panels = Page.content_panels + [ 
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        """ IT IS NEEDED TO CREATE THIS CONTEXT BECAUSE context VAR IS WHAT WE LOOP IN TEMPLATE, and you will loop
        over the posts"""
        context["posts"] = BlogDetailPage.objects.live().public()
        return context


class BlogDetailPage(Page):
    """Blog detail page, BECAUSE IN THIS CLASS THERE IS NO GET CONTEXT, TO GET THIS VARS YOU MUST USE self"""
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Default Title"
    )
    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    content = StreamField(
    [ 
        ("title_and_text", blocks.TitleAndTextBlock()),
        ("full_richtext", blocks.RichtextBlock()),
        ("simple_richtext", blocks.LimitedRichtextBlock()),
        ("cards", blocks.CardBlock()),
        ("cta", blocks.CTABlock())
    ],
    null=True,
    blank=True,
    )

    content_panels = Page.content_panels + [ 
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        StreamFieldPanel("content")
    ]