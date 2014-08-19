#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://drf-json-patch.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='drf-json-patch',
    version='0.1.0',
    description='JSON Patch support for Django REST Framework.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Kevin Brown',
    author_email='kevin@kevinbrown.in',
    url='https://github.com/kevin-brown/rest_framework_json_patch',
    packages=[
        'rest_framework_json_patch',
    ],
    package_dir={'rest_framework_json_patch':
                 'rest_framework_json_patch'},
    include_package_data=True,
    install_requires=["jsonpatch"],
    license="MIT",
    zip_safe=False,
    keywords='rest_framework_json_patch',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
