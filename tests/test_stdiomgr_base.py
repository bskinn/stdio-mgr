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


def test_CaptureStdout():  # noqa: N802
    """Confirm stdout capture."""
    from stdio_mgr import stdio_mgr

    with stdio_mgr() as (i, o, e):
        s = "test str"
        print(s)

        # 'print' automatically adds a newline
        assert s + "\n" == o.getvalue()


def test_CaptureStderr():  # noqa: N802
    """Confirm stderr capture."""
    import warnings
    from stdio_mgr import stdio_mgr

    with stdio_mgr() as (i, o, e):
        w = "This is a warning"
        warnings.warn(w, stacklevel=2)

        # Warning text comes at the end of a line; newline gets added
        assert w + "\n" in e.getvalue()


def test_DefaultStdin():  # noqa: N802
    """Confirm stdin default-populate."""
    from stdio_mgr import stdio_mgr

    in_str = "This is a test string.\n"

    with stdio_mgr(in_str) as (i, o, e):
        assert in_str == i.getvalue()

        out_str = input()

        # TeeStdin tees the stream contents, *including* the newline,
        # to the managed stdout
        assert in_str == o.getvalue()

        # 'input' strips the trailing newline before returning
        assert in_str[:-1] == out_str


def test_ManagedStdin():  # noqa: N802
    """Confirm stdin populate within context."""
    from stdio_mgr import stdio_mgr

    str1 = "This is a test string."
    str2 = "This is another test string.\n"

    with stdio_mgr() as (i, o, e):
        # Preload str1 to stdout, and check. As above, 'print'
        # appends a newline
        print(str1)
        assert str1 + "\n" == o.getvalue()

        # Use custom method .append to add the contents
        # without moving the seek position; check stdin contents.
        # The newline remains, since the stream contents were not
        # run through 'input'
        i.append(str2)
        assert str2 == i.getvalue()

        # Pull the contents of stdin to variable
        out_str = input()

        # stdout should have both strings. The newline of str2 is
        # *retained* here, because str2 was teed from stdin upon
        # the read of stdin by the above 'input' call.
        assert str1 + "\n" + str2 == o.getvalue()

        # 'input' should just have put str2 to out_str, *without*
        # the trailing newline, per normal 'input' behavior.
        assert str2[:-1] == out_str
