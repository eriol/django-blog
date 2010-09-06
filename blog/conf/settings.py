# -*- coding: utf-8 -*-
from django.conf import settings

TINYMCE_URL = getattr(settings, 'TINYMCE_URL',
                      '/media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js')

TINYMCE_SETUP_URL = getattr(settings, 'TINYMCE_SETUP_URL',
                            '/media/admin/tinymce_setup/tinymce_setup.js')

BLOG_TITLE = getattr(settings, 'BLOG_TITLE', 'A nice blog!')

BLOG_COMMENTS = getattr(settings, 'BLOG_COMMENTS', True)
