# -*- coding: utf-8 -*-
"""
Tests for flake8-ownership.

:author: Joe Joyce <joe@decafjoe.com>
:copyright: Copyright (c) Joe Joyce, 2016-2017.
:license: BSD
"""
import datetime
import os
import re
import tempfile
import unittest

import mock

from flake8_ownership import Checker


#: "Standard" test value for the author.
#:
#: :type: :class:`str`
test_author = 'Joe Joyce <joe@decafjoe.com>'

#: Regex that matches the "standard" author value.
#:
#: :type: :mod:`re`
test_author_re = re.compile('^Joe Joyce <joe@decafjoe.com>$')

#: "Standard" test value for the copyright.
#:
#: :type: :class:`str`
test_copyright = 'Copyright (c) Joe Joyce, 2016'

#: Regex that matches the "standard" copyright value.
#:
#: :type: :mod:`re`
test_copyright_re = re.compile('^Copyright \(c\) Joe Joyce, 2016$')

#: "Standard" test value for the license.
#:
#: :type: :class:`str`
test_license = 'BSD'

#: Regex that matches the "standard" license value.
#:
#: :type: :mod:`re`
test_license_re = re.compile('^BSD$')


class OptionTest(unittest.TestCase):
    """Test the option handling for the checker."""

    def setUp(self):
        """Reset checker."""
        Checker.author_re = None
        Checker.copyright_re = None
        Checker.license_re = None

    def test_add_options(self):
        """Test :meth:`flake8_ownership.Checker.add_options`."""
        expected_calls = []
        for tag in ('author', 'copyright', 'license'):
            expected_calls.append(mock.call(
                '--%s-re' % tag,
                comma_separated_list=True,
                help='regular expression(s) for valid :%s: lines' % tag,
                parse_from_config=True,
            ))
        parser = mock.Mock()
        Checker.add_options(parser)
        parser.add_option.assert_has_calls(expected_calls, any_order=True)

    def test_parse_option(self):
        """Test :meth:`flake8_ownership.Checker._parse_option`."""
        options = mock.Mock()
        options.test = ['item 1', 'item 2<COMMA> <YEAR>']
        regexes = Checker._parse_option(options, 'test')
        self.assertEqual(2, len(regexes))
        r1, r2 = regexes

        r1string, r1regex = r1
        self.assertEqual('item 1', r1string)
        self.assertTrue(type(r1regex) is type(re.compile('')))  # noqa: E721

        r2string, r2regex = r2
        r2string_expected = 'item 2, %s' % datetime.datetime.today().year
        self.assertEqual(r2string_expected, r2string)
        self.assertTrue(type(r2regex) is type(re.compile('')))  # noqa: E721

    def test_parse_options(self):
        """Test :meth:`flake8_ownership.Checker.parse_options`."""
        options = mock.Mock()
        options.author_re = []
        options.copyright_re = ['item 1']
        options.license_re = ['item 2', 'item 3']
        Checker.parse_options(options)
        self.assertEqual(0, len(Checker.author_re))
        self.assertEqual(1, len(Checker.copyright_re))
        self.assertEqual(2, len(Checker.license_re))


