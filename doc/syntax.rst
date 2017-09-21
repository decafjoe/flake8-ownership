
.. _syntax:

=========================================
 An Apology for the Configuration Syntax
=========================================

That silly ``<COMMA>`` and ``<YEAR>`` stuff is ugly, I know. The
design requirements were:

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
