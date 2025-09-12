# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'AriAstro'
copyright = '2025, Varghese Reji'
author = 'Varghese Reji'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'

html_logo = "_static/AriAstro_logo.png"
html_static_path = ['_static']

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",   # optional: for Google/NumPy style docstrings
    "sphinx.ext.viewcode",   # optional: adds links to source code
]

