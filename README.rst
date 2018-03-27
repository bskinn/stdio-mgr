stdio Manager
=============

*Python context manager for mocking/wrapping* ``stdin``/``stdout``/``stderr``

.. image:: https://travis-ci.org/bskinn/stdio-mgr.svg?branch=dev
    :target: https://travis-ci.org/bskinn/stdio-mgr
.. image:: https://codecov.io/gh/bskinn/stdio-mgr/branch/dev/graph/badge.svg
    :target: https://codecov.io/gh/bskinn/stdio-mgr
.. image:: https://img.shields.io/pypi/v/stdio_mgr.svg
    :target: https://pypi.org/project/stdio-mgr
.. image:: https://img.shields.io/pypi/pyversions/stdio-mgr.svg
.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/bskinn/stdio-mgr/blob/master/LICENSE.txt

**Have a command-line Python application?
Want to automate testing of your user-facing CLI components?**

`stdio Manager` can help.

First, install:

.. code::

    $ pip install stdio-mgr

Then use!

Mock ``stdout``:

.. code::

    >>> from stdio_mgr import stdio_mgr
    >>> with stdio_mgr() as (in_, out_, err_):
    ...     print('foobar')
    ...     capture = out_.getvalue()
    >>> print(capture)
    foobar
    <BLANKLINE>

Note that by default ``print``
`appends a newline <https://docs.python.org/3/library/functions.html#print>`__
after its argument *each time it's called*. So, ``capture`` actually refers to ``'foobar\n'``,
and the ``print(capture)`` call outputs two newlines total.
The ``<BLANKLINE>`` is thus
`needed <https://docs.python.org/2/library/doctest.html#how-are-docstring-examples-recognized>`__
to make the above example pass in ``doctest``.

*[more about mocking stdio]*


**Want to modify the internal printing behavior of a function?**

In addition to mocking `stdio` for testing, `stdio_mgr` can also be used to
wrap functions that directly output to ``stdout``/``stderr``. A ``stdout`` example:

.. code::

    >>> def emboxen(func):
    ...     def func_wrapper(s):
    ...         from stdio_mgr import stdio_mgr
    ...
    ...         with stdio_mgr() as (in_, out_, err_):
    ...             func(s)
    ...             content = out_.getvalue()
    ...
    ...         max_len = max(map(len, content.splitlines()))
    ...         fmt_str = '| {{: <{0}}} |\n'.format(max_len)
    ...
    ...         newcontent = '=' * (max_len + 4) + '\n'
    ...         for line in content.splitlines():
    ...             newcontent += fmt_str.format(line)
    ...         newcontent += '=' * (max_len + 4)
    ...
    ...         print(newcontent)
    ...
    ...     return func_wrapper

    >>> @emboxen
    ... def testfunc(s):
    ...     print(s)

    >>> testfunc("""\
    ... Foo bar baz quux.
    ... Lorem ipsum dolor sit amet....""")
    ==================================
    | Foo bar baz quux.              |
    | Lorem ipsum dolor sit amet.... |
    ==================================

