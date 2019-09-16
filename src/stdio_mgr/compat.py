r"""``stdio_mgr.compat`` *code module*.

``stdio_mgr.compat`` provides backports of Python standard library.

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
    The Python-2.0 License.

**Members**

"""
import abc

# AbstractContextManager was introduced in Python 3.6
# and may be used with typing.ContextManager.
# See https://github.com/jazzband/contextlib2/pull/21 for more complete backport
try:
    from contextlib import AbstractContextManager
except ImportError:  # pragma: no cover
    # Copied from _collections_abc
    def _check_methods(cls, *methods):
        mro = cls.__mro__
        for method in methods:
            for base in mro:
                if method in base.__dict__:
                    if base.__dict__[method] is None:
                        return NotImplemented
                    break
            else:
                return NotImplemented
        return True

    # Copied from contextlib
    class AbstractContextManager(abc.ABC):
        """An abstract base class for context managers."""

        def __enter__(self):
            """Return `self` upon entering the runtime context."""
            return self

        @abc.abstractmethod
        def __exit__(self, exc_type, exc_value, traceback):
            """Raise any exception triggered within the runtime context."""
            return None

        @classmethod
        def __subclasshook__(cls, subclass):
            """Check whether subclass is considered a subclass of this ABC."""
            if cls is AbstractContextManager:
                return _check_methods(subclass, "__enter__", "__exit__")
            return NotImplemented
