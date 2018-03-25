# ------------------------------------------------------------------------------
# Name:        stdio_mgr_base
# Purpose:     Core test module for stdio_mgr
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     24 Mar 2018
# Copyright:   (c) Brian Skinn 2018
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#              https://www.github.com/bskinn/stdio-mgr
#
# ------------------------------------------------------------------------------

"""Base submodule for the stdio_mgr test suite."""

import unittest as ut


class TestStdioMgrExpectGood(ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_CaptureStdout(self):
        """Confirm stdout capture."""
        import sys
        from stdio_mgr import stdio_mgr

        with stdio_mgr(sys) as (i, o, e):
            s = 'test str'
            print(s)
            self.assertEqual(s + '\n', o.getvalue())

    def test_CaptureStderr(self):
        """Confirm stderr capture."""
        import sys
        import warnings
        from stdio_mgr import stdio_mgr

        with stdio_mgr(sys) as (i, o, e):
            w = 'This is a warning'
            warnings.warn(w)
            self.assertIn(w + '\n', e.getvalue())


def suite_all():
    """Create and return the test suite for all tests."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestStdioMgrExpectGood)])

    return s


if __name__ == '__main__':
    print("Module not executable.")
