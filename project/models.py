from django.db import models
from blog.models import BlogPage

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks as wagtail_blocks
from streams import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

class ProjectPage(Page):
    project_title = models.CharField(
        blank=False,
        max_length=120,
    )

    featured = models.BooleanField(default=False)

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
        help_text="A brief summary of the project."
    )

    external_page_link = models.URLField(
        null=True,
        help_text="Website Link"
    )

    main_content = StreamField([
        ("blockquote", blocks.BlockquoteBlock()),
        ("Richtext", wagtail_blocks.RichTextBlock(
            template="streams/simple_richtext_block.html",
            features=["bold", "italic", "h1", "h2", "h3", "ol", "ul", "link"]
        )),
        ("ImageAndText", blocks.ImageAndTextBlock()),
        ("Testimonial", SnippetChooserBlock(
            target_model='testimonials.Testimonial',
            template="streams/testimonial_block.html"
        ))
    ],
    null=True,
    blank=True,)

    detail_content = StreamField([
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
        FieldPanel("project_title"),
        ImageChooserPanel("preview_image"),
        FieldPanel("summary"),
        StreamFieldPanel("main_content"),
        StreamFieldPanel("detail_content"),
        FieldPanel("external_page_link"),
        FieldPanel("featured")
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["projects"] = ProjectPage.objects.live().public().filter(featured=True).exclude(id=self.id)[:4]
        return context
