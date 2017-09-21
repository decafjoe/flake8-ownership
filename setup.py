# -*- coding: utf-8 -*-
"""
Package configuration for flake8-ownership.

:author: Joe Joyce <joe@decafjoe.com>
:copyright: Copyright (c) Joe Joyce and contributors, 2016-2017.
:license: BSD
"""
from setuptools import setup


name = 'flake8-ownership'
version = '1.1.0'
requires = (
    'flake8>=3,<4',
)

description = 'A flake8 checker for assuring that author, copyright, and ' \
              'license are specified in source files.'
long_description = 'Please see the official project page at ' \
                   'http://flake8_ownership.readthedocs.io.'

setup(
    author='Joe Joyce',
    author_email='joe@decafjoe.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    description=description,
    entry_points={
        'flake8.extension': [
            'O10 = %s:Checker' % name.replace('-', '_'),
        ],
    },
    install_requires=requires,
    license='BSD',
    long_description=long_description,
    name=name,
    package_dir={'': 'src'},
    py_modules=[name.replace('-', '_')],
    test_suite='test',
    url='http://%s.readthedocs.io' % name,
    version=version,
    zip_safe=False,
)
