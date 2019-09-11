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
import collections.abc
from contextlib import suppress
from io import TextIOBase

from stdio_mgr.compat import AbstractContextManager


class MultiItemTuple(collections.abc.Iterable):
    """Iterable with methods that operate on all items."""

    @staticmethod
    def _invoke_name(item, method_name):
        item = getattr(item, method_name)
        if callable(item):
            item = item()
        return item

    def _map_method(self, method_name):
        """Perform method on all items."""
        for item in self:
            item = self._invoke_name(item, method_name)
            yield item

    def _map(self, op):
        """Return generator for performing op on all items."""
        if isinstance(op, str):
            return self._map_method(op)

        return map(op, self)

    def suppress_map(self, ex, op):
        """Return generator for performing op on all item, suppressing ex."""
        for item in self:
            with suppress(ex):
                yield self._invoke_name(item, op) if isinstance(op, str) else op(item)

    def _all(self, op):
        """Perform op on all items, returning True when all were successful."""
        return all(self._map(op))

    def suppress_all(self, ex, op):
        """Perform op on all items, suppressing ex."""
        return all(self.suppress_map(ex, op))

    def _any(self, op):
        """Perform op on all items, returning True when all were successful."""
        return any(self._map(op))


class TupleContextManager(tuple, AbstractContextManager):
    """Base for context managers that are also a tuple."""

    # This is needed to establish a workable MRO.


class StdioTupleBase(TupleContextManager, MultiItemTuple):
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

        return super(StdioTupleBase, cls).__new__(cls, items)

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


class ClosingStdioTuple(StdioTupleBase):
    """Tuple context manager of stdin, stdout and stderr stream-like objects.

    Used as a context manager, it will close all of the streams on exit.
    however it does not open the streams on entering the context manager.

    No exception handling is performed while closing the streams, so any
    exception occurring the close of any stream renders them all in an
    unpredictable state.
    """

    def close(self):
        """Close all streams."""
        return list(self._map("close"))

    def safe_close(self):
        """Close all streams, ignoring any ValueError."""
        return list(self.suppress_map(ValueError, "close"))

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context, closing all members."""
        self.close()
        return super().__exit__(exc_type, exc_value, traceback)


class TextIOTuple(StdioTupleBase):
    """Tuple context manager of stdin, stdout and stderr TextIOBase objects."""

    _ITEM_BASE = TextIOBase

    # pytest and colorama inject objects into sys.std* that are not real TextIOBase
    # and fail the assertion of this class

    def __new__(cls, iterable):
        """Instantiate new tuple from iterable containing three TextIOBase streams."""
        self = super(TextIOTuple, cls).__new__(cls, iterable)
        if not self._all(lambda item: isinstance(item, cls._ITEM_BASE)):
            raise ValueError(
                "iterable must contain only {}".format(cls._ITEM_BASE.__name__)
            )
        return self


class FakeIOTuple(StdioTupleBase):
    """Tuple context manager of stdin, stdout and stderr-like objects."""


class AnyIOTuple(StdioTupleBase):
    """Tuple context manager which will create FakeIOTuple or TextIOTuple."""

    def __new__(cls, iterable):
        """Instantiate new TextIOTuple or FakeIOTuple from iterable."""
        items = list(iterable)
        if any(not isinstance(item, TextIOTuple._ITEM_BASE) for item in items):
            return FakeIOTuple(items)
        else:
            return TextIOTuple(items)
