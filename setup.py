# -*- coding: utf-8 -*-
"""
Package configuration for flake8-ownership.

:author: Joe Joyce <joe@decafjoe.com>
:copyright: Copyright (c) Joe Joyce, 2016-2017. All rights reserved.
:license: BSD
"""
from setuptools import setup


name = 'flake8-ownership'
version = '0.9.1'
requires = ()


setup(
    author='Joe Joyce',
    author_email='joe@decafjoe.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    description='Checks for author, copyright, and license attributes.',
    entry_points={
        'flake8.extension': [
            '%(name)s = %(name)s:Checker' % dict(name=name.replace('-', '_')),
        ],
    },
    install_requires=requires,
    license='Proprietary',
    long_description=open('README.rst').read(),
    name=name,
    package_dir={'': 'src'},
    py_modules=[name.replace('-', '_')],
    test_suite='test',
    url='https://bitbucket.org/decafjoe/%s' % name,
    version=version,
    zip_safe=False,
)
