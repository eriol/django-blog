# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from blog import VERSION

setup(
    name='blog',
    version=VERSION,
    description='A simple blog app for Django.',
    author='Daniele Tricoli',
    author_email='eriol@mornie.org',
    packages=find_packages(),
    package_data = {
        'blog': [
            'locale/*/LC_MESSAGES/*',
            'templates/flatpages/*',
        ],
    },
)
