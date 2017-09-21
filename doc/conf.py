# -*- coding: utf-8 -*-
"""
Sphinx configuration file for flake8-ownership.

:author: Joe Joyce <joe@decafjoe.com>
:copyright: Copyright (c) Joe Joyce and contributors, 2016-2017.
:license: BSD
"""
import os
import sys


root_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
src_path = os.path.join(root_path, 'src')
sys.path.insert(0, src_path)


# =============================================================================
# -- General configuration ----------------------------------------------------
# =============================================================================

# Basic project information
project = u'flake8-ownership'
copyright = u'2016-2017, Joe Joyce and contributors'
author = u'Joe Joyce'
version = u'1.0'
release = u'1.0.3'

# Paths
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
master_doc = 'index'
source_suffix = '.rst'
templates_path = []

# Miscellaneous
language = None
pygments_style = 'sphinx'

# Extensions.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]


# =============================================================================
# -- HTML ---------------------------------------------------------------------
# =============================================================================

html_theme = 'sphinx_rtd_theme'
html_static_path = []
htmlhelp_basename = '%s-doc' % project


# =============================================================================
# -- LaTeX --------------------------------------------------------------------
# =============================================================================

# Basic config
latex_elements = {}
latex_documents = [
    (
        master_doc,
        '%s.tex' % project,
        project,
        author,
        'manual',
    ),
]

# References
latex_show_pagerefs = True
latex_show_urls = 'footnote'


# =============================================================================
# -- Man page -----------------------------------------------------------------
# =============================================================================

man_pages = [
    (
        master_doc,
        project,
        project,
        [author],
        7,
    ),
]
man_show_urls = True


# =============================================================================
# -- Texinfo ------------------------------------------------------------------
# =============================================================================

setup_path = os.path.join(root_path, 'setup.py')
with open(setup_path) as f:
    for line in f:
        line = line.strip()
        if line.startswith('description='):
            texinfo_description = line[13:-2]
            break

texinfo_documents = [
    (
        master_doc,
        project,
        project,
        author,
        project,
        texinfo_description,
        'Miscellaneous',
    ),
]
texinfo_show_urls = 'footnote'


# =============================================================================
# -- sphinx.ext.intersphinx ---------------------------------------------------
# =============================================================================

intersphinx_mapping = {
    'https://docs.python.org/': None,
}


# =============================================================================
# -- sphinx.ext.todo ----------------------------------------------------------
# =============================================================================

todo_include_todos = True
