r"""``stdio_mgr.types`` *code module*.

``stdio_mgr.types`` provides misc. types and classes.

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
from contextlib import ExitStack, suppress

try:
    from contextlib import AbstractContextManager
except ImportError:  # pragma: no cover
    from stdio_mgr.compat import AbstractContextManager


class MultiItemIterable(collections.abc.Iterable):
    """Iterable with methods that operate on all items."""

    @staticmethod
    def _invoke_name(item, name):
        item = getattr(item, name)
        if callable(item):
            return item()
        return item

    def _map_name(self, name):
        """Perform attribute name on all items."""
        for item in self:
            item = self._invoke_name(item, name)
            yield item

    def map_(self, op):
        """Return generator for performing op on all items."""
        if isinstance(op, str):
            return self._map_name(op)

        return map(op, self)

    def suppress_map(self, ex, op):
        """Return generator for performing op on all item, suppressing ex."""
        for item in self:
            with suppress(ex):
                yield self._invoke_name(item, op) if isinstance(op, str) else op(item)

    def all_(self, op):
        """Perform op on all items, returning True when all were successful."""
        return all(self.map_(op))

    def suppress_all(self, ex, op):
        """Perform op on all items, suppressing ex."""
        return all(self.suppress_map(ex, op))

    def any_(self, op):
        """Perform op on all items, returning True when all were successful."""
        return any(self.map_(op))


class TupleContextManager(tuple, AbstractContextManager):
    """Base for context managers that are also a tuple."""

    # This is needed to establish a workable MRO.


class ClosingStdioTuple(TupleContextManager, MultiItemIterable):
    """Context manager of streams objects to close them on exit.

    Used as a context manager, it will close all of the streams on exit.
    however it does not open the streams on entering the context manager.

    No exception handling is performed while closing the streams, so any
    exception occurring the close of any stream renders them all in an
    unpredictable state.
    """

    def close(self):
        """Close all streams."""
        return list(self.map_("close"))

    def safe_close(self):
        """Close all streams, ignoring any ValueError."""
        return list(self.suppress_map(ValueError, "close"))

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context, closing all members."""
        self.close()
        return super().__exit__(exc_type, exc_value, traceback)


class MultiCloseContextManager(TupleContextManager):
    """Manage multiple closable members of a tuple."""

    def __enter__(self):
        """Enter context of all members."""
        with ExitStack() as stack:
            all(map(stack.enter_context, self))

            self._close_files = stack.pop_all().close

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context, closing all members."""
        self._close_files()
