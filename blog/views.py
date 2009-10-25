# -*- coding: utf-8 -*-
from django.views.generic.date_based import object_detail

from blog.models import Entry

def enhanced_object_detail(*args, **kwargs):
    '''Show entries with DRAFT or HIDDEN status if user.is_staff is True'''

    request = args[0]

    if request.user.is_staff:
        entry_info = {
            'queryset': Entry.objects.all(),
            'date_field': 'pub_date',
            'month_format': '%m',
        }

        kwargs.update(entry_info)
        return object_detail(*args, **kwargs)

    return object_detail(*args, **kwargs)
