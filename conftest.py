r"""*pytest configuration for the* ``stdio_mgr`` *test suite*.

``stdio_mgr`` provides a context manager for convenient
mocking and/or wrapping of ``stdin``/``stdout``/``stderr``
interactions.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    6 Feb 2019

**Copyright**
    \(c) Brian Skinn 2018-2019

**Source Repository**
    http://www.github.com/bskinn/stdio-mgr

**Documentation**
    See README.rst at the GitHub repository

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import sys

import pytest

from stdio_mgr import stdio_mgr


@pytest.fixture(autouse=True)
def add_stdio_mgr(doctest_namespace):
    """Add stdio_mgr to doctest namespace."""
    doctest_namespace["stdio_mgr"] = stdio_mgr


@pytest.fixture(scope="session")
def convert_newlines():
    """Supply platform-dependent newline transform function."""
    if sys.platform == "win32":
        return lambda s: s.replace("\n", "\r\n")
    else:
        return lambda s: s
