from django.db import models
from blog.models import BlogPage
from project.models import ProjectPage
from testimonials.models import Testimonial

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

class HomePage(Page):
    banner_title = models.CharField(
        max_length=200,
        help_text="Main banner title.",
        null=True,
    )
    banner_subtitle = models.CharField(
        max_length=250,
        help_text="Banner subtitle.",
        null=True,
    )
    banner_button_text = models.CharField(
        max_length=60,
        help_text="CTA button text.",
        null=True,
    )
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name="+",
        help_text="Banner background image.",
        on_delete=models.SET_NULL,
    )
    promise_subtitle = models.CharField(
        max_length=200,
        help_text="Our promise subtitle.",
        null=True,
    )
    web_design_body = models.TextField(
        max_length=400,
        help_text="Web design card body text.",
        null=True,
    )
    web_dev_body = models.TextField(
        max_length=400,
        help_text="Web dev card body text.",
        null=True,
    )
    logo_design_body = models.TextField(
        max_length=400,
        help_text="Logo Design card body text.",
        null=True,
    )
    web_hosting_body = models.TextField(
        max_length=400,
        help_text="Web hosting card body text.",
        null=True,
    )
    seo_body = models.TextField(
        max_length=400,
        help_text="SEO card body text.",
        null=True,
    )
    media_man_body = models.TextField(
        max_length=400,
        help_text="Media management card body text.",
        null=True,
    )
    banner_bottom_title = models.CharField(
        max_length=200,
        help_text="Bottom banner title.",
        null=True,
    )
    banner_bottom_subtitle = models.CharField(
        max_length=250,
        help_text="Bottom banner subtitle.",
        null=True,
    )
    banner_bottom_cta = models.CharField(
        max_length=60,
        help_text="CTA button text.",
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        FieldPanel("banner_button_text"),
        ImageChooserPanel("banner_image"),
        FieldPanel("promise_subtitle"),
        FieldPanel("web_design_body"),
        FieldPanel("web_dev_body"),
        FieldPanel("logo_design_body"),
        FieldPanel("web_hosting_body"),
        FieldPanel("seo_body"),
        FieldPanel("media_man_body"),
        FieldPanel("banner_bottom_title"),
        FieldPanel("banner_bottom_subtitle"),
        FieldPanel("banner_bottom_cta"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["projects"] = ProjectPage.objects.live().public().filter(featured=True)[:4]
        context["posts"] = BlogPage.objects.live().public().filter(featured=True)[:4]
        context["testimonials"] = Testimonial.objects.all()[:3]
        return context
