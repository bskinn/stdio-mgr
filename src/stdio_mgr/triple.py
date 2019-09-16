r"""``stdio_mgr.types`` *code module*.

``stdio_mgr.types`` provides context managers for convenient
interaction with ``stdin``/``stdout``/``stderr`` as a tuple.

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
from io import TextIOBase

from stdio_mgr.types import MultiItemIterable, TupleContextManager


class IOTriple(TupleContextManager, MultiItemIterable):
    """Base type for a type of stdin, stdout and stderr stream-like objects.

    While it is a context manager, no action is taken on entering or exiting
    the context.

    Used as a context manager, it will close all of the streams on exit.
    however it does not open the streams on entering the context manager.

    No exception handling is performed while closing the streams, so any
    exception occurring the close of any stream renders them all in an
    unpredictable state.
    """

    def __new__(cls, iterable):
        """Instantiate new tuple from iterable containing three streams."""
        items = list(iterable)
        assert len(items) == 3, "iterable must be three items"  # noqa: S101

        return super(IOTriple, cls).__new__(cls, items)

    @property
    def stdin(self):
        """Return stdin stream."""
        return self[0]

    @property
    def stdout(self):
        """Return stdout stream."""
        return self[1]

    @property
    def stderr(self):
        """Return stderr stream."""
        return self[2]


class TextIOTriple(IOTriple):
    """Tuple context manager of stdin, stdout and stderr TextIOBase objects."""

    _ITEM_BASE = TextIOBase

    # pytest and colorama inject objects into sys.std* that are not real TextIOBase
    # and fail the assertion of this class

    def __new__(cls, iterable):
        """Instantiate new tuple from iterable containing three TextIOBase streams."""
        self = super(TextIOTriple, cls).__new__(cls, iterable)
        if not self.all_(lambda item: isinstance(item, cls._ITEM_BASE)):
            raise ValueError(
                "iterable must contain only {}".format(cls._ITEM_BASE.__name__)
            )
        return self


class FakeIOTriple(IOTriple):
    """Tuple context manager of stdin, stdout and stderr-like objects."""


class AutoIOTriple(IOTriple):
    """Tuple context manager which will create FakeIOTuple or TextIOTuple."""

    def __new__(cls, iterable):
        """Instantiate new TextIOTuple or FakeIOTuple from iterable."""
        items = list(iterable)
        if any(not isinstance(item, TextIOTriple._ITEM_BASE) for item in items):
            return FakeIOTriple(items)
        else:
            return TextIOTriple(items)
