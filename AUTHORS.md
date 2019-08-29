Credits
=======

`stdio-mgr` is maintained by Brian Skinn ([Blog](https://bskinn.github.io)) ([Twitter](https://twitter.com/btskinn)).

Both the standard library (via the [`contextlib` module](https://docs.python.org/library/contextlib.html)) and `pytest` provide mechanisms for capturing/mocking `sys.stdout` and `sys.stderr`. However, neither provides functionality for mocking `sys.stdin`, and the usage of both can tend to be verbose. Thus, `stdio-mgr` was originally created with two main goals in mind:

1) Providing a mock for `sys.stdin`, in particular one with the capability to:
   a) Enable dynamic addition of text to the mocked input, and 
   b) 'Tee' the content read to `sys.stdout` (also mocked) in order to mimic what would be observed by a user at the console.
2) Implementing a concise, simultaneous mock for all of `sys.stdin`, `sys.stdout`, and `sys.stderr`

These goals were achieved in v1.x, authored by Brian Skinn, and enabled [direct testing of CLI logic involving user input](https://github.com/bskinn/sphobjinv/blob/8d46d61faa3d4735c4171f30e17ef593b402215e/tests/test_cli.py#L244-L257).

`stdio-mgr` v2, under active development as of 30 Aug 2019, aims to significantly expand the capabilities and correctness of the mocked stdio streams. [John Vandenberg](https://github.com/jayvdb) is leading these efforts.  See the [CHANGELOG](https://github.com/bskinn/stdio-mgr/blob/master/CHANGELOG.md) (eventually) for details of added features, changed behavior/API, etc.

