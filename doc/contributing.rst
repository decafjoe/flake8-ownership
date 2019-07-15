
==============
 Contributing
==============

There shouldn't be much to contribute. This is a pretty small, simple
project that doesn't aim to be any more ambitious than it already is.
If you run into bugs, please file them in the project's issue tracker
on GitHub. Code and documentation patches are welcome, but please
file a feature request before spending much time, so we can make sure
the change is in line with the goals of the project.

That said, here's the info about the development environment.


Prerequisites
=============

Requirements:

* Common development tools like git, make, a C compiler, etc
* Python 3.6 -- this is the "main" interpreter used for development
* Virtualenv

Recommendations:

* All supported Python interpreters

  * Python 2.7
  * Python 3.4
  * Python 3.5
  * Python 3.6
  * PyPy
  * PyPy 3

Suggestions:

* LaTeX -- for building the documentation as a PDF


Setup
=====

The repository can be cloned anywhere you like on your local machine.
At any time, you can delete the entire project and its environment by
``rm -rf`` -ing the local directory.

.. highlight:: bash

The following instructions clone the repository to
``~/flake8-ownership``::

   cd
   git clone https://github.com/decafjoe/flake8-ownership.git
   cd flake8-ownership
   make env

Wait ~10m and you should be good to go!

Note that all dependencies are installed underneath the repository
directory (take a peek at ``.env/``). To delete the development
environment artifacts, you can run ``make pristine`` (see below). To
delete everything, simply ``rm -rf`` the clone.


Tooling
=======

flake8-ownership's developer tooling is exposed via ``make``. Run
``make`` with no arguments to get a list of available targets. All
targets except ``make release`` are idempotent, so they can be run at
any time.

Environment:

* ``make env`` installs the development environment; subsequent runs
  update the environment if required
* ``make clean`` deletes build artifacts like .pyc files, sdists, etc
* ``make pristine`` kills the local development environment
* ``make check-update`` checks for updates to Python packages
  installed in the development environment

Documentation:

* ``make html`` generates the HTML documentation to
  ``doc/_build/html/``
* ``make pdf`` generates the PDF documentation to
  ``doc/_build/latex/clik.pdf``
* ``make docs`` builds both HTML and PDF documentation to their
  respective locations

Build:

* ``make dist`` builds a sdist into ``dist/``
* ``make release`` builds a clean sdist, uploads it to PyPI, tags the
  commit with the current version number, bumps the version, then
  commits the new version number and pushes it up to GitHub (this is
  largely implemented by the ``tool/pre-release`` and
  ``tool/post-release`` scripts)

QA:

* ``make lint`` runs the Flake8 linter on the Python files in the
  project
* ``make test`` runs the test suite against the "main" development
  interpreter
* ``make test-all`` runs the linter, runs the test suite against all
  supported interpreters, and generates a coverage report to
  ``coverage/``
