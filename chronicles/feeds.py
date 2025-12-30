import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from django.utils.feedgenerator import Atom1Feed


from .models import Post


class PostFeed(Feed):
    title = "My Chronicles"
    link = reverse_lazy("chronicles:post_list")
    subtitle = "Updates on changes & additions to My Chronicles"
    feed_type = Atom1Feed

    def items(self):
        return Post.published.order_by("-updated")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_updateddate(self, item):
        return item.updated
