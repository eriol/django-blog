# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin

from tinymce.widgets import TinyMCE

from blog.models import Category, Entry, Link

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

class EntryForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
    )

    class Meta:
        model = Entry

class EntryAdmin(admin.ModelAdmin):
    form = EntryForm
    prepopulated_fields = {'slug': ['title']}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link)