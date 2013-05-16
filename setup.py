# -*- coding: utf-8 -*-
# Copyright (C)2007 'jeanmichel FRANCOIS'

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
This module contains the tool of makina.recipe.postgres
"""
import os
from setuptools import setup, find_packages

version = '0.1'

README = os.path.join(os.path.dirname(__file__), 
                      'makina',
                      'recipe',
                      'postgres', 'docs', 'README.txt')

long_description = open(README).read() + '\n\n' 

entry_point = 'makina.recipe.postgres:Recipe'

entry_points = {"zc.buildout": ["default = %s" % entry_point]}

setup(name='makina.recipe.postgres',
      version=version,
      description="Install a postgresql's database for the project",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='postgresql',
      author='jeanmichel FRANCOIS',
      author_email='jeanmichel.francois@makina-corpus.com',
      url='http://www.makina-corpus.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['makina.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zope.testing',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      entry_points=entry_points,
      )
