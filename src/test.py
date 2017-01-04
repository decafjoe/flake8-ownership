# -*- coding: utf-8 -*-
"""
Unit tests for flake8-ownership.

:author: Joe Strickler <joe@decafjoe.com>
:copyright: Joe Strickler, 2016-2017. All rights reserved.
:license: Proprietary
"""
import os
import tempfile
import unittest

from flake8_ownership import Checker


#: Valid author line.
#:
#: :type: :class:`str`
test_author = ':author: Joe Strickler <joe@decafjoe.com>'

#: Valid copyright line.
#:
#: :type: :class:`str`
test_copyright = ':copyright: Joe Strickler, 2016-2017. All rights reserved.'

#: Valid license line.
#:
#: :type: :class:`str`
test_license = ':license: Proprietary'


class Test(unittest.TestCase):
    """Test the checker."""

    def setUp(self):
        """Create temporary file for code."""
        self._tmp_fd, self._tmp_path = tempfile.mkstemp()
        self._tmp = os.fdopen(self._tmp_fd, 'w')

    def tearDown(self):
        """Close and delete temporary file created in :meth:`setUp`."""
        os.unlink(self._tmp_path)

    def write(
            self,
            author=test_author,
            copyright=test_copyright,
            license=test_license,
            extra=None,
    ):
        """
        Write author, copyright, and license to the temporary file.

        :param author: Author line to write to the file. Line is skipped if
                       argument is :data:`None`.
        :type author: :class:`str` or :data:`None`
        :param copyright: Copyright line to add to the file. Line is skipped
                          if argument is :data:`None`.
        :type copyright: :class:`str` or :data:`None`
        :param license: License line to add to the file. Line is skipped if
                        argument is :data:`None`.
        :type license: :class:`str` or :data:`None`
        """
        if author is not None:
            self._tmp.write('%s\n' % author)
        if copyright is not None:
            self._tmp.write('%s\n' % copyright)
        if license is not None:
            self._tmp.write('%s\n' % license)
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

    def test_author_missing(self):
        """Check error when author is missing."""
        self.write(author=None)
        self.assert_error(0, 0, 'O100 missing author')

    def test_author_invalid(self):
        """Check error when author is invalid."""
        self.write(author=':author: Joseph Strickler <joe@decafjoe.com>')
        self.assert_error(1, 0, 'O100 unrecognized author')

    def test_copyright_missing(self):
        """Check error when copyright is missing."""
        self.write(copyright=None)
        self.assert_error(0, 0, 'O101 missing copyright')

    def test_copyright_invalid(self):
        """Check error when copyright is invalid."""
        line = ':copyright: Joe Strickler, 2015. All rights reserved.'
        self.write(copyright=line)
        self.assert_error(2, 0, 'O101 unrecognized copyright')

    def test_license_missing(self):
        """Check error when license is missing."""
        self.write(license=None)
        self.assert_error(0, 0, 'O102 missing license')

    def test_license_invalid(self):
        """Check error when license is invalid."""
        self.write(license=':license: NotARealLicense')
        self.assert_error(3, 0, 'O102 unrecognized license')

    def test_valid(self):
        """Check properly formatted file."""
        self.write()
        errors = self.check()
        fmt = 'expected no errors, got %i'
        self.assertEqual(0, len(errors), fmt % len(errors))

    def test_stops_checking_when_satisfied(self):
        """Check that the checker returns immediately once it is satisfied."""
        self.write(extra=':author: Not the desired author')
        errors = self.check()
        fmt = 'expected no errors, got %i'
        self.assertEqual(0, len(errors), fmt % len(errors))
