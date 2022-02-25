from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks


class HomePage(Page):
    """ Home page model """
    template = "home/home_page.html"
    max_count = 1

    banner_title  = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic"])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    # on flex/models this one is cta
    link_to_other_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    # this content is copied from streams/models.FlexPage, also
    # it's needed to do migrations
    content = StreamField(
    [ 
        # ("title_and_text", blocks.TitleAndTextBlock()),
        # ("full_richtext", blocks.RichtextBlock()),
        # ("simple_richtext", blocks.LimitedRichtextBlock()),
        # ("cards", blocks.CardBlock()),
        ("cta", blocks.CTABlock())
    ],
    null=True,
    blank=True,
    )

    content_panels = Page.content_panels + [ 
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        ImageChooserPanel("banner_image"),
        PageChooserPanel("link_to_other_page"),
        StreamFieldPanel("content")
    ]

    class Meta:
        verbose_name = "Home page"
