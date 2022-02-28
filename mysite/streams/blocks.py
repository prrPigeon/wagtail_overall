from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    """ Title and text and nothing else."""
    title = blocks.CharBlock(required=True, help_text="Add you title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features.
    But when is full, someone can add JS and fuck us with cross scripting!!!"""

    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full Richtext"


class LimitedRichtextBlock(blocks.RichTextBlock):
    """Richtext without all the features. But there is shorter way in the CTABlock example"""
    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        """ Init from the main class, then overwrite self.features """
        super().__init__(**kwargs)
        self.features = [ 
            "bold",
            "italic",
            "link"
        ]

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple Richtext"


class CardBlock(blocks.StructBlock):
    """Card with images and text. """
    title = blocks.CharBlock(required=True, help_text="Add you title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [ 
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False, help_text="Cao cao cao")),
            ]
        )
    )

    class Meta:
        template = "streams/cards.html"
        icon = "placeholder"
        label = "Expensive Lightbulbs"


class CTABlock(blocks.StructBlock):
    """ Simple call to action section"""
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text =  blocks.CharBlock(required=True, default="Read More", max_length=60)

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"



class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls, 'I think this will be some kind of help to ButtonBlock class' """

    def url(self):
        button_page = self.get("button_page")
        button_url = self.get("button_url")
        # return page.url if page else external_url
        if button_url:
            return button_url
        else:
            return button_page.url

        # def latest_posts(self):
        """ Caling a BlogDetailPage causes circular import, must investigate about it"""
        #     return BlogDetailPage.objects.live()[:3]

class ButtonBlock(blocks.StructBlock):
    """To avoid writing logic inside template, you can write a custom StreamField logic"""
    button_page = blocks.PageChooserBlock(required=False, help_text="if selected, this url will be used first")
    button_url = blocks.URLBlock(required=False, help_text="if added, this url will be used secondarily to button page")
    

    class Meta:
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue
