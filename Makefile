#
# Makefile for the flake8-ownership project.
#
# Copyright Joe Joyce, 2016-2017. All rights reserved.
#

PROJECT = flake8-ownership

# Virtualenv command
VIRTUALENV ?= virtualenv

# "Main" python version for development.
PYTHON_VERSION = python3.6

# Base directories
ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
ENV = $(ROOT)/.env

# Code
ENV_SOURCES = $(ROOT)/setup.py $(ROOT)/requirements.txt
README = $(ROOT)/README.rst
SOURCES = $(ROOT)/src/flake8_ownership.py
UPDATED_ENV = $(ENV)/updated

# Commands
COVERAGE = $(ENV)/bin/coverage
FLAKE8 = $(ENV)/bin/flake8
PIP = $(ENV)/bin/pip
PYTHON = $(ENV)/bin/python
SPHINX = $(ENV)/bin/sphinx-build
TOX = $(ENV)/bin/tox
TWINE = $(ENV)/bin/twine

# Distribution
VERSION = $(shell python $(ROOT)/setup.py --version)
DIST = $(ROOT)/dist/$(PROJECT)-$(VERSION).tar.gz

# Python package settings
FORCE_UPDATES_TO_PYTHON_PACKAGES = pip setuptools wheel
IGNORE_UPDATES_TO_PYTHON_PACKAGES = "\($(PROJECT)\)\|\(virtualenv\)"

# Git hooks
PRE_COMMIT = $(ROOT)/.git/hooks/pre-commit
PRE_COMMIT_HOOK = make lint
PRE_PUSH = $(ROOT)/.git/hooks/pre-push
PRE_PUSH_HOOK = make test


help :
	@printf "usage: make <target> where target is one of:\n\n"
	@printf "  check-update  Check for updates to packages\n"
	@printf "  clean         Delete generated files (dists, .pyc, etc)\n"
	@printf "  docs          Generate PDF and HTML documentation\n"
	@printf "  dist          Create sdist in dist/\n"
	@printf "  env           Install development environment\n"
	@printf "  html          Generate HTML documentation\n"
	@printf "  lint          Run linter on code\n"
	@printf "  pdf           Generate PDF documentation\n"
	@printf "  pristine      Delete development environment\n"
	@printf "  release       Cut a release of the software\n"
	@printf "  test          Run tests\n\n"


# =============================================================================
# ----- Environment -----------------------------------------------------------
# =============================================================================

$(PYTHON) :
	$(VIRTUALENV) --python=$(PYTHON_VERSION) $(ENV)

$(PIP) : $(PYTHON)

$(UPDATED_ENV) : $(PIP) $(ENV_SOURCES)
	$(PIP) install -U $(FORCE_UPDATES_TO_PYTHON_PACKAGES)
	$(PIP) install \
		--editable $(ROOT) \
		--requirement $(ROOT)/requirements.txt
	touch $(UPDATED_ENV)

env : $(PRE_COMMIT) $(PRE_PUSH) $(UPDATED_ENV)

check-update : env
	@printf "Checking for library updates...\n"
	@$(PIP) list --outdated --local --format=columns | \
		grep -v $(IGNORE_UPDATES_TO_PYTHON_PACKAGES) ||\
		printf "All libraries are up to date :)\n"

pristine : clean
	cd $(ROOT); git clean -dfX


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
	$(FLAKE8) --ignore=D203 \
		$(ROOT)/doc/conf.py \
		$(ROOT)/setup.py \
		$(ROOT)/src
	@printf "Flake8 is happy :)\n"

test-cover :
	cd $(ROOT); \
		$(COVERAGE) run setup.py test; \
		$(COVERAGE) report; \
		$(COVERAGE) html

test-tox :
	cd $(ROOT); $(TOX)

test : lint test-tox test-cover


# =============================================================================
# ----- Documentation ---------------------------------------------------------
# =============================================================================

html : env
	cd $(ROOT)/doc; make html SPHINXBUILD=$(SPHINX)

pdf : env
	cd $(ROOT)/doc; make latexpdf SPHINXBUILD=$(SPHINX)

docs: html pdf


# =============================================================================
# ----- Build -----------------------------------------------------------------
# =============================================================================

$(DIST) : $(README) $(SOURCES) $(UPDATED_ENV)
	cp $(README) README
	-cd $(ROOT) && $(PYTHON) setup.py sdist && touch $(DIST)
	rm README

dist : $(DIST)

release : clean dist
	$(ROOT)/bin/pre-release
	$(TWINE) upload $(DIST)
	$(ROOT)/bin/post-release $(VERSION)

clean :
	cd $(ROOT) && rm -rf \
		$(shell find $(ROOT) -type f -name .DS_Store) \
		$(shell find $(ROOT)/src -type f -name *.pyc) \
		.coverage \
		coverage \
		dist
