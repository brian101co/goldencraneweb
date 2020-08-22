from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class ImageAndTextBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        help_text="An image.",
    )
    title = blocks.CharBlock(max_length=100)

    class Meta:
        template="streams/image_and_text_block.html"
        icon = "image"
        label = "Image & Text"

class BlockquoteBlock(blocks.StructBlock):
    text = blocks.TextBlock(
        required=True,
        help_text="Quote to be display on the page."
    )

    attribution = blocks.CharBlock(
        max_length=100,
        help_text="Attribution",
    )

    class Meta:
        template = "streams/blockquote_block.html"
        icon = "openquote"
        label = "Blockquote"
        help_text =  "A full width quote to display on the page."