# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.dates import (
    ArchiveIndexView,
    YearArchiveView,
    MonthArchiveView,
    DayArchiveView
)
from django.views.generic.list import ListView


from blog.feeds import LatestEntriesFeed, CategoryFeed
from blog.models import Category, Entry
from blog.views import EnhancedDateDetailView

entry_info = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
    'paginate_by': 10,
}
entry_info_month = dict(entry_info, month_format='%m')

category_info = {
    'queryset': Category.objects.all(),
    'paginate_by': 10,
}


urlpatterns = patterns('',
    url(r'^$', ArchiveIndexView.as_view(**entry_info), name='blog_entry_index'),
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(**entry_info),
        name='blog_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$',
        MonthArchiveView.as_view(**entry_info_month),
        name = 'blog_entry_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$',
        DayArchiveView.as_view(**entry_info_month),
        name='blog_entry_archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
        EnhancedDateDetailView.as_view(),
        name='blog_entry_detail'),

    url(r'^category/(?P<slug>[-\w]+)/$',
        ListView.as_view(**category_info),
        name='blog_category_detail'),

    # Feeds
    url(r'^feeds/entries/$', LatestEntriesFeed(), name='latest-entries-feed'),
    url(r'^feeds/category/(?P<slug>[-\w]+)/$',
        CategoryFeed(),
        name='latest-category-entries-feed'),
)
