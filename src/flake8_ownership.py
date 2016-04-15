# -*- coding: utf-8 -*-
"""
Flake8 extension for checking author, copyright, and license.

:author: Joe Strickler <joe@decafjoe.com>
:copyright: Joe Strickler, 2016. All rights reserved.
:license: Proprietary
"""
import datetime
import re

#: Version of the extension.
#:
#: :type: :class:`str`
__version__ = '0.1.1'


#: Current year, used for calculating what the copyright line should be.
#:
#: :type: :class:`int`
year = datetime.date.today().year

#: Regex that matches the ``:author:`` line.
#:
#: :type: :func:`re <re.compile>`
author_re = re.compile(r'^:author: (?P<author>.+)$')

#: Sequence of regexes matching expected ``:author:`` values.
#:
#: :type: :class:`list`
expected_authors = (
    re.compile(r'^Joe Strickler <joe@decafjoe.com>$'),
)

#: Regex that matches the ``:copyright:`` line.
#:
#: :type: :func:`re <re.compile>`
copyright_re = re.compile(r'^:copyright: (?P<copyright>.+)$')

#: Sequence of regexes matching expected ``:copyright:`` values.
#:
#: :type: :class:`list`
expected_copyrights = (
    re.compile(r'^Joe Strickler, (20\d{2}-)?%s. All rights reserved.$' % year),
)

#: Regex that matches the ``:license:`` line.
#:
#: :type: :func:`re <re.compile>`
license_re = re.compile(r'^:license: (?P<license>.+)$')

#: Sequence of regexes matching expected ``:license:`` values.
#:
#: :type: :class:`list`
expected_licenses = (
    re.compile(r'^Proprietary$'),
)


class Checker(object):
    """Flake8 checker class that checks for author, copyright, and license."""

    #: Prefix for the error codes emitted from this class.
    #:
    #: :type: :class:`str`
    codes = 'O10'

    #: Name of the checker.
    #:
    #: :type: :class:`str`
    name = 'flake8_ownership'

    #: Version of the checker.
    #:
    #: :type: :class:`str`
    version = __version__

    def __init__(self, tree, filename):  # noqa
        self.filename = filename
        self.tree = tree

    def run(self):
        """Run the :class:`Checker` on a :attr:`filename`."""
        tags = [
            dict(
                name='author',
                error='0',
                re=author_re,
                expected=expected_authors,
            ),
            dict(
                name='copyright',
                error='1',
                re=copyright_re,
                expected=expected_copyrights,
            ),
            dict(
                name='license',
                error='2',
                re=license_re,
                expected=expected_licenses,
            ),
        ]
        with open(self.filename) as f:
            i = 0
            for line in f:
                i += 1
                line = line[:-1]
                found_tag = None
                for tag in tags:  # pragma: no branch
                    match = tag['re'].search(line)
                    if match:
                        found_tag = tag
                        value = match.groupdict()[tag['name']]
                        for regex in tag['expected']:
                            if regex.search(value):
                                break
                        else:
                            msg = '%s%s unrecognized %s' % (
                                self.codes,
                                tag['error'],
                                tag['name'],
                            )
                            yield i, 0, msg, type(self)
                        break
                if found_tag:  # pragma: no branch
                    tags.remove(found_tag)
                    if len(tags) == 0:
                        break
        for tag in tags:
            msg = '%s%s missing %s' % (self.codes, tag['error'], tag['name'])
            yield 0, 0, msg, type(self)
