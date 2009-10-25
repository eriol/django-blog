# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin

from tinymce.widgets import TinyMCE

from blog.models import Category, Entry, Link

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

class EntryForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCE(attrs={'cols': 100, 'rows': 30})
    )

    class Meta:
        model = Entry

class EntryAdmin(admin.ModelAdmin):
    exclude = ('author',)
    form = EntryForm
    list_display = ('title', 'pub_date', 'status', 'author')
    prepopulated_fields = {'slug': ['title']}

    fieldsets = [
        (None, {'fields': ['title', 'body', 'status', 'categories']}),
        ('Date information', {'fields': ['pub_date'],
                              'classes': ['collapse']}),
        ('Options', {'fields': ['slug', 'featured', 'enable_comments', 'tags'],
                     'classes': ['collapse']}),
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

admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link)
