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
version = '1.0.1'
requires = (
    'flake8>=3,<4',
)

root = os.path.abspath(os.path.dirname(__file__))


def read(filename, default):
    """
    Read and return content of FILENAME (or FILENAME.rst) from root directory.

    If neither of the files exist, ``default`` is returned.
    """
    path = os.path.join(root, filename)
    if os.path.exists(path):
        return open(path).read()
    path = '%s.rst' % path
    if os.path.exists(path):
        return open(path).read()
    return default


changelog = read('CHANGELOG', 'No changelog present.')
readme = read('README', 'No readme present.')
long_description = '%s\n\n%s' % (readme, changelog)

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
    description='Checks for author, copyright, and license info.',
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
    url='https://bitbucket.org/decafjoe/%s' % name,
    version=version,
    zip_safe=False,
)
