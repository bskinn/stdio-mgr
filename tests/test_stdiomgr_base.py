r"""*Base submodule for the* ``stdio_mgr`` *test suite*.

``stdio_mgr`` provides a context manager for convenient
mocking and/or wrapping of ``stdin``/``stdout``/``stderr``
interactions.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    24 Mar 2018

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

import collections.abc
import io
import sys
import warnings

# AbstractContextManager was introduced in Python 3.6
try:
    from contextlib import AbstractContextManager
except ImportError:
    AbstractContextManager = object

import pytest

from stdio_mgr import stdio_mgr, StdioManager
from stdio_mgr.stdio_mgr import _Tee


def test_context_manager_instance():
    """Confirm StdioManager instance is a tuple and registered context manager."""
    cm = StdioManager()

    assert isinstance(cm, tuple)

    value_list = list(cm)

    assert isinstance(cm, collections.abc.Sequence)
    assert isinstance(cm, AbstractContextManager)
    assert not isinstance(cm, collections.abc.MutableSequence)
    assert all(isinstance(item, io.TextIOWrapper) for item in cm)

    # Check copies are equal
    assert list(cm) == value_list


def test_context_manager_instance_with():
    """Confirm StdioManager works in with."""
    with StdioManager() as cm:
        assert isinstance(cm, tuple)

        inner_value_list = list(cm)

        assert isinstance(cm, collections.abc.Sequence)
        assert isinstance(cm, AbstractContextManager)
        assert not isinstance(cm, collections.abc.MutableSequence)
        assert all(isinstance(item, io.TextIOWrapper) for item in cm)
        # Check copies are equal
        assert list(cm) == inner_value_list

    # Still equal
    assert list(cm) == inner_value_list


def test_instance_capture_stdout(convert_newlines):
    """Confirm object stdout capture."""
    with stdio_mgr() as cm:
        s = "test str"
        print(s)

        # 'print' automatically adds a newline
        assert convert_newlines(s + "\n") == cm.stdout.getvalue()


def test_capture_stdout(convert_newlines):
    """Confirm stdout capture."""
    with stdio_mgr() as (i, o, e):
        s = "test str"
        print(s)

        # 'print' automatically adds a newline
        assert convert_newlines(s + "\n") == o.getvalue()


def test_catch_warnings(convert_newlines, skip_warnings):
    """Confirm warnings under catch_warnings appear in stderr."""
    if skip_warnings:
        pytest.skip("Skip warning tests")

    with stdio_mgr() as (i, o, e):
        w = "This is a warning"

        with warnings.catch_warnings():
            warnings.simplefilter("always")
            warnings.warn(w)

        # Warning text comes at the end of a line; newline gets added
        assert convert_newlines(w + "\n") in e.getvalue()


def test_capture_stderr_print(convert_newlines):
    """Confirm stderr capture of print."""
    with stdio_mgr() as (i, o, e):
        w = "This is a warning"

        print(w, file=sys.stderr)

        # Warning text comes at the end of a line; newline gets added
        assert convert_newlines(w + "\n") in e.getvalue()


def test_capture_instance_stderr_print(convert_newlines):
    """Confirm object capture of stderr print."""
    with stdio_mgr() as cm:
        w = "This is a warning"

        print(w, file=sys.stderr)

        # Warning text comes at the end of a line; newline gets added
        assert convert_newlines(w + "\n") in cm.stderr.getvalue()


def test_capture_stderr_warn(convert_newlines, skip_warnings):
    """Confirm stderr capture of warnings.warn."""
    if skip_warnings:
        pytest.skip("Skip warning tests")

    with stdio_mgr() as (i, o, e):
        w = "This is a warning"

        warnings.warn(w)

        # Warning text comes at the end of a line; newline gets added
        assert convert_newlines(w + "\n") in e.getvalue()


def test_default_stdin(convert_newlines):
    """Confirm stdin default-populate."""
    in_str = "This is a test string.\n"

    with stdio_mgr(in_str) as (i, o, e):
        assert in_str == i.getvalue()

        out_str = input()

        # TeeStdin tees the stream contents, *including* the newline,
        # to the managed stdout
        assert convert_newlines(in_str) == o.getvalue()

        # 'input' strips the trailing newline before returning
        assert convert_newlines(in_str[:-1]) == out_str


def test_capture_instance_stdin(convert_newlines):
    """Confirm object stdin."""
    in_str = "This is a test string.\n"

    with stdio_mgr(in_str) as cm:
        assert in_str == cm.stdin.getvalue()

        out_str = input()

        # TeeStdin tees the stream contents, *including* the newline,
        # to the managed stdout
        assert convert_newlines(in_str) == cm.stdout.getvalue()

        # 'input' strips the trailing newline before returning
        assert convert_newlines(in_str[:-1]) == out_str


def test_managed_stdin(convert_newlines):
    """Confirm stdin populate within context."""
    str1 = "This is a test string."
    str2 = "This is another test string.\n"

    with stdio_mgr() as (i, o, e):
        # Preload str1 to stdout, and check. As above, 'print'
        # appends a newline
        print(str1)
        assert convert_newlines(str1 + "\n") == o.getvalue()

        # Use custom method .append to add the contents
        # without moving the seek position; check stdin contents.
        # The newline remains, since the stream contents were not
        # run through 'input'
        i.append(convert_newlines(str2))
        assert convert_newlines(str2) == i.getvalue()

        # Pull the contents of stdin to variable
        out_str = input()

        # stdout should have both strings. The newline of str2 is
        # *retained* here, because str2 was teed from stdin upon
        # the read of stdin by the above 'input' call.
        assert convert_newlines(str1 + "\n" + str2) == o.getvalue()

        # 'input' should just have put str2 to out_str, *without*
        # the trailing newline, per normal 'input' behavior.
        assert convert_newlines(str2[:-1]) == out_str


def test_repeated_use(convert_newlines):
    """Confirm repeated stdio_mgr use works correctly."""
    for _ in range(4):
        # Tests both stdin and stdout
        test_default_stdin(convert_newlines)

        # Tests stderr
        test_capture_stderr_print(convert_newlines)


def test_noop():
    """Confirm sys module state is restored after use."""
    real_sys_stdio = (sys.stdin, sys.stdout, sys.stderr)

    stdio_mgr()
    assert (sys.stdin, sys.stdout, sys.stderr) == real_sys_stdio

    with stdio_mgr():
        pass
    assert (sys.stdin, sys.stdout, sys.stderr) == real_sys_stdio


def test_exception():
    """Confirm state is restored after an exception during context."""
    real_sys_stdio = (sys.stdin, sys.stdout, sys.stderr)
    with pytest.raises(ZeroDivisionError):
        with stdio_mgr() as (i, o, e):
            1 / 0
    assert (sys.stdin, sys.stdout, sys.stderr) == real_sys_stdio


def test_manual_close(convert_newlines):
    """Confirm files remain open if close=False after the context has exited."""
    with stdio_mgr(close=False) as (i, o, e):
        test_default_stdin(convert_newlines)

        test_capture_stderr_print(convert_newlines)

    assert not i.closed
    assert not o.closed
    assert not e.closed

    i.close()
    o.close()
    e.close()


def test_manual_close_detached_fails(convert_newlines):
    """Confirm files kept open become unusable after being detached."""
    with stdio_mgr(close=False) as (i, o, e):
        test_default_stdin(convert_newlines)

        test_capture_stderr_print(convert_newlines)

        i.detach()
        o.detach()
        e.detach()

        with pytest.raises(ValueError) as err:
            i.close()

        assert str(err.value) == "underlying buffer has been detached"

        with pytest.raises(ValueError):
            i.closed
        with pytest.raises(ValueError):
            o.close()
        with pytest.raises(ValueError):
            o.closed
        with pytest.raises(ValueError):
            e.close()
        with pytest.raises(ValueError):
            e.closed

    with pytest.raises(ValueError) as err:
        i.close()

    assert str(err.value) == "underlying buffer has been detached"

    with pytest.raises(ValueError):
        i.closed
    with pytest.raises(ValueError):
        o.close()
    with pytest.raises(ValueError):
        o.closed
    with pytest.raises(ValueError):
        e.close()
    with pytest.raises(ValueError):
        e.closed


def test_stdin_closed(convert_newlines):
    """Confirm stdin's buffer can be closed within the context."""
    with stdio_mgr() as (i, o, e):
        print("test str")

        i.close()

        with pytest.raises(ValueError) as err:
            i.getvalue()

        assert str(err.value) == "I/O operation on closed file."

        with pytest.raises(ValueError) as err:
            i.append("anything")

        assert str(err.value) == "I/O operation on closed file."

        assert convert_newlines("test str\n") == o.getvalue()

    assert convert_newlines("test str\n") == o.getvalue()


