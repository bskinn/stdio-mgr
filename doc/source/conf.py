# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import re
from textwrap import dedent

# -- Project information -----------------------------------------------------

project = "stdio-mgr"
copyright = "2019, Brian Skinn"
author = "Brian Skinn"

# The full version, including alpha/beta/rc tags
from stdio_mgr import __version__ as release

version = re.match(r"\d+\.\d+", release).group(0)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinxcontrib.programoutput",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# reST epilog to define common substitutions
rst_epilog = """

.. |None| replace:: :obj:`None`

.. |True| replace:: :obj:`True`

.. |False| replace:: :obj:`False`

.. |int| replace:: :obj:`int`

.. |str| replace:: :obj:`str`

.. |bytes| replace:: :obj:`bytes`

.. |license_txt| replace:: LICENSE.txt
.. _license_txt: https://github.com/bskinn/stdio-mgr/blob/master/LICENSE.txt

"""

# inheritance_diagram settings
inheritance_graph_attrs = {
    "rankdir": "TB",
    "size": '"2000!"',
}

inheritance_node_attrs = {
    "fontsize": 11,
}

inheritance_alias = {
    "_io.BytesIO": "io.BytesIO",
    "_io._BufferedIOBase": "io.BufferedIOBase",
    "_io._IOBase": "io.IOBase",
    "_io.TextIOWrapper": "io.TextIOWrapper",
    "_io._TextIOBase": "io.TextIOBase",
}

graphviz_output_format = "svg"


# doctest settings
doctest_global_setup = r"""\
import re

p_strip_memaddress = re.compile(r"^(.*) at 0x[0-9A-F]+>$", re.I)

def strip_memaddress(desc_str):
    m = p_strip_memaddress.match(desc_str)

    if m:
        return m.group(1) + ">"
    else:
        return desc_str

def method_origins(cls):
    skipped_methods = ["__dict__", "__doc__"]
    methods = [m for m in dir(cls) if m not in skipped_methods]

    width = 1 + max(len(m) for m in methods)

    descs = {m: strip_memaddress(repr(getattr(cls, m))) for m in methods}

    print(*(f"{m: <{width}} :: {descs[m]}" for m in methods), sep="\n")

"""

# intersphinx docset mappings
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}
