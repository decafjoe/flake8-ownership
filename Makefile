#
# Makefile for the flake8-ownership project.
#
# Copyright Joe Strickler, 2016. All rights reserved.
#

.PHONY = check-update clean dist docs env help html lint pdf pristine test

PROJECT = flake8-ownership

VIRTUALENV ?= virtualenv

PWD := $(shell pwd)
ENV = $(PWD)/.env

ENV_SOURCES = $(PWD)/setup.py $(PWD)/requirements.txt
README = $(PWD)/README.rst
SOURCES = $(PWD)/src/flake8_ownership.py

COVERAGE = $(ENV)/bin/coverage
FLAKE8 = $(ENV)/bin/flake8
PIP = $(ENV)/bin/pip
PYTHON = $(ENV)/bin/python
SPHINX = $(ENV)/bin/sphinx-build
UPDATED_ENV = $(ENV)/updated

DIST = $(PWD)/dist/$(PROJECT)-$(shell python setup.py --version).tar.gz

FORCE_UPDATES_TO_PYTHON_PACKAGES = pip setuptools wheel
IGNORE_UPDATES_TO_PYTHON_PACKAGES = "\($(PROJECT)\)\|\(virtualenv\)"


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
	@printf "  test          Run tests\n\n"


# =============================================================================
# ----- Environment -----------------------------------------------------------
# =============================================================================

$(PYTHON) :
	$(VIRTUALENV) --python=python2.7 $(ENV)

$(PIP) : $(PYTHON)

$(UPDATED_ENV) : $(PIP) $(ENV_SOURCES)
	$(PIP) install -U $(FORCE_UPDATES_TO_PYTHON_PACKAGES)
	$(PIP) install \
		--editable . \
		--requirement requirements.txt
	touch $(UPDATED_ENV)

env : $(UPDATED_ENV)

check-update : env
	@printf "Checking for library updates...\n"
	@$(PIP) list --outdated --local | \
		grep -v $(IGNORE_UPDATES_TO_PYTHON_PACKAGES) ||\
		printf "All libraries are up to date :)\n"

pristine : clean
	git clean -dfX


# =============================================================================
# ----- QA/Test ---------------------------------------------------------------
# =============================================================================

lint : env
	$(FLAKE8) --ignore=D203 doc/conf.py setup.py src
	@printf "Flake8 is happy :)\n"

test : lint
	$(COVERAGE) run setup.py test
	$(COVERAGE) report
	$(COVERAGE) html


# =============================================================================
# ----- Documentation ---------------------------------------------------------
# =============================================================================

html : env
	cd doc; make html SPHINXBUILD=$(SPHINX)

pdf : env
	cd doc; make latexpdf SPHINXBUILD=$(SPHINX)

docs: html pdf


# =============================================================================
# ----- Build -----------------------------------------------------------------
# =============================================================================

$(DIST) : $(README) $(SOURCES) $(UPDATED_ENV)
	cp $(README) README
	-$(PYTHON) setup.py sdist && touch $(DIST)
	rm README

dist : $(DIST)

clean :
	rm -rf \
		$(shell find . -type f -name .DS_Store) \
		$(shell find src -type f -name *.pyc) \
		.coverage \
		coverage \
		dist
