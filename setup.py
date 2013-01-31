# -*- coding: utf-8 -*-

import os

from setuptools import Command
from setuptools import setup
from setuptools import find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


# register test method to a module...
class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess
        #errno = subprocess.call([sys.executable, 'runtests.py', 'src'])
        errno = subprocess.call([sys.executable, 'test.sh'])
        raise SystemExit(errno)


setup(name='scads',
      version='0.1',
      description='Scalable Data Structures',
      long_description=read('src/scads/docs/index.rst'),
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='',
      author='Daniel Kraft',
      author_email='daniel.kraft@d9t.de',
      url='http://d9t.de/',
      license='GPLv3',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      #test_suite='website.tests',
      cmdclass={'test': PyTest},
      install_requires=[
          #'setuptools',
          'riak',
          'riak_pb',
          'protobuf',
          #'docopt',
          'passlib',
          #'mock',
          'nose',
          'nose-selecttests',
          #'coverage',
          #'unittest2',
          #'setuptools-flakes',
          #'pep8',
          #'webtest',
          #'wsgi_intercept',
          #'mechanize',
          #'zope.testbrowser',
          #'mock',
          'pytest',
          'pytest-cov',
          'pytest-pep8',
          'Sphinx',
          ],
      #entry_points="""\
      #[console_scripts]
      #riak_shell = website.scripts.riak_shell:main
      #""",
      include_package_data=True,
      zip_safe=False,
      )
