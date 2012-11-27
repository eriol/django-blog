# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from blog import settings
from blog.models import Category, Entry

class LatestEntriesFeed(Feed):
    title = '%s: latest entries' % settings.BLOG_TITLE
    description_template = 'feeds/entries_description.html'

    def items(self):
        return Entry.live.all()[:10]

    def link(self, obj):
        return reverse('blog_entry_index')

    def item_pubdate(self, item):
        return item.pub_date

    def item_author_name(self, item):
        return item.author

class CategoryFeed(LatestEntriesFeed):
    description_template = 'feeds/category_description.html'

    def get_object(self, request, slug):
        return get_object_or_404(Category, slug__exact=slug)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def title(self, obj):
        return '%s: latest entries in category "%s"' % (settings.BLOG_TITLE,
                                                        obj.name)

    def items(self, obj):
        return obj.entries.all()[:10]
