stdio Manager
=============

*Python context manager for mocking/wrapping stdin/stdout/stderr*

.. image:: https://travis-ci.org/bskinn/stdio-mgr.svg?branch=dev
    :target: https://travis-ci.org/bskinn/stdio-mgr

.. image:: https://codecov.io/gh/bskinn/stdio-mgr/branch/dev/graph/badge.svg
    :target: https://codecov.io/gh/bskinn/stdio-mgr

.. image:: https://img.shields.io/pypi/v/stdio_mgr.svg
    :target: https://pypi.org/project/stdio-mgr

.. image:: https://img.shields.io/pypi/pyversions/stdio-mgr.svg

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/bskinn/stdio-mgr/blob/master/LICENSE.txt

Have a command-line Python application? Want to test *[...continued]*



*[more about mocking stdio]*


In addition to mocking `stdio` for testing, `stdio_mgr` can also be used to
wrap functions that directly interact with `stdio`. Example:

.. code::

    >>> def embellish(func):
    ...     def func_wrapper(s):
    ...         import sys
    ...         from stdio_mgr import stdio_mgr
    ...
    ...         with stdio_mgr() as (i, o, e):
    ...             func(s)
    ...             content = o.getvalue()
    ...         newcontent = '*** ' + content.replace('\n', ' ***\n*** ')
    ...         newcontent = newcontent[:-5]
    ...         print(newcontent)
    ...     return func_wrapper

    >>> @embellish
    ... def testfunc(s):
    ...     print(s)

    >>> testfunc("""\
    ... Foo bar baz quux.
    ... Lorem ipsum dolor sit amet....""")
    *** Foo bar baz quux. ***
    *** Lorem ipsum dolor sit amet.... ***

