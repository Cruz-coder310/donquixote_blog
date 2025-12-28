import markdown
from django import template
from django.utils.html import mark_safe

from ..models import Post

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    # TODO: This is unsafe for user input. add sanitization (bleach) later.
    html = markdown.markdown(text)
    return mark_safe(html)


@register.simple_tag
def get_post_count():
    post_count = Post.published.count()
    return post_count


@register.inclusion_tag("chronicles/latest_posts.html")
def get_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}
