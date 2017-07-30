from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestEntriesFeed(Feed):
    title = "kekerenan.com rss"
    link = "/rss/main"
    description = "kekerenan.com rss 2.0.1  is a Python class that represents a syndication feed."

    def items(self):
        return Post.objects.order_by('-publish')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    # item_link is only needed if Post has no get_absolute_url method.
    #def item_link(self, item):
        #return reverse('', args=[item.pk])
