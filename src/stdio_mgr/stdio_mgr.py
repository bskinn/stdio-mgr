r"""``stdio_mgr`` *code module*.

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

import sys
from contextlib import ExitStack, suppress
from io import BufferedRandom, BufferedReader, BytesIO, TextIOBase, TextIOWrapper

# AbstractContextManager was introduced in Python 3.6
# and may be used with typing.ContextManager.
try:
    from contextlib import AbstractContextManager
except ImportError:  # pragma: no cover
    AbstractContextManager = object

import attr


class _PersistedBytesIO(BytesIO):
    """Class to persist the value after close.

    A copy of the bytes value is given to a callback prior to
    the :meth:`~io.IOBase.close`.
    """

    def __init__(self, closure_callback):
        """Store callback invoked before close."""
        self._callback = closure_callback

    def close(self):
        """Send buffer to callback and close."""
        self._callback(self.getvalue())
        super().close()


class RandomTextIO(TextIOWrapper):
    """Class to capture writes to a buffer even when detached.

    Subclass of :class:`~io.TextIOWrapper` that utilises an internal
    buffer defaulting to utf-8 encoding.

    As a subclass of :class:`~io.TextIOWrapper`, it is not thread-safe.

    All writes are immediately flushed to the buffer.

    This class provides :meth:`~RandomTextIO.getvalue` which emulates the
    behavior of :meth:`StringIO.getvalue() <io.StringIO.getvalue>`,
    decoding the buffer using the :attr:`~io.TextIOBase.encoding`.
    The value is available even if the stream is detached or closed.
    """

    def __init__(self):
        """Initialise buffer with utf-8 encoding."""
        self._stream = _PersistedBytesIO(self._set_closed_buf)
        self._buf = BufferedRandom(self._stream)
        super().__init__(self._buf, encoding="utf-8")

    def write(self, *args, **kwargs):
        """Flush after each write."""
        super().write(*args, **kwargs)
        self.flush()

    def _set_closed_buf(self, value):
        self._closed_buf = value

    def getvalue(self):
        """Obtain buffer of text sent to the stream."""
        if self._stream.closed:
            return self._closed_buf.decode(self.encoding)
        else:
            return self._stream.getvalue().decode(self.encoding)


@attr.s(slots=False)
class TeeStdin(TextIOWrapper):
    """Class to tee contents to a side buffer on read.

    Subclass of :class:`~io.TextIOWrapper` that overrides
    :meth:`~io.TextIOBase.read` and :meth:`~io.TextIOBase.readline`
    to tee all content *read* from the stream to `tee`. The
    canonical use-case is with :func:`stdio_mgr`,
    where `tee` is the mocked stream for `stdin`.

    To emphasize: teeing occurs on content *read*, **not write**.

    As a subclass of :class:`~io.TextIOWrapper`, it is not thread-safe.

    This class provides :meth:`~TeeStdin.getvalue` which emulates the
    behavior of :meth:`StringIO.getvalue() <io.StringIO.getvalue>`,
    decoding the buffer using the :attr:`~io.TextIOBase.encoding`.

    This class also provides the method
    :meth:`~TeeStdin.append`, which is not available
    for the base :class:`TextIOWrapper <io.TextIOBase>` type.
    This method adds new content to the end of the
    stream while leaving the read position unchanged.

    Instantiation takes two arguments:

    `tee`

        :class:`~io.TextIOBase` -- Text stream to receive
        content teed from :class:`TeeStdin` upon read

    `init_text`

        |str| *(optional)* --
        Text to use as the initial contents of the
        underlying :class:`~io.TextIOWrapper`. `init_text` is
        passed directly to the :class:~io.TextIOWrapper`
        instantiation call. Default is an empty |str|.

    `encoding`

        |str| *(optional)* --
        Encoding for the underlying :class:`~io.TextIOWrapper`.
        Default is "utf-8".
    """

    from io import SEEK_SET, SEEK_END

    tee = attr.ib(validator=attr.validators.instance_of(TextIOBase))
    init_text = attr.ib(default="", validator=attr.validators.instance_of(str))
    _encoding = attr.ib(default="utf-8", validator=attr.validators.instance_of(str))

    def __attrs_post_init__(self):
        """Call normal __init__ on superclass."""
        self._buf = BytesIO(self.init_text.encode(self._encoding))
        super().__init__(BufferedReader(self._buf), encoding=self._encoding)

    def read(self, size=None):  # pragma: no cover
        """Tee text to side buffer when read.

        Overrides :meth:`TextIOWrapper.read() <io.TextIOBase.read>`
        to implement the teeing.

        Parameters
        ----------
        size

            |int| or |None| *(optional)* --
            Number of characters to return; a negative or |None|
            value reads to EOF.

        """
        text = super().read(size)
        self.tee.write(text)
        return text

    def readline(self, size=-1):
        """Tee text to side buffer when read.

        Overrides :meth:`TextIOWrapper.readline() <io.TextIOBase.readline>`
        to implement the teeing.

        Parameters
        ----------
        size

            |int| *(optional)* --
            Number of characters to return; a negative value
            reads an entire line, regardless of length

        """
        text = super().readline(size)
        self.tee.write(text)
        return text

    def append(self, text):
        """Write to end of stream while maintaining seek position.

        Actually stores the current position; seeks to end;
        writes `text`; and seeks to prior position.

        Parameters
        ----------
        text

            |str| -- Text to append to the current stream contents.

        """
        pos = self.tell()
        self.seek(0, self.SEEK_END)
        retval = self._buf.write(text.encode(self.encoding))
        self.seek(pos, self.SEEK_SET)
        return retval

    def getvalue(self):
        """Obtain pending buffer of text for stdin."""
        if self.closed:  # Triggers a ValueError if detached
            self.read()  # Triggers a ValueError
        return self.buffer.peek().decode(self.encoding)


class _SafeCloseIOBase(TextIOBase):
    """Class to ignore ValueError when exiting the context.

    Subclass of :class:`~io.TextIOBase` that disregards ValueError, which can
    occur if the file has already been closed, when exiting the context.
    """

    def __exit__(self, exc_type, exc_value, traceback):
        """Suppress ValueError while exiting context.

        :exc:`ValueError` may occur when the underlying
        buffer is detached or the file was closed.
        """
        with suppress(ValueError):
            super().__exit__(exc_type, exc_value, traceback)


class SafeCloseRandomTextIO(_SafeCloseIOBase, RandomTextIO):
    """Class to capture writes to a buffer even when detached, and safely close.

    Subclass of :class:`~_SafeCloseIOBase` and :class:`~RandomTextIO`.
    """


class SafeCloseTeeStdin(_SafeCloseIOBase, TeeStdin):
    """Class to tee contents to a side buffer on read, and safely close.

    Subclass of :class:`~_SafeCloseIOBase` and :class:`~TeeStdin`.
    """


class _MultiCloseContextManager(tuple, AbstractContextManager):
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


class StdioManager(_MultiCloseContextManager):
    r"""Substitute temporary text buffers for `stdio` in a managed context.

    Context manager.

    Substitutes empty :class:`RandomTextIO`\ s for
    :obj:`sys.stdout` and :obj:`sys.stderr`,
    and a :class:`TeeStdin` for :obj:`sys.stdin` within the managed context.

    Upon exiting the context, the original stream objects are restored
    within :mod:`sys`, and the temporary streams are closed.

    Parameters
    ----------
    in_str

        |str| *(optional)* -- Initialization text for
        the :class:`TeeStdin` substitution for `stdin`.
        Default is an empty string.

    Yields
    ------
    in_

        :class:`TeeStdin` -- Temporary stream for `stdin`.

    out_

        :class:`RandomTextIO` -- Temporary stream for `stdout`,
        initially empty.

    err_

        :class:`RandomTextIO` -- Temporary stream for `stderr`,
        initially empty.

    """

    def __new__(cls, in_str="", close=True):
        """Instantiate new context manager that emulates namedtuple."""
        if close:
            out_cls = SafeCloseRandomTextIO
            in_cls = SafeCloseTeeStdin
        else:
            out_cls = RandomTextIO
            in_cls = TeeStdin

        stdout = out_cls()
        stderr = out_cls()
        stdin = in_cls(stdout, in_str)

        self = super(StdioManager, cls).__new__(cls, [stdin, stdout, stderr])

        self._close = close

        return self

    @property
    def stdin(self):
        """Return capturing stdin stream."""
        return self[0]

    @property
    def stdout(self):
        """Return capturing stdout stream."""
        return self[1]

    @property
    def stderr(self):
        """Return capturing stderr stream."""
        return self[2]

    def __enter__(self):
        """Enter context, replacing sys stdio objects with capturing streams."""
        self._prior_streams = (sys.stdin, sys.stdout, sys.stderr)

        super().__enter__()

        (sys.stdin, sys.stdout, sys.stderr) = self

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context, closing files and restoring state of sys module."""
        (sys.stdin, sys.stdout, sys.stderr) = self._prior_streams

        if self._close:
            super().__exit__(exc_type, exc_value, traceback)


stdio_mgr = StdioManager
