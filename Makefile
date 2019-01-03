#
# Makefile for the flake8-ownership project.
#
# Copyright Joe Joyce and contributors, 2016-2018.
# See LICENSE for licensing information.
#

PROJECT = flake8-ownership

# Virtualenv command
VIRTUALENV ?= virtualenv

# "Main" python version for development
ifeq ($(TRAVIS),)
	PYTHON_DEFAULT_TOX_ENV = py36
	PYTHON_VERSION = python3.6
	PYTHON_VIRTUALENV_ARGUMENT = --python=$(PYTHON_VERSION)
else
	PYTHON_VERSION = default
	PYTHON_VIRTUALENV_ARGUMENT =
endif

# Base directories
ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
ENV = $(ROOT)/.env
DOC = $(ROOT)/doc
SRC = $(ROOT)/src
TOOL = $(ROOT)/tool

# Code
SETUP = $(ROOT)/setup.py
REQUIREMENTS = $(ROOT)/req
ENV_REQUIREMENTS = $(REQUIREMENTS)/env.txt
LINT_REQUIREMENTS = $(REQUIREMENTS)/lint.txt
TEST_REQUIREMENTS = $(REQUIREMENTS)/test.txt
ENV_SOURCES = $(SETUP) $(ENV_REQUIREMENTS) $(LINT_REQUIREMENTS) \
	$(TEST_REQUIREMENTS)
README = $(ROOT)/README.rst
SOURCES := $(shell find $(SRC) -name "*.py")
LINT_FILES = $(DOC)/conf.py $(SETUP) $(SOURCES)
UPDATED_ENV = $(ENV)/updated

# Commands
FLAKE8 = $(ENV)/bin/flake8
PIP = $(ENV)/bin/pip
PYTHON = $(ENV)/bin/python
SPHINX = $(ENV)/bin/sphinx-build
TOX = $(ENV)/bin/tox
TWINE = $(ENV)/bin/twine

# Distribution
VERSION = $(shell grep "version = '" $(SETUP) | awk -F\' '{print $$2}')
DIST = $(ROOT)/dist/$(PROJECT)-$(VERSION).tar.gz

# Python package settings
FORCE_UPDATES_TO_PYTHON_PACKAGES = pip setuptools wheel
IGNORE_UPDATES_TO_PYTHON_PACKAGES = "\($(PROJECT)\)\|\(virtualenv\)"

# Git hooks
PRE_COMMIT = $(ROOT)/.git/hooks/pre-commit
PRE_COMMIT_HOOK = $(TOOL)/pre-commit
PRE_PUSH = $(ROOT)/.git/hooks/pre-push
PRE_PUSH_HOOK = $(TOOL)/pre-push


help :
	@printf "usage: make <target> where target is one of:\n"
	@printf "\n"
	@printf "  check-update  Check for updates to dependencies\n"
	@printf "  clean         Delete build artifacts (dists, .pyc, etc)\n"
	@printf "  docs          Generate PDF and HTML documentation\n"
	@printf "  dist          Create sdist in dist/\n"
	@printf "  env           Install development environment\n"
	@printf "  html          Generate HTML documentation\n"
	@printf "  lint          Run linter on code\n"
	@printf "  pdf           Generate PDF documentation\n"
	@printf "  pristine      Delete development environment\n"
	@printf "  release       Cut a release of the software\n"
	@printf "  test          Run tests against $(PYTHON_VERSION)\n"
	@printf "  test-all      Run tests in all supported versions\n"
	@printf "\n"


# =============================================================================
# ----- Environment -----------------------------------------------------------
# =============================================================================

$(PYTHON) :
	$(VIRTUALENV) $(PYTHON_VIRTUALENV_ARGUMENT) $(ENV)

$(PIP) : $(PYTHON)

$(UPDATED_ENV) : $(PIP) $(ENV_SOURCES)
	$(PIP) install -U $(FORCE_UPDATES_TO_PYTHON_PACKAGES)
	$(PIP) install \
		--editable $(ROOT) \
		--requirement $(ENV_REQUIREMENTS)
	touch $(UPDATED_ENV)

env : $(PRE_COMMIT) $(PRE_PUSH) $(UPDATED_ENV)

check-update : env
	@printf "Checking for library updates...\n"
	@$(PIP) list --outdated --local --format=columns | \
		grep -v $(IGNORE_UPDATES_TO_PYTHON_PACKAGES) ||\
		printf "All libraries are up to date :)\n"

pristine : clean
	git -C $(ROOT) clean -dfX
	rm -f $(PRE_COMMIT) $(PRE_PUSH)


# =============================================================================
# ----- QA/Test ---------------------------------------------------------------
# =============================================================================

$(PRE_COMMIT) : $(ROOT)/Makefile
	echo "$(PRE_COMMIT_HOOK)" > $(PRE_COMMIT)
	chmod +x $(PRE_COMMIT)

$(PRE_PUSH) : $(ROOT)/Makefile
	echo "$(PRE_PUSH_HOOK)" > $(PRE_PUSH)
	chmod +x $(PRE_PUSH)

lint : env
	@$(FLAKE8) --ignore=D203 $(LINT_FILES)
	@printf "Flake8 is happy :)\n"

test : env
	cd $(ROOT); $(TOX) -e$(PYTHON_DEFAULT_TOX_ENV),cover

test-all : env
	cd $(ROOT); $(TOX)


# =============================================================================
# ----- Documentation ---------------------------------------------------------
# =============================================================================

html : env
	make -C $(DOC) html SPHINXBUILD=$(SPHINX)

pdf : env
	make -C $(DOC) latexpdf SPHINXBUILD=$(SPHINX)

docs: html pdf


# =============================================================================
# ----- Build -----------------------------------------------------------------
# =============================================================================

$(DIST) : $(README) $(SOURCES) $(UPDATED_ENV)
	cp $(README) $(ROOT)/README
	-cd $(ROOT) && $(PYTHON) setup.py sdist && touch $(DIST)
	rm $(ROOT)/README

dist : $(DIST)

release :
	$(TOOL)/pre-release
	make -C $(ROOT) clean dist
	$(TWINE) upload $(DIST)
	$(TOOL)/post-release $(VERSION)

clean :
	cd $(ROOT) && rm -rf \
		$(shell find $(ROOT) -type f -name .DS_Store) \
		$(shell find $(SRC) -type f -name *.pyc) \
		.tox/coverage* \
		coverage \
		dist
