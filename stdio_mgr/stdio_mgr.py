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
    [pending]

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

from contextlib import contextmanager
from io import StringIO, TextIOBase

import attr


@attr.s(slots=True)
class TeeStdin(StringIO):
    """Class to tee contents to a side buffer on read.

    Also provides .append(), which adds new content to the end of the
    stream while leaving the read position unchanged.

    """

    from io import SEEK_SET, SEEK_END

    tee = attr.ib(validator=attr.validators.instance_of(TextIOBase))
    init_text = attr.ib(default='',
                        validator=attr.validators.instance_of(str))

    def __attrs_post_init__(self):
        """Call normal __init__ on superclass."""
        super().__init__(self.init_text)

    def read(self, size=None):  # pragma: no cover
        """Tee text to side buffer when read."""
        text = super().read(size)
        self.tee.write(text)
        return text

    def readline(self, size=-1):
        """Tee text to side buffer when read."""
        text = super().readline(size)
        self.tee.write(text)
        return text

    def append(self, text):
        """Write to end of stream, restore position."""
        pos = self.tell()
        self.seek(0, self.SEEK_END)
        retval = self.write(text)
        self.seek(pos, self.SEEK_SET)
        return retval


@contextmanager
def stdio_mgr(cmd_str=''):
    """Prepare indicated sys for wrapped/mocked I/O."""
    import sys

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    new_stdout = StringIO()
    new_stderr = StringIO()
    new_stdin = TeeStdin(new_stdout, cmd_str)

    sys.stdin = new_stdin
    sys.stdout = new_stdout
    sys.stderr = new_stderr

    yield new_stdin, new_stdout, new_stderr

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    sys.stdout.write(new_stdout.read())
    sys.stderr.write(new_stderr.read())

    new_stdin.close()
    new_stdout.close()
    new_stderr.close()


if __name__ == '__main__':  # pragma: no cover
    print("Module not executable.")
