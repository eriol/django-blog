# -*- coding: utf-8 -*-
from distutils.core import setup

from blog import VERSION

setup(name='blog',
      version=VERSION,
      description='A simple blog app for django',
      author='Daniele Tricoli',
      author_email='eriol@mornie.org',
      package_dir={'blog': 'blog'},
      packages=['blog', 'blog.conf', 'blog.templatetags']
     )
