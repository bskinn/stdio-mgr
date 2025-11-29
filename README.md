## stdio-mgr: Context manager for mocking/wrapping `stdin`/`stdout`/`stderr`

#### Current Development Version:

[![GitHub Workflow Status][workflow badge]][workflow link target]

#### Most Recent Stable Release

[![PyPI Version][pypi badge]][pypi link target]
![Python Versions][python versions badge]

#### Info

[![MIT License][license badge]][license link target]
[![black formatted][black badge]][black link target]
[![PePY stats][pepy badge]][pepy link target]

----

### Have a CLI Python application?

_Want to automate testing of the actual console input & output of your
user-facing components?_

#### `stdio-mgr` can help

`stdio-mgr` is a context manager for mocking/managing all three standard I/O
streams: `stdout`, `stderr`, and `stdin`. While some functionality here is more
or less duplicative of `redirect_stdout` and `redirect_stderr` in
`contextlib` [within the standard library][stdlib redirect_stdout],
it provides (i) a much more concise way to mock both `stdout` and `stderr`
at the same time, and (ii) a mechanism for mocking `stdin`, which is not
available in `contextlib`.

##### First, install:

```bash
$ pip install stdio-mgr
```

Then use!

All of the below examples assume `stdio_mgr` has already been imported via:

```py
from stdio_mgr import stdio_mgr
```

##### Mock `stdout`:

```py
>>> with stdio_mgr() as (in_, out_, err_):
...     print('foobar')
...     out_cap = out_.getvalue()
>>> out_cap
'foobar\n'
>>> in_.closed and out_.closed and err_.closed
True

```

By default `print` [appends a newline][print newline] after each argument, which
is why `out_cap` is `'foobar\n'` and not just `'foobar'`.

As currently implemented, `stdio_mgr` closes all three mocked streams upon
exiting the managed context.


##### Mock `stderr`:

```py
>>> import warnings
>>> with stdio_mgr() as (in_, out_, err_):
...     warnings.warn("'foo' has no 'bar'")
...     err_cap = err_.getvalue()
>>> err_cap
'... UserWarning: \'foo\' has no \'bar\'\n...'

```


##### Mock `stdin`:

The simulated user input has to be pre-loaded to the mocked stream. **Be sure to
include newlines in the input to correspond to each mocked** `Enter`
**keypress!** Otherwise, `input` will hang, waiting for a newline that will
never come.

If the entirety of the input is known in advance, it can just be provided as an
argument to `stdio_mgr`. Otherwise, `.append()` mocked input to `in_` within the
managed context as needed:

```py
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

```

The `_ =` assignment suppresses `print`ing of the return value from the
`in_.append()` call—otherwise, it would be interleaved in `out_cap`, since this
example is shown for an interactive context. For non-interactive execution, as
with `unittest`, `pytest`, etc., these 'muting' assignments should not be
necessary.

**Both** the `'??? '` prompts for `input` **and** the mocked input strings are
echoed to `out_`, mimicking what a CLI user would see.

A subtlety: While the trailing newline on, e.g., `'foobar\n'` is stripped by
`input`, it is *retained* in `out_`. This is because `in_` tees the content read
from it to `out_` *before* that content is passed to `input`.


#### Want to modify internal `print` calls within a function or method?

In addition to mocking, `stdio_mgr` can also be used to wrap functions that
directly output to `stdout`/`stderr`. A `stdout` example:

```py
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

```

----

Available on [PyPI][pypi link target] (`pip install stdio-mgr`).

Source on [GitHub][gh repo]. Bug reports and feature requests are welcomed at
the [Issues][gh issues] page there.

Copyright \(c) 2018-2019 Brian Skinn

The `stdio-mgr` documentation (currently docstrings and README) is licensed
under a [Creative Commons Attribution 4.0 International License][cc-by] (CC-BY).
The `stdio-mgr` codebase is released under the [MIT License]. See
[`LICENSE.txt`] for full license terms.


[`LICENSE.txt`]: https://github.com/bskinn/flake8-absolute-import/blob/main/LICENSE.txt

[black badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black link target]: https://github.com/psf/black

[cc-by]: http://creativecommons.org/licenses/by/4.0/

[gh issues]: https://github.com/bskinn/stdio-mgr/issues
[gh repo]: https://github.com/bskinn/stdio-mgr

[license badge]: https://img.shields.io/github/license/mashape/apistatus.svg
[license link target]: https://github.com/bskinn/stdio-mgr/blob/stable/LICENSE.txt

[MIT License]: https://opensource.org/licenses/MIT

[pepy badge]: https://pepy.tech/badge/stdio-mgr/month
[pepy link target]: https://pepy.tech/projects/stdio-mgr?timeRange=threeMonths&category=version&includeCIDownloads=true&granularity=daily&viewType=line&versions=1.0.1%2C1.0.1.1

[print newline]: https://docs.python.org/3/library/functions.html#print

[pypi badge]: https://img.shields.io/pypi/v/stdio-mgr.svg?logo=pypi
[pypi link target]: https://pypi.org/project/stdio-mgr

[python versions badge]: https://img.shields.io/pypi/pyversions/stdio-mgr.svg?logo=python

[stdlib redirect_stdout]: https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout

[workflow badge]: https://img.shields.io/github/actions/workflow/status/bskinn/stdio-mgr/all_core_tests.yml?branch=main&logo=github
[workflow link target]: https://github.com/bskinn/stdio-mgr/actions
