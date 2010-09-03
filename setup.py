# -*- coding: utf-8 -*-
import os

from distutils.core import setup

from blog import VERSION


main_pkg = 'blog'
packages = []
data_files = []

for root, dirnames, files in os.walk(main_pkg):
    # Remove hidden directories
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in files:
        pkg = root.replace(os.path.sep, '.')
        packages.append(pkg)
    elif files:
        for data_file in files:
            # Strip main_pkg/ from the path
            path = root[len(main_pkg) + 1:]
            data_files.append(os.path.join(path, data_file))


setup(name='blog',
      version=VERSION,
      description='A simple blog app for django',
      author='Daniele Tricoli',
      author_email='eriol@mornie.org',
      packages=packages,
      package_dir={'blog': main_pkg},
      package_data={'blog': data_files},
     )
