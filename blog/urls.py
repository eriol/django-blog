# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from blog.models import Category, Entry

entry_info = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
}
entry_info_month = dict(entry_info, month_format='%m')

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 'archive_index', entry_info, 'blog_entry_index'),
    (r'^(?P<year>\d{4})/$', 'archive_year', entry_info,
     'blog_entry_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', entry_info_month,
     'blog_entry_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'archive_day',
     entry_info_month, 'blog_entry_archive_day'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
     'object_detail', entry_info_month, 'blog_entry_detail'),
)
