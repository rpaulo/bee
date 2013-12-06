#!/usr/bin/env python

from distutils.core import setup

setup(name='bee',
      version='0.1',
      description='bhyve configuration tool',
      author='Rui Paulo',
      author_email='rpaulo@felyko.com',
      url='https://bitbucket.org/rpaulo/bee',
      packages=['bee'],
      package_dir={'' : 'src/lib'},
      scripts=['src/bee'])
