r"""``stdio_mgr`` *code module*.

``stdio_mgr`` provides a context manager for convenient
mocking and/or wrapping of ``stdin``/``stdout``/``stderr``
interactions.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    24 Mar 2018

**Copyright**
    \(c) Brian Skinn 2018

**Source Repository**
    http://www.github.com/bskinn/stdio-mgr

**Documentation**
    See README.rst at the GitHub repository

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

from contextlib import contextmanager
from io import StringIO, TextIOBase

import attr


@attr.s(slots=False)
class TeeStdin(StringIO):
    """Class to tee contents to a side buffer on read.

    Subclass of :cls:`~io.StringIO` that overrides
    :meth:`~io.StringIO.read` and :meth:`~io.StringIO.readline`
    to tee all content *read* from the stream to `tee`. The
    canonical use-case is with :func:`stdio_mgr`,
    where `tee` is the mocked stream for `stdin`.

    To emphasize: teeing occurs on content *read*, **not write**.

    This class also provides the method
    :meth:`TeeStdin..append`, which is not available
    for the base :cls:`~io.StringIO` type.
    This method adds new content to the end of the
    stream while leaving the read position unchanged.

    Instantiation takes two arguments:

    `tee`

        :cls:`~io.TextIOBase` -- Text stream to receive
        content teed from :cls:`TeeStdin` upon read

    `init_text`

        |str| *(optional)* --
        Text to use as the initial contents of the
        underlying :cls:`~io.StringIO`. `init_text` is
        passed directly to the :cls:~io.StringIO`
        instantiation call. Default is an empty |str|.

    """

    from io import SEEK_SET, SEEK_END

    tee = attr.ib(validator=attr.validators.instance_of(TextIOBase))
    init_text = attr.ib(default='',
                        validator=attr.validators.instance_of(str))

    def __attrs_post_init__(self):
        """Call normal __init__ on superclass."""
        super().__init__(self.init_text)

    def read(self, size=None):  # pragma: no cover
        """Tee text to side buffer when read.

        Overrides :meth:`io.StringIO.read <StringIO.read>`
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

        Overrides :meth:`io.StringIO.readline <StringIO.readline>`
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
        retval = self.write(text)
        self.seek(pos, self.SEEK_SET)
        return retval


@contextmanager
def stdio_mgr(in_str=''):
    r"""Subsitute temporary text buffers for `stdio` in a managed context.

    Context manager.

    Substitutes empty :cls:`~io.StringIO`\ s for
    :cls:`sys.stdout` and :cls:`sys.stderr`,
    and a :cls:`TeeStdin` for :cls:`sys.stdin` within the managed context.

    Upon exiting the context, the original stream objects are restored
    within :mod:`sys`, and the temporary streams are closed.

    Parameters
    ----------
    in_str

        |str| *(optional)* -- Initialization text for
        the :cls:`TeeStdin` substitution for `stdin`.
        Default is an empty string.

    Yields
    ------
    in_

        :cls:`TeeStdin` -- Temporary stream for `stdin`.

    out_

        :cls:`~io.StringIO` -- Temporary stream for `stdout`,
        initially empty.

    err_

        :cls:`~io.StringIO` -- Temporary stream for `stderr`,
        initially empty.

    """
    import sys

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    new_stdout = StringIO()
    new_stderr = StringIO()
    new_stdin = TeeStdin(new_stdout, in_str)

    sys.stdin = new_stdin
    sys.stdout = new_stdout
    sys.stderr = new_stderr

    yield new_stdin, new_stdout, new_stderr

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    new_stdin.close()
    new_stdout.close()
    new_stderr.close()


if __name__ == '__main__':  # pragma: no cover
    print("Module not executable.")
