# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from blog import get_version

setup(
    name='blog',
    version=get_version(),
    description='A simple blog app for Django.',
    author='Daniele Tricoli',
    author_email='eriol@mornie.org',
    packages=find_packages(),
    package_data = {
        'blog': [
            'locale/*/LC_MESSAGES/*',
        ],
    },
)
