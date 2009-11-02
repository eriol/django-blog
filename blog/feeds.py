# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed

from blog.models import Category, Entry

class LatestEntriesFeed(Feed):
    title = '%s: latest entries' % settings.BLOG_TITLE

    def items(self):
        return Entry.live.all()[:10]

    def link(self, obj):
        return reverse('blog_entry_index')

    def item_pubdate(self, item):
        return item.pub_date

    def item_author_name(self, item):
        return item.author

class CategoryFeed(LatestEntriesFeed):

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Category.objects.get(slug__exact=bits[0])

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def title(self, obj):
        return '%s: latest entries in category "%s"' % (settings.BLOG_TITLE,
                                                        obj.name)

    def items(self, obj):
        return obj.entries.all()[:10]
