from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
        FieldPanel, PageChooserPanel, 
        StreamFieldPanel, InlinePanel,
        MultiFieldPanel
    )
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
# import which will enable routable page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from streams import blocks



class HomePageCarouselImages(Orderable):
    """Orderable first class, render between 1 and 5 images"""
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [ 
        ImageChooserPanel('carousel_image')
    ]


class HomePage(RoutablePageMixin, Page):
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
        MultiFieldPanel([
            # moved from list to MultiFieldPanel
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            ImageChooserPanel("banner_image"),
            PageChooserPanel("link_to_other_page"),
        ], heading="Banner Options"),
        # FieldPanel("banner_title"),
        # FieldPanel("banner_subtitle"),
        # ImageChooserPanel("banner_image"),
        # PageChooserPanel("link_to_other_page"),
        StreamFieldPanel("content"),
        #InlinePanel("carousel_images"), # removed to InlinePanel
        # MultiFieldPanel is to rearrange interface in admin panel
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=5, min_num=1, label="Image"), # by related name, don't forget
        ], heading="Carousel Images"),
    ]

    class Meta:
        verbose_name = "Home page"

    # this one will overwrite home page is route is /, but if you add name of the route it will be blog/subscribe
    # and here we will add already created Subscriber model
    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["a_special_text"] = "Hello world 123123"
        return render(request, "home/subscribe.html", context)