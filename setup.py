import os
from setuptools import setup, find_packages


version = '1.0.dev0'


extras_require = {
    'simplelayout': [
        'simplelayout.base',
        'ftw.contentpage']}


tests_require = [
    'unittest2',
    'pyquery',
    'ftw.testing',
    'zope.configuration',
    'plone.app.testing',
    ] + reduce(list.__add__, extras_require.values())

extras_require['tests'] = tests_require


setup(name='ftw.topics',
      version=version,
      description='Create subject trees in Plone',

      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw topics',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.topics',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'plone.app.dexterity',
        'collective.dexteritytextindexer',
        'plone.app.referenceablebehavior',
        'plone.directives.form',
        'plone.browserlayer',
        'ftw.contentpage',
        ],

      tests_require=tests_require,
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
