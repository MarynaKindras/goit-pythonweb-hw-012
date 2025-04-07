# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path

# Додаємо шлях до src директорії
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

# Встановлюємо змінні середовища для імпорту
os.environ['CLD_NAME'] = 'test'
os.environ['CLD_API_KEY'] = '326488457974591'
os.environ['CLD_API_SECRET'] = 'test'
os.environ['SECRET_KEY'] = 'test'
os.environ['ALGORITHM'] = 'HS256'
os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = '30'
os.environ['REFRESH_TOKEN_EXPIRE_DAYS'] = '7'

project = 'Contacts API'
copyright = '2024, Your Name'
author = 'Your Name'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'uk'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
