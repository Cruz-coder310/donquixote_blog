import markdown
from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    # TODO: This is unsafe for user input. add sanitization (bleach) later.
    html = markdown.markdown(text)
    return mark_safe(html)
