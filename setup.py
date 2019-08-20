import os.path as osp
from setuptools import setup, find_packages


with open(osp.join("src", "stdio_mgr", "version.py")) as f:
    exec(f.read())


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
    python_requires=">=3.4",
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
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Development Status :: 5 - Production/Stable",
    ],
)
