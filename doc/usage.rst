
=======
 Usage
=======

flake8-ownership was inspired by `flake8-copyright`_ and a personal
desire to learn how to write flake8 extensions. It's meant to be a
little more powerful than `flake8-copyright`_ while not quite as
flexible as `flake8-regex`_.

flake8-ownership can make sure your codebase has proper
``:author:``, ``:copyright:``, and ``:license:`` tags in each file.
The required content of those tags is set in the `flake8
configuration`_.

.. highlight:: ini

For example, the configuration for this project is::

  [flake8]
  author-re = ^Joe Joyce <joe@decafjoe.com>$
  copyright-re = ^Copyright \(c\) Joe Joyce and contributors<COMMA> 2016-<YEAR>.$
  license-re = ^BSD$


.. highlight:: rst

This configuration ensures that each file in the project has the
following lines::

  :author: Joe Joyce <joe@decafjoe.com>
  :copyright: Copyright (c) Joe Joyce and contributors, 2016-2017.
  :license: BSD

If any of those lines are missing, it's a violation. If they don't
match the regex, it's a violation. :ref:`My apologies <syntax>` for
the weird ``<COMMA>`` and ``<YEAR>`` stuff. Those special strings will be
substituted with an actual comma and the current year, respectively.
(For all three tags.)

Note that all three settings are optional; if you do not specify any
of the ``-re`` settings, flake8-ownership will not do any checks. If
you specify one or two, it will check *only* those one or two.

You may also specify multiple valid author/copyright/license regexes
by supplying a comma separated list::

  [flake8]
  author-re =
    ^Joe Joyce <joe@decafjoe.com>$,
    ^John Everyman <john@example.com>$

With that configuration, either of the following lines passes::

  :author: Joe Joyce <joe@decafjoe.com>
  :author: John Everyman <john@example.com>

.. _flake8-copyright: https://pypi.python.org/pypi/flake8-copyright
.. _flake8-regex: https://pypi.python.org/pypi/flake8-regex
.. _flake8 configuration: http://flake8.pycqa.org/en/latest/user/configuration.html
