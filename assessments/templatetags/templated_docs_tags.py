# --coding: utf8--

import os.path

from django.db.models.fields.files import ImageFieldFile
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django import template
register = template.Library()

PIXEL_TO_CM = 0.00846666


class ImageNode(template.Node):
    def __init__(self, value):
        self.value = template.Variable(value)

    def render(self, context):
        try:
            self.value = self.value.resolve(context)
            if not isinstance(self.value, ImageFieldFile):
                raise template.VariableDoesNotExist(
                    'Image argument should be an ImageField')
            images = context.dicts[0].setdefault('ootemplate_imgs', {})
            #for image in images:
            #    print("from loop: " + str(image))

            id = len(images)
            #print(id)
            z_index = id + 3  # Magic
            width = self.value.width * PIXEL_TO_CM

            height = self.value.height * PIXEL_TO_CM
            filename = os.path.basename(self.value.name)
            #print(filename + " width: " + str(width))
            #print(filename + " height: " + str(height))

            basename = os.path.splitext(filename)[0]
            #print(basename)

            images[self.value.path] = self.value
            #print(self.value)
            #print(images[self.value.path])
            return ('<draw:frame draw:style-name="gr%(z_index)s" '
                    'draw:name="%(basename)s" '
                    'draw:id="id%(id)s" '
                    'text:anchor-type="char" svg:width="%(width)fcm" '
                    'svg:height="%(height)fcm" draw:z-index="%(z_index)s">'
                    '<draw:image xlink:href="Pictures/%(filename)s" '
                    'xlink:type="simple" xlink:show="embed" '
                    'xlink:actuate="onLoad"/></draw:frame>') % locals()
        except template.VariableDoesNotExist:
            print("template variable does not exist")
            return ''


@register.tag
def image(parser, token):
    """
    Insert an image from a ImageField into a document.
    """
    try:
        tag_name, value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires a file as an argument' % tag_name)
    #print(str(ImageNode(value)))
    return ImageNode(value)
''

@register.filter
def lolinebreaks(value):
    """
    LibreOffice-flavored ``linebreaks`` filter.
    """
    if not value:
        return ''
    paragraphs = [line for line in escape(value).splitlines()]
    return mark_safe('<text:line-break/>'.join(paragraphs))