class CheckerTest(unittest.TestCase):
    """Test the actual checks."""

    def setUp(self):
        """Reset checker, create temporary file for checker tests."""
        Checker.author_re = None
        Checker.copyright_re = None
        Checker.license_re = None
        self._tmp_fd, self._tmp_path = tempfile.mkstemp()
        self._tmp = os.fdopen(self._tmp_fd, 'w')

    def tearDown(self):
        """Close and delete temporary file created in :meth:`setUp`."""
        os.unlink(self._tmp_path)

    def write(self, author=None, copyright=None, license=None, extra=None):
        """
        Write author, copyright, and license to the temporary file.

        :param author: Value for the author line. :data:`None` if no author
                       line is to be written.
        :type author: :class:`str` or :data:`None`
        :param copyright: Value for the copyright line. :data:`None` if no
                          copyright line is to be written.
        :type copyright: :class:`str` or :data:`None`
        :param license: Value for the license line. :data:`None` if no license
                        line is to be written.
        :type license: :class:`str` or :data:`None`
        :param extra: Extra data to write to end of the file.
        :type extra: :class:`str` or :data:`None`
        """
        self._tmp.write('\n')
        if author is not None:
            self._tmp.write(':author: %s\n' % author)
        if copyright is not None:
            self._tmp.write(':copyright: %s\n' % copyright)
        if license is not None:
            self._tmp.write(':license: %s\n' % license)
        if extra is not None:
            self._tmp.write('%s\n' % extra)

    def check(self):
        """
        Run checker on the temporary file (call after :meth:`write`).

        :return: List of errors from the checker. Each error is of the format
                 ``(line<int>, column<int>, message<str>, klass<type>)``.
        :rtype: :class:`list`
        """
        self._tmp.flush()
        return list(Checker(None, self._tmp_path).run())

    def configure(self, author=False, copyright=False, license=False):
        """
        Configure the checker.

        :param bool author: Whether to enable author checking.
        :param bool copyright: Whether to enable copyright checking.
        :param bool license: Whether to enable license checking.
        """
        if author:
            Checker.author_re = [test_author_re]
        if copyright:
            Checker.copyright_re = [test_copyright_re]
        if license:
            Checker.license_re = [test_license_re]

    def assert_error(self, line, column, message):
        """
        Assert that that the file has a single error.

        :param line: Line number where the error should have.
        :type line: int
        :param column: Column number where the error should have occurred.
        :type column: int
        :param message: Error message.
        :type message: str
        """
        errors = self.check()

        fmt = 'expected exactly one error, got %i'
        self.assertEqual(1, len(errors), fmt % len(errors))

        actual_line, actual_column, actual_message, _ = errors[0]

        fmt = 'expected line number to be %i, got %i'
        self.assertEqual(line, actual_line, fmt % (line, actual_line))

        fmt = 'expected column number to be %i, got %i'
        self.assertEqual(column, actual_column, fmt % (column, actual_column))

        fmt = 'expected message to be "%s", got "%s"'
        msg = fmt % (message, actual_message)
        self.assertEqual(message, actual_message, msg)

    def test_default(self):
        """Check that no config and empty file passes the checks."""
        self.write()
        errors = self.check()
        fmt = 'expected no errors, got %i'
        self.assertEqual(0, len(errors), fmt % len(errors))

    def test_valid(self):
        """Full author/copyright/license with a file that should be valid."""
        self.configure(author=True, copyright=True, license=True)
        self.write(
            author=test_author,
            copyright=test_copyright,
            license=test_license,
        )
        errors = self.check()
        messages = '"%s"' % '", "'.join([m for _, _, m, _ in errors])
        msg = 'expected no errors, got %i (%s)' % (len(errors), messages)
        self.assertEqual(0, len(errors), msg)

    def test_author_missing(self):
        """Check error when author is missing."""
        self.configure(author=True)
        self.write()
        self.assert_error(0, 0, 'O100 missing author')

    def test_author_invalid(self):
        """Check error when author is invalid."""
        self.configure(author=True)
        self.write(author='Bob Wrongman <bob@example.com>')
        self.assert_error(2, 0, 'O100 unrecognized author')

    def test_copyright_missing(self):
        """Check error when copyright is missing."""
        self.configure(copyright=True)
        self.write()
        self.assert_error(0, 0, 'O101 missing copyright')

    def test_copyright_invalid(self):
        """Check error when copyright is invalid."""
        self.configure(copyright=True)
        self.write(copyright='Copyright (c) EvilCorp 2015')
        self.assert_error(2, 0, 'O101 unrecognized copyright')

    def test_license_missing(self):
        """Check error when license is missing."""
        self.configure(license=True)
        self.write()
        self.assert_error(0, 0, 'O102 missing license')

    def test_license_invalid(self):
        """Check error when license is invalid."""
        self.configure(license=True)
        self.write(license=':license: NotARealLicense')
        self.assert_error(2, 0, 'O102 unrecognized license')

    def test_stops_checking_when_satisfied(self):
        """Check that the checker returns immediately once it is satisfied."""
        self.configure(author=True)
        self.write(author=test_author, extra=':author: Not the desired author')
        errors = self.check()
        fmt = 'expected no errors, got %i'
        self.assertEqual(0, len(errors), fmt % len(errors))
