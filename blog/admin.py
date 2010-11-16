# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _


from blog import settings
from blog.models import Category, Entry, Link

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

class EntryAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('title', 'pub_date', 'status', 'author', 'enable_comments')
    search_fields = ['title', 'author', 'author__first_name',
                     'author__last_name', 'author__email']
    list_filter = ('status', 'enable_comments', 'featured')

    prepopulated_fields = {'slug': ['title']}

    fieldsets = [
        (None, {'fields': ['title', 'body', 'status']}),
        (_('Date information'), {'fields': ['pub_date'],
                                 'classes': ['collapse']}),
        (_('Options'), {'fields': ['slug', 'featured', 'enable_comments',
                                   'categories', 'tags'],
                        'classes': ['collapse', 'closed']}),
    ]

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(EntryAdmin, self).has_change_permission(
            request, obj
        )

        if not has_class_permission:
            return False

        if (obj is not None and
            not request.user.is_superuser and
            request.user.id != obj.author.id):
                return False

        return True

    def queryset(self, request):
        if request.user.is_superuser:
            return Entry.objects.all()
        return Entry.objects.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    formfield_overrides = {
        models.TextField:
            {'widget': forms.Textarea(attrs={'class': 'ckeditor'})},
    }

    class Media:
        css = {'all': settings.BLOG_CUSTOM_CSS}
        js = [settings.CKEDITOR_URL]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link)
