from django.db import models
from django.shortcuts import render 

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from streams import blocks 


class BlogListingPage(RoutablePageMixin, Page):
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
        context["a_special_link"] = self.reverse_subpage('latest_blog_posts')
        context["regular_context_var"] = "yea yea yea"
        return context


    @route(r'^latest/$')
    def latest_blog_posts(self, request, *args, **kwargs):
        """you can override name of routable page with name as the second parameter in @route()
        @route(r'^latest/$', name="latestposts")
        by adding r'^latest/?$ question mark it will auto correct and add / on the routable page"""
        context = self.get_context(request, *args, **kwargs)
        context["latest_posts"] = BlogDetailPage.objects.live().public()[:1]
        """ YOU CAN ADD HERE WHAT EVER YOU WANT, THIS CONTEXT IS USABEL IN THE TEMPLATES"""
        context["creator"] = "Mijato"
        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request):
        """ overriding sitemap to add RoutablePageMixin page, nad to exclude from sitemap
        just return empty list """
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_blog_posts"),
                # when BlogListingPage is updated count this one too
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9
            }
        )
        return sitemap




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