# -*- coding: utf-8 -*-
"""
Sphinx configuration file for flake8-ownership.

:author: Joe Strickler <joe@decafjoe.com>
:copyright: Joe Strickler, 2016. All rights reserved.
:license: Proprietary
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
copyright = u'2016, Joe Strickler'
author = u'Joe Strickler'
version = u'0.1'
release = u'0.1.1'

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

html_theme = 'pyramid'
html_static_path = []
htmlhelp_basename = 'flake8-ownership-doc'


# =============================================================================
# -- LaTeX --------------------------------------------------------------------
# =============================================================================

# Basic config
latex_elements = {}
latex_documents = [
    (
        master_doc,
        'flake8-ownership.tex',
        u'flake8-ownership',
        u'Joe Strickler',
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
        'flake8-ownership',
        u'flake8-ownership',
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
        'flake8-ownership',
        u'flake8-ownership',
        author,
        'flake8-ownership',
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
