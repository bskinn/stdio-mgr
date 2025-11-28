import os, sys
from setuptools import setup, find_packages


sys.path.append(os.path.abspath("src"))
from stdio_mgr import __version__

sys.path.pop()


def readme():
    with open("README.rst", "r") as f:
        return f.read()


setup(
    name="stdio-mgr",
    version=__version__,
    packages=find_packages("src"),
    package_dir={"": "src"},
    provides=["stdio_mgr"],
    requires=["attrs (>=17.1)"],
    install_requires=["attrs>=17.1"],
    python_requires=">=3",
    url="https://www.github.com/bskinn/stdio-mgr",
    license="MIT License",
    author="Brian Skinn",
    author_email="bskinn@alum.mit.edu",
    description="Context manager for mocking/wrapping stdin/stdout/stderr",
    long_description=readme(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Development Status :: 5 - Production/Stable",
    ],
)


# ##### BREAK

import re
from pathlib import Path
from typing import Any, cast

from setuptools import setup

NAME = "stdio-mgr"

exec_ns: dict[str, Any] = {}
exec(Path("src", "sphobjinv", "version.py").read_text(encoding="utf-8"), exec_ns)
__version__ = cast(str, exec_ns["__version__"])

version_override: str | None = None


def readme():
    content = Path("README.md").read_text(encoding="utf-8")

    new_ver = version_override if version_override else __version__

    # Helper function
    def content_update(content, pattern, sub):
        return re.sub(pattern, sub, content, flags=re.M | re.I)

    # Docs reference updates to current release version, for PyPI
    # This one gets the badge image
    content = content_update(
        content, r"(?<=/readthedocs/{0}/)\S+?(?=\.svg$)".format(NAME), "v" + new_ver
    )

    # This one gets the RtD links
    content = content_update(
        content, r"(?<={0}\.readthedocs\.io/en/)\S+?(?=/)".format(NAME), "v" + new_ver
    )

    return content


setup(
    name=NAME,
    long_description=readme(),
    long_description_content_type="text/markdown",
)
