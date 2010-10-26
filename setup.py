# -*- coding: utf-8 -*-
"""
This module contains the tool of ftw.favorite
"""
from setuptools import setup, find_packages

def read(*rnames):
    return open('/'.join(rnames)).read()

version = open('ftw/favorite/version.txt').read().strip()
maintainer = 'Mathias Leimgruber'

long_description = (
    read('README.txt')
    + '\n\n\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('docs', 'HISTORY.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('ftw', 'favorite', 'README.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='ftw.favorite',
      version=version,
      description="ftw.favorite (Maintainer: %s)" % maintainer,
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='%s, 4teamwork GmbH' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='http://psc.4teamwork.ch/4teamwork/ftw.favorite',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'ftw.favorite.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*- 
      """,
      )
