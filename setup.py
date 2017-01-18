from setuptools import setup, find_packages
import os

version = '1.0.dev0'

desc = 'Transmogrifier source for reading JSON files from the filesystem'
long_desc = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)
tests_require = [
    'plone.app.testing',
    'plone.testing',
    'unittest2',
    'zope.component',
    'zope.intid',
]


setup(name='transmogrify.jsonsource',
      version=version,
      description=desc,
      long_description=long_desc,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone transmogrifier json filesystem',
      author='Cleber J Santos',
      author_email='cleber@cleberjsantos.com.br',
      url='http://pypi.python.org/pypi/transmogrify.jsonsource',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['transmogrify'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.transmogrifier',
          'plone.app.transmogrifier',
          'Products.CMFCore',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = transmogrify
      """,
      )

