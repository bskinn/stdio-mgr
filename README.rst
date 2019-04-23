stdio Manager: Context manager for mocking/wrapping ``stdin``/``stdout``/``stderr``
===================================================================================

**Current Development Version:**

.. image:: https://travis-ci.org/bskinn/stdio-mgr.svg?branch=dev
    :target: https://travis-ci.org/bskinn/stdio-mgr

.. image:: https://codecov.io/gh/bskinn/stdio-mgr/branch/dev/graph/badge.svg
    :target: https://codecov.io/gh/bskinn/stdio-mgr

**Most Recent Stable Release:**

.. image:: https://img.shields.io/pypi/v/stdio_mgr.svg
    :target: https://pypi.org/project/stdio-mgr

.. image:: https://img.shields.io/pypi/pyversions/stdio-mgr.svg

**Info:**

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/bskinn/stdio-mgr/blob/master/LICENSE.txt

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

----

**Have a CLI Python application?**

**Want to automate testing of the actual console input & output
of your user-facing components?**

`stdio Manager` can help.

While some functionality here is more or less duplicative of
``redirect_stdout`` and ``redirect_stderr`` in ``contextlib``
`within the standard library <https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout>`__,
it provides (i) a much more concise way to mock both ``stdout`` and ``stderr`` at the same time,
and (ii) a mechanism for mocking ``stdin``, which is not available in ``contextlib``.

**First, install:**

.. code::

    $ pip install stdio-mgr

Then use!

All of the below examples assume ``stdio_mgr`` has already
been imported via:

.. code::

    from stdio_mgr import stdio_mgr

**Mock** ``stdout``\ **:**

.. code::

    >>> with stdio_mgr() as (in_, out_, err_):
    ...     print('foobar')
    ...     out_cap = out_.getvalue()
    >>> out_cap
    'foobar\n'
    >>> in_.closed and out_.closed and err_.closed
    True

By default ``print``
`appends a newline <https://docs.python.org/3/library/functions.html#print>`__
after each argument, which is why ``out_cap`` is ``'foobar\n'``
and not just ``'foobar'``.

As currently implemented, ``stdio_mgr`` closes all three mocked streams
upon exiting the managed context.


**Mock** ``stderr``\ **:**

.. code ::

    >>> import warnings
    >>> with stdio_mgr() as (in_, out_, err_):
    ...     warnings.warn("foo has no bar")
    ...     err_cap = err_.getvalue()
    >>> err_cap
    '...UserWarning: foo has no bar\n...'


**Mock** ``stdin``\ **:**

The simulated user input has to be pre-loaded to the mocked stream.
**Be sure to include newlines in the input to correspond to
each mocked** `Enter` **keypress!**
Otherwise, ``input`` will hang, waiting for a newline
that will never come.

If the entirety of the input is known in advance,
it can just be provided as an argument to ``stdio_mgr``.
Otherwise, ``.append()`` mocked input to ``in_``
within the managed context as needed:

.. code::

    >>> with stdio_mgr('foobar\n') as (in_, out_, err_):
    ...     print('baz')
    ...     in_cap = input('??? ')
    ...
    ...     _ = in_.append(in_cap[:3] + '\n')
    ...     in_cap2 = input('??? ')
    ...
    ...     out_cap = out_.getvalue()
    >>> in_cap
    'foobar'
    >>> in_cap2
    'foo'
    >>> out_cap
    'baz\n??? foobar\n??? foo\n'

The ``_ =`` assignment suppresses ``print``\ ing of the return value
from the ``in_.append()`` call--otherwise, it would be interleaved
in ``out_cap``, since this example is shown for an interactive context.
For non-interactive execution, as with ``unittest``, ``pytest``, etc.,
these 'muting' assignments should not be necessary.

**Both** the ``'??? '`` prompts for ``input``
**and** the mocked input strings
are echoed to ``out_``, mimicking what a CLI user would see.

A subtlety: While the trailing newline on, e.g., ``'foobar\n'`` is stripped
by ``input``, it is *retained* in ``out_``.
This is because ``in_`` tees the content read from it to ``out_``
*before* that content is passed to ``input``.


**Want to modify internal** ``print`` **calls
within a function or method?**

In addition to mocking, ``stdio_mgr`` can also be used to
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
    ... Lorem ipsum dolor sit amet.""")
    ===============================
    | Foo bar baz quux.           |
    | Lorem ipsum dolor sit amet. |
    ===============================

----

Available on `PyPI <https://pypi.python.org/pypi/stdio-mgr>`__
(``pip install stdio-mgr``).

Source on `GitHub <https://github.com/bskinn/stdio-mgr>`__.  Bug reports
and feature requests are welcomed at the
`Issues <https://github.com/bskinn/stdio-mgr/issues>`__ page there.

Copyright \(c) 2018-2019 Brian Skinn

License: The MIT License. See `LICENSE.txt <https://github.com/bskinn/stdio-mgr/blob/master/LICENSE.txt>`__
for full license terms.

