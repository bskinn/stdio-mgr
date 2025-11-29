## CHANGELOG: stdio-mgr stdin/stdout/stderr mock/wrap context manager

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

### [Unreleased]

#### Internal

- Convert project build config (mostly) from `setup.py` to `pyproject.toml`
  ([#108]).
  - The dynamic README stays in `setup.py`.
- Convert CI to GitHub Actions and diversify ([#108]).
  - Ubuntu tests across Pythons on every PR.
  - Cross-platform tests across Pythons on PRs to `stable`.
  - Ensuring testability of sdist in PRs to `stable`.
    - Augment `MANIFEST.in` until tests run successfully on unpacked sdist.
  - Checking all tests ran in PRs to `stable`.
  - `[skip ci]` implemented in all.

- Refactor `__version__` to new `version.py` ([#108]).

- Set up `black`, `flake`, `isort` with `tox` envs and run/fix ([#108]).

- Update Python & deps versions in `tox` env matrix ([#108]).


### [1.0.1] - 2019-02-11

#### Changed

 * `TeeStdin` is now a `slots=False` attrs class, to avoid errors arising
   from some manner of change in the vicinity of attrs v18.1/v18.2.

### [1.0.0] - 2018-04-01

#### Features

 * `stdio_mgr` context manager with capability for mocking/wrapping all three
   of `stdin`/`stdout`/`stderr`
 * `stdin` mocking/wrapping is implemented with the custom `TeeStdin`, a
   subclass of `StringIO`, which tees all content read from itself into
   the mocked/wrapped `stdout`
 * `TeeStdin` is extended from `StringIO` by an `.append()` method,
   which adds content to the end of the stream without changing the
   current seek position.


[#108]: https://github.com/bskinn/stdio-mgr/pull/108