def test_stdin_detached(convert_newlines):
    """Confirm stdin's buffer can be detached within the context.

    Like the real sys.stdin, use after detach should fail with ValueError.
    """
    with stdio_mgr() as (i, o, e):
        print("test str")

        f = i.detach()

        with pytest.raises(ValueError) as err:
            i.read()

        assert str(err.value) == "underlying buffer has been detached"

        with pytest.raises(ValueError) as err:
            i.getvalue()

        assert str(err.value) == "underlying buffer has been detached"

        with pytest.raises(ValueError) as err:
            i.append("anything")

        assert str(err.value) == "underlying buffer has been detached"

        assert convert_newlines("test str\n") == o.getvalue()

        print("second test str")

        assert convert_newlines("test str\nsecond test str\n") == o.getvalue()

        with pytest.raises(ValueError) as err:
            i.closed

        assert str(err.value) == "underlying buffer has been detached"

    assert convert_newlines("test str\nsecond test str\n") == o.getvalue()

    assert not f.closed

    with pytest.raises(ValueError) as err:
        i.closed

    assert str(err.value) == "underlying buffer has been detached"

    assert o.closed
    assert e.closed


def test_stdout_detached(convert_newlines):
    """Confirm stdout's buffer can be detached within the context.

    Like the real sys.stdout, writes after detach should fail, however
    writes to the detached stream should be captured.
    """
    with stdio_mgr() as (i, o, e):
        print("test str")

        f = o.detach()

        assert isinstance(f, io.BufferedRandom)
        assert f is o._buf
        assert f is i.tee._buf

        assert convert_newlines("test str\n") == o.getvalue()

        with pytest.raises(ValueError) as err:
            o.write("second test str\n")

        assert str(err.value) == "underlying buffer has been detached"

        assert convert_newlines("test str\n") == o.getvalue()

        with pytest.raises(ValueError) as err:
            print("anything")

        assert str(err.value) == "underlying buffer has been detached"

        f.write(convert_newlines("second test str\n").encode("utf8"))
        f.flush()

        assert convert_newlines("test str\nsecond test str\n") == o.getvalue()

        with pytest.raises(ValueError) as err:
            o.closed

        assert str(err.value) == "underlying buffer has been detached"

    assert convert_newlines("test str\nsecond test str\n") == o.getvalue()

    assert not f.closed

    with pytest.raises(ValueError) as err:
        o.closed

    assert str(err.value) == "underlying buffer has been detached"

    assert i.closed
    assert e.closed


