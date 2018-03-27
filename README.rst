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

|larger|\ **Have a command-line Python application?
Want to automate testing of the actual console input & output
of your user-facing CLI components?**\ |/larger|

|larger|\ `stdio Manager` can help.\ |/larger|

|large|\ **First, install:**\ |/large|

.. code::

    $ pip install stdio-mgr

Then use!

All of the below examples assume ``stdio_mgr`` has already
been imported via:

.. code::

    ``from stdio_mgr import stdio_mgr``.

|large|\ **Mock** ``stdout``\ **:**\ |/large|

.. code::

    >>> with stdio_mgr() as (in_, out_, err_):
    ...     print('foobar')
    ...     capture = out_.getvalue()
    >>> capture
    'foobar\n'

Note that by default ``print``
`appends a newline <https://docs.python.org/3/library/functions.html#print>`__
after each argument, which is why ``capture`` is ``'foobar\n'``
and not just ``'foobar'``.


|large|\ **Mock** ``stderr``\ **:**\ |/large|

.. code ::

    >>> import warnings
    >>> from stdio_mgr import stdio_mgr
    >>> with stdio_mgr() as (in_, out_, err_):
    ...     warnings.warn("'foo' has no 'bar'")
    ...     capture = err_.getvalue()
    >>> capture
    "C:\\Temp\\git\\stdiomgr\\README.rst:2: UserWarning: 'foo' has no 'bar'\n  =============\n"


|large|\ **Mock** ``stdin``\ **:**\ |/large|

The simulated user input has to be pre-loaded to the mocked stream.
Either provide it as an argument to ``stdio_mgr``:

.. code ::

    >>> # COMPLETE THIS


|larger|\ **Want to modify the internal printing behavior of a function?**\ |/larger|

In addition to mocking ``stdio`` for testing, ``stdio_mgr`` can also be used to
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



.. |large| raw:: html

    <span style="font-size: 110%">

.. |/large| raw:: html

    </span>


.. |larger| raw:: html

    <span style="font-size: 125%">

.. |/larger| raw:: html

    </span>
