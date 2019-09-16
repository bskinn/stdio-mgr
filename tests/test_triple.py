r"""*Submodule for test suite of the* ``stdio_mgr.types`` components.

**Author**
    John Vandenberg (jayvdb@gmail.com)

**File Created**
    6 Sep 2019

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

import io

import pytest

from stdio_mgr.stdio_mgr import _IMPORT_SYS_STREAMS, _RUNTIME_SYS_STREAMS
from stdio_mgr.triple import FakeIOTriple, IOTriple, TextIOTriple
from stdio_mgr.types import ClosingStdioTuple


def _create_dummy_wrapper():
    return io.TextIOWrapper(io.BufferedRandom(io.BytesIO()))


def _create_dummy_wrapper_tuple():
    return (
        io.TextIOWrapper(io.BufferedRandom(io.BytesIO())),
        io.TextIOWrapper(io.BufferedRandom(io.BytesIO())),
        io.TextIOWrapper(io.BufferedRandom(io.BytesIO())),
    )


class _UnsafeCloseIOTriple(IOTriple, ClosingStdioTuple):
    pass


class _SafeCloseIOTriple(IOTriple, ClosingStdioTuple):

    close = ClosingStdioTuple.safe_close


def test_sys_module(request):
    """Confirm sys module objects are of expected types."""
    assert isinstance(_RUNTIME_SYS_STREAMS, TextIOTriple)

    # This probably isnt enough, due to capture.py _py36_windowsconsoleio_workaround
    if request.config.known_args_namespace.capture == "no":
        assert isinstance(_RUNTIME_SYS_STREAMS, TextIOTriple)
    else:
        assert isinstance(_IMPORT_SYS_STREAMS, FakeIOTriple)


def test_stdio_base_close():
    """Test StdioTupleBase close()."""
    cm = _UnsafeCloseIOTriple((io.BytesIO(), io.BytesIO(), io.BytesIO()))

    with cm:
        assert not cm.stdin.closed
        assert not cm.stdout.closed
        assert not cm.stderr.closed
        assert not cm.any_("closed")

    assert cm.stdin.closed
    assert cm.stdout.closed
    assert cm.stderr.closed
    assert cm.all_("closed")

    cm = _UnsafeCloseIOTriple(_create_dummy_wrapper_tuple())

    # Detaching works ok.
    cm.stdout.detach()

    cm = _UnsafeCloseIOTriple(_create_dummy_wrapper_tuple())

    # Detaching causes the __exit__ to fail
    with pytest.raises(ValueError) as err:
        with cm:
            cm.stdout.detach()

    assert str(err.value) == "underlying buffer has been detached"


def test_stdio_base_safe_close():
    """Test ClosingStdioTuple safe_close()."""
    cm = _SafeCloseIOTriple(_create_dummy_wrapper_tuple())

    with cm:
        cm.stdout.detach()

    assert cm.stdin.closed
    assert cm.stderr.closed
    assert cm.suppress_all(ValueError, "closed")


def test_incorrect_item_types():
    """Test that incorrect item type do not raise unexpected exceptions."""
    empty_string = ""
    empty_string_tuple = (empty_string, empty_string, empty_string)

    # Ensure empty_string used has no __enter__, __exit__ or close()
    assert not hasattr(empty_string, "__enter__")
    assert not hasattr(empty_string, "__exit__")
    assert not hasattr(empty_string, "close")

    # The base types can be instantiated with any type
    ClosingStdioTuple(empty_string_tuple)

    # But may fail when used in a context
    with pytest.raises(AttributeError) as err:
        with ClosingStdioTuple(empty_string_tuple):
            pass

    assert str(err.value) == "'str' object has no attribute 'close'"

    # The base safe close also doesnt handle closing incorrect types,
    # as it only valid types that become unusable, raising ValueError
    with pytest.raises(AttributeError) as err:
        with _SafeCloseIOTriple(empty_string_tuple):
            pass

    assert str(err.value) == "'str' object has no attribute 'close'"

    # TextIOTuple requires TextIOBase members
    with pytest.raises(ValueError) as err:
        TextIOTriple(empty_string_tuple)

    assert str(err.value) == "iterable must contain only TextIOBase"