def test_stdout_access_buffer_after_close(convert_newlines):
    """Confirm stdout's buffer is captured after close."""
    with stdio_mgr() as (i, o, e):
        print("test str")

        assert convert_newlines("test str\n") == o.getvalue()

        print("second test str")
        o.close()

        with pytest.raises(ValueError) as err:
            o.read()

        assert str(err.value) == "I/O operation on closed file."

        assert convert_newlines("test str\nsecond test str\n") == o.getvalue()

        with pytest.raises(ValueError) as err:
            print("anything")

        assert str(err.value) == "I/O operation on closed file."

        assert convert_newlines("test str\nsecond test str\n") == o.getvalue()

    assert convert_newlines("test str\nsecond test str\n") == o.getvalue()


def test_tee_type():
    """Test that incorrect type for Tee.tee raises ValueError."""
    with pytest.raises(ValueError) as err:
        _Tee(tee="str", buffer=io.StringIO())

    assert str(err.value) == "tee must be a TextIOBase."


@pytest.mark.xfail(reason="Want to ensure 'real' warnings aren't suppressed")
def test_bare_warning(skip_warnings):
    """Test that a "real" warning is exposed when raised."""
    from enum import Enum

    # skip_warnings=True implies that pytest is being run with warning
    # reporting ENABLED. So, proceed to warning test.
    # skip_warnings=False implies that pytest is being run with
    # -p no:warnings, and thus the below warning will be suppressed.
    # Thus, for the latter case, a forced fail is appropriate
    assert skip_warnings

    class Foo(Enum):
        One = 1
        Two = 2

    "foo" in Foo
