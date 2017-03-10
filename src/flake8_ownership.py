# -*- coding: utf-8 -*-
"""
Flake8 extension for checking author, copyright, and license.

:author: Joe Joyce <joe@decafjoe.com>
:copyright: Copyright (c) Joe Joyce, 2016-2017. All rights reserved.
:license: BSD
"""
import datetime
import re

#: Version of the extension.
#:
#: :type: :class:`str`
__version__ = '0.9.3'

#: Regex that matches the ``:author:`` line.
#:
#: :type: :func:`re <re.compile>`
author_re = re.compile(r'^:author: (?P<author>.+)$')

#: Regex that matches the ``:copyright:`` line.
#:
#: :type: :func:`re <re.compile>`
copyright_re = re.compile(r'^:copyright: (?P<copyright>.+)$')

#: Regex that matches the ``:license:`` line.
#:
#: :type: :func:`re <re.compile>`
license_re = re.compile(r'^:license: (?P<license>.+)$')


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

    #: List of regexes of valid :author: values.
    #:
    #: :type: :class:`list` of :mod:`re` instances.
    author_re = None

    #: List of regexes of valid :copyright: values.
    #:
    #: :type: :class:`list` of :mod:`re` instances.
    copyright_re = None

    #: List of regexes of valid :license: values.
    #:
    #: :type: :class:`list` of :mod:`re` instances.
    license_re = None

    @classmethod
    def add_options(cls, parser):
        """Add --author-re, --copyright-re, and --license-re options."""
        parser.add_option(
            '--author-re',
            comma_separated_list=True,
            help='regular expression(s) for valid :author: lines',
            parse_from_config=True,
        )
        parser.add_option(
            '--copyright-re',
            comma_separated_list=True,
            help='regular expression(s) for valid :copyright: lines',
            parse_from_config=True,
        )
        parser.add_option(
            '--license-re',
            comma_separated_list=True,
            help='regular expression(s) for valid :license: lines',
            parse_from_config=True,
        )

    @classmethod
    def _parse_option(cls, options, option):
        rv = []
        year = str(datetime.datetime.today().year)
        for regex in getattr(options, option, ()):
            regex = regex.replace('<COMMA>', ',').replace('<YEAR>', year)
            rv.append((regex, re.compile(regex)))
        return rv

    @classmethod
    def parse_options(cls, options):
        """
        Process the supplied configuration.

        This populates the :attr:`author_re`, :attr:`copyright_re`, and
        :attr:`license_re` attributes. For each configuration option, this
        substitutes ``<COMMA>`` and ``<YEAR>`` as appropriate, then compiles
        each regex.
        """
        for option in ('author_re', 'copyright_re', 'license_re'):
            regexes = cls._parse_option(options, option)
            setattr(cls, option, [regex[1] for regex in regexes])

    def __init__(self, tree, filename):
        """Initialize the checker; nothing special here."""
        self.filename = filename
        self.tree = tree

    def run(self):
        """Run the :class:`Checker` on a :attr:`filename`."""
        tags = []
        if self.author_re:
            tags.append(dict(
                name='author',
                error='0',
                re=author_re,
                expected=self.author_re,
            ))
        if self.copyright_re:
            tags.append(dict(
                name='copyright',
                error='1',
                re=copyright_re,
                expected=self.copyright_re,
            ))
        if self.license_re:
            tags.append(dict(
                name='license',
                error='2',
                re=license_re,
                expected=self.license_re,
            ))

        with open(self.filename) as f:
            i = 0
            for line in f:
                i += 1
                line = line[:-1]
                found_tag = None
                for tag in tags:
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
                if found_tag:
                    tags.remove(found_tag)
                    if len(tags) == 0:
                        break
        for tag in tags:
            msg = '%s%s missing %s' % (self.codes, tag['error'], tag['name'])
            yield 0, 0, msg, type(self)
