# -*- coding: utf-8 -*-
from django.conf import settings


CKEDITOR_URL = getattr(settings, 'CKEDITOR_URL', 'ckeditor/ckeditor.js')
# Title of the blog
BLOG_TITLE = getattr(settings, 'BLOG_TITLE', 'A nice blog!')
# If True comments are enabled by default
BLOG_COMMENTS = getattr(settings, 'BLOG_COMMENTS', True)
# Default value for custom css is an empty tuple to give greater flexibility.
# In yours settings.py you should use:
# BLOG_CUSTOM_CSS = ('custom-css.css',) # single css file
# BLOG_CUSTOM_CSS = ('custom-css1.css', 'custom-css2.css') # multiple css
BLOG_CUSTOM_CSS = getattr(settings, 'BLOG_CUSTOM_CSS', ())
