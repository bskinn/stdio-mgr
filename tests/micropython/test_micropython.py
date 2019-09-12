r"""``unittest`` *tests for MicroPython, for* ``stdio-mgr``.

``stdio_mgr`` provides a context manager for convenient
mocking and/or wrapping of ``stdin``/``stdout``/``stderr``
interactions.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    12 Sep 2019

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

import unittest as ut


class TestDummyTest(ut.TestCase):
    """Initial stub test to confirm unittest suite is working."""

    def test_dummy_test(self):
        """Confirm that a trivial test passes."""
        self.assertTrue(True)


if __name__ == "__main__":
    ut.main()
