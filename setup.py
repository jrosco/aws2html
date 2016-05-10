#!/usr/bin/env python

from distutils.core import setup

setup(name='aws2html',
      version='2.0',
      description='Pipe the aws-cli json output and convert to html',
      author='Joel Cumberland',
      author_email='joel_c@zoho.com',
      scripts=['aws2html.py'],
      package_data = ['templates/']
      )
