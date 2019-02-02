# ------------------------------------------------------------------------------
# Name:        tests
# Purpose:     Master script for stdio_mgr testing suite
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     24 Mar 2018
# Copyright:   (c) Brian Skinn 2018
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#           http://www.github.com/bskinn/stdio-mgr
#
# ------------------------------------------------------------------------------


class AP(object):
    """ Container for arguments for selecting test suites.

    Also includes PFX, a helper string for substitution/formatting.

    """
    ALL = 'all'

    PFX = "--{0}"


def get_parser():
    import argparse

    # Create the parser
    prs = argparse.ArgumentParser(description="Run tests for stdio_mgr")

    # Verbosity argument
    prs.add_argument('-v', action='store_true',
                     help="Show verbose output")

    # Options without subgroups
    prs.add_argument(AP.PFX.format(AP.ALL), '-a',
                     action='store_true',
                     help="Run all tests (overrides any other selections)")

    # Return the parser
    return prs


def main():
    import os
    import os.path as osp
    import sys
    import unittest as ut

    import tests

    # Retrieve the parser
    prs = get_parser()

    # Pull the dict of stored flags, saving the un-consumed args, and
    # update sys.argv
    ns, args_left = prs.parse_known_args()
    params = vars(ns)
    sys.argv = sys.argv[:1] + args_left

    # Create the empty test suite
    ts = ut.TestSuite()

    # Helper function for adding test suites. Just uses ts and params from
    # the main() function scope
    def addsuiteif(suite, flags):
        if any(params[k] for k in flags):
            ts.addTest(suite)

    # Add commandline-indicated tests per-group
    # Expect-good tests
    addsuiteif(tests.stdio_mgr_base.suite_all(),
               [AP.ALL])

    # Create the test runner and execute
    ttr = ut.TextTestRunner(buffer=True,
                            verbosity=(2 if params['v'] else 1))

    success = ttr.run(ts).wasSuccessful()

    # Return based on success result (lets tox report success/fail)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
