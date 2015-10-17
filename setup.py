#!/usr/bin/env python
# The MIT License (MIT)
#
# Copyright (c) 2015 Numenta, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sdict = {}

execfile('riverpy/version.py', {}, sdict)

def findRequirements():
  """
  Read the requirements.txt file and parse into requirements for setup's
  install_requirements option.
  """
  return [
    line.strip()
    for line in open("requirements.txt").readlines()
    if not line.startswith("#")
  ]

sdict.update({
    'name' : 'riverpy',
    'description' : 'Python client for River View',
    'url': 'http://github.com/nupic-community/riverpy',
    'author' : 'Matthew Taylor',
    'author_email' : 'matt@numenta.org',
    'keywords' : ['river', 'view', 'client'],
    'license' : 'MIT',
    'install_requires': findRequirements(),
    # 'test_suite': 'tests.unit',
    'packages' : ['riverpy'],
    'classifiers' : [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python'],
})

setup(**sdict)
