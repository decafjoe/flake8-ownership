
==================
 flake8-ownership
==================

flake8-ownership was inspired by `flake8-copyright`_ and a personal
desire to learn how to write flake8 extensions. It's meant to be a
little more powerful than `flake8-copyright`_ while not quite as
flexible as `flake8-regex`_.

flake8-ownership can make sure your codebase has proper
``:author:``, ``:copyright:``, and ``:license:`` tags in each file.
The required content of those tags is set in the `flake8
configuration`_.

For example, the configuration for this project is::

  [flake8]
  author-re = ^Joe Joyce <joe@decafjoe.com>$
  copyright-re = ^Copyright \(c\) Joe Joyce<COMMA> 2016-<YEAR>.$
  license-re = ^BSD$

This configuration ensures that each file in the project has the
following lines::

  :author: Joe Joyce <joe@decafjoe.com>
  :copyright: Copyright (c) Joe Joyce, 2016-2017.
  :license: BSD

If any of those lines are missing, it's a violation. If they don't
match the regex, it's a violation. `My apologies`_ for
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


Contributing
============

There shouldn't be much to contribute. This is a pretty small, simple
project. If you run into bugs, please file them in the project's `issue
tracker on Bitbucket`_. Code and documentation patches are welcome, but
please file a feature request before spending much time, so we can make
sure the change is in line with the goals of the project.

For development you'll need:

* Python 2.6, 2.7, 3.3, 3.4, 3.5, and 3.6
* PyPy 2 and 3
* Standard build tools like gcc, make, etc

To get started, clone this repo, ``cd`` into its directory, and run
``make test``. This will install the development tools and virtual
environments, as well as run the linter and full test suite under all
supported versions. If the tests pass, you're all set up.

.. _issue tracker on Bitbucket: https://bitbucket.org/decafjoe/flake8-ownership/issues

.. _My apologies:

An Apology for the Configuration Syntax
=======================================

It sucks, I know. The design requirements were:

#. Must support flexible specification of acceptable
   author/copyright/license lines. Since this is a programmer product,
   regexes are a good choice here.
#. Projects may include code from other projects. That code will have
   author/copyright/license lines that are different than the main
   project's. So there must be a way to specify multiple acceptable
   values for each.

The last one tripped things up. Flake8 supports providing a list of
values using a comma separated list::

  [flake8]
  some-setting =
    first thing,
    second thing,
    third thing

Great, but copyright lines often have commas in them::

  [flake8]
  copyright-re =
    Copyright 2016-2017, Joe Joyce,
    Copyright 2015 by Other Project and its contributers.

Whoops! The configuration parser reads this as three different
regexes. Maybe we can escape the comma?

::

   [flake8]
   copyright-re =
    Copyright 2016-2017\, Joe Joyce,
    Copyright 2015 by Other project and its contributors.

No dice.

Ok, so we'll have to have a placeholder and do some interpolation.
Python format strings?

::

   [flake8]
   copyright-re =
    Copyright 2016-2017%(comma)s Joe Joyce,
    Copyright 2015 by Other Project and its contributers.

Bzzzt. The config parser tries to interpolate this value from the
config file itself. And we don't control the config parsing behavior
so we can't tell it not to do that.

And that's why I ended up with the crappy,
where-the-heck-did-that-come-from syntax that flake8-ownership
uses::

   [flake8]
   copyright-re =
    Copyright 2016-2017<COMMA> Joe Joyce,
    Copyright 2015 by Other Project and its contributers.

The config parser doesn't do anything clever with this, and
flake8-ownership can replace ``<COMMA>`` with ``,`` when it processes
the config values.
