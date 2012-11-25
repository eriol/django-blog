# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from blog.feeds import LatestEntriesFeed, CategoryFeed
from blog.models import Category, Entry

entry_info = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
}

entry_info_month = dict(entry_info, month_format='%m')

category_info = {
    'queryset': Category.objects.all(),
}

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 'archive_index', entry_info, 'blog_entry_index'),
    (r'^(?P<year>\d{4})/$', 'archive_year', entry_info,
     'blog_entry_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'archive_month', entry_info_month,
     'blog_entry_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', 'archive_day',
     entry_info_month, 'blog_entry_archive_day'),
)

urlpatterns += patterns('',
    (r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
     'blog.views.enhanced_object_detail', entry_info_month, 'blog_entry_detail'),
)

urlpatterns += patterns('django.views.generic.list_detail',
    (r'^category/(?P<slug>[-\w]+)/$', 'object_detail', category_info,
     'blog_category_detail'),
)

urlpatterns += patterns('',
    url(r'^feeds/entries/$', LatestEntriesFeed(), name='latest-entries-feed'),
    url(r'^feeds/category/(?P<slug>[-\w]+)/$',
        CategoryFeed(),
        name='latest-category-entries-feed'),
)
