# -*- coding: utf-8 -*-
from django.views.generic.dates import DateDetailView


from blog.models import Entry


class EnhancedDateDetailView(DateDetailView):
    """Show entries with DRAFT or HIDDEN status if user.is_staff is True"""

    date_field = 'pub_date'
    month_format = '%m'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Entry.objects.all()
        else:
            return Entry.live.all()
