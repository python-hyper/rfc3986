"""Packaging logic for the rfc3986 library."""
import io
import os
import sys

import setuptools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))  # noqa

import rfc3986

packages = [
    'rfc3986',
]

with io.open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setuptools.setup(
    name='rfc3986',
    version=rfc3986.__version__,
    description='Validating URI References per RFC 3986',
    long_description=readme,
    author='Ian Stapleton Cordasco',
    author_email='graffatcolmingov@gmail.com',
    url='http://rfc3986.readthedocs.io',
    packages=packages,
    package_dir={'': 'src'},
    package_data={'': ['LICENSE']},
    include_package_data=True,
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
    extras_require={
        'idna2008':  ['idna']
    }
)
