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
import warnings

import pytest

from stdio_mgr import stdio_mgr


def pytest_addoption(parser):
    """Add custom CLI options to pytest."""
    parser.addoption(
        "--skipwarnings",
        action="store_true",
        help=("Skip tests that intentionally raise warnings"),
    )


@pytest.fixture(scope="session")
def skip_warnings(pytestconfig):
    """Provide concise access to '--skipwarnings' CLI option."""
    skip_warnings = pytestconfig.getoption("--skipwarnings")

    if not skip_warnings:
        # Check pytest was no invoked with -p no:warnings.
        try:
            impl = warnings._showwarnmsg_impl
        except AttributeError:
            # Python < 3.6
            impl = warnings.showwarning
        assert (
            impl.__name__ != "append"
        ), "Please use pytest -p no:warnings or pytest --skipwarnings"

    return skip_warnings


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
