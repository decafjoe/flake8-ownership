# -*- coding: utf-8 -*-
"""
Package configuration for flake8-ownership.

:author: Joe Joyce <joe@decafjoe.com>
:copyright: Copyright (c) Joe Joyce, 2016-2017.
:license: BSD
"""
import os

from setuptools import setup


name = 'flake8-ownership'
version = '0.9.4'
requires = ()

root = os.path.abspath(os.path.dirname(__file__))
changelog = open(os.path.join(root, 'CHANGELOG.rst')).read()
readme = open(os.path.join(root, 'README.rst')).read()
long_description = '%s\n\n%s' % (readme, changelog)


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
    description='Checks for author, copyright, and license info.',
    entry_points={
        'flake8.extension': [
            '%(name)s = %(name)s:Checker' % dict(name=name.replace('-', '_')),
        ],
    },
    install_requires=requires,
    license='BSD',
    long_description=long_description,
    name=name,
    package_dir={'': 'src'},
    py_modules=[name.replace('-', '_')],
    test_suite='test',
    url='https://bitbucket.org/decafjoe/%s' % name,
    version=version,
    zip_safe=False,
)
