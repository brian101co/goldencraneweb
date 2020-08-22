import readtime

from django.db import models
from django.utils import timezone
from django.db.models import Count

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks as wagtail_blocks
from streams import blocks

class BlogPage(Page):
    post_title = models.CharField(
        blank=False,
        max_length=120,
    )

    featured = models.BooleanField(default=False)

    published_date = models.DateTimeField(default=timezone.now)

    author = models.CharField(max_length=100)

    preview_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
        help_text="The preview image."
    )

    summary = models.TextField(
        blank=False,
        max_length=300,
        help_text="A brief summary of the article for the post listing."
    )

    internal_page_link = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text="Select and internal page to link too.",
        on_delete=models.SET_NULL,
    )

    main_content = StreamField([
        ("blockquote", blocks.BlockquoteBlock()),
        ("Richtext", wagtail_blocks.RichTextBlock(
            template="streams/simple_richtext_block.html",
            features=["bold", "italic", "h1", "h2", "h3", "ol", "ul", "link"]
        )),
        ("ImageAndText", blocks.ImageAndTextBlock()),
    ],
    null=True,
    blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel("post_title"),
        FieldPanel("published_date"),
        FieldPanel("author"),
        ImageChooserPanel("preview_image"),
        FieldPanel("summary"),
        StreamFieldPanel("main_content"),
        FieldPanel("featured"),
        
    ]

    def get_read_time(self):
        string = str(self.main_content)
        result = readtime.of_html(string)
        return result
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = BlogPage.objects.live().public().exclude(id=self.id)[:4]
        context["posts"] = posts
        return context
