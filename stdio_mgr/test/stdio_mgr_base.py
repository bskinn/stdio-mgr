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

            # 'print' automatically adds a newline
            self.assertEqual(s + '\n', o.getvalue())

    def test_CaptureStderr(self):
        """Confirm stderr capture."""
        import sys
        import warnings
        from stdio_mgr import stdio_mgr

        with stdio_mgr(sys) as (i, o, e):
            w = 'This is a warning'
            warnings.warn(w)

            # Warning text comes at the end of a line; newline gets added
            self.assertIn(w + '\n', e.getvalue())

    def test_DefaultStdin(self):
        """Confirm stdin default-populate."""
        import sys
        from stdio_mgr import stdio_mgr

        in_str = 'This is a test string.\n'

        with stdio_mgr(sys, in_str) as (i, o, e):
            self.assertEqual(in_str, i.getvalue())

            out_str = input()

            # TeeStdin tees the stream contents, *including* the newline,
            # to the managed stdout
            self.assertEqual(in_str, o.getvalue())

            # 'input' strips the trailing newline before returning
            self.assertEqual(in_str[:-1], out_str)

    def test_ManagedStdin(self):
        """Confirm stdin populate within context."""
        import sys
        from stdio_mgr import stdio_mgr

        str1 = 'This is a test string.'
        str2 = 'This is another test string.\n'

        with stdio_mgr(sys) as (i, o, e):
            # Preload str1 to stdout, and check. As above, 'print'
            # appends a newline
            print(str1)
            self.assertEqual(str1 + '\n', o.getvalue())

            # Use custom method .append to add the contents
            # without moving the seek position; check stdin contents.
            # The newline remains, since the stream contents were not
            # run through 'input'
            i.append(str2)
            self.assertEqual(str2, i.getvalue())

            # Pull the contents of stdin to variable
            out_str = input()

            # stdout should have both strings. The newline of str2 is
            # *retained* here, because str2 was teed from stdin upon
            # the read of stdin by the above 'input' call.
            self.assertEqual(str1 + '\n' + str2, o.getvalue())

            # 'input' should just have put str2 to out_str, *without*
            # the trailing newline, per normal 'input' behavior.
            self.assertEqual(str2[:-1], out_str)


def suite_all():
    """Create and return the test suite for all tests."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestStdioMgrExpectGood)])

    return s


if __name__ == '__main__':
    print("Module not executable.")
