#!/usr/bin/env python

import os
import sys

import rfc3986

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py bdist_wheel sdist upload')
    sys.exit()

packages = [
    'rfc3986',
]

with open('README.rst') as f:
    readme = f.read()

with open('HISTORY.rst') as f:
    history = f.read()

setup(
    name='rfc3986',
    version=rfc3986.__version__,
    description='Validating URI References per RFC 3986',
    long_description=readme + '\n\n' + history,
    author='Ian Cordasco',
    author_email='ian.cordasco@rackspace.com',
    url='https://rfc3986.rtfd.org',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'requests': 'requests'},
    include_package_data=True,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ),
)
