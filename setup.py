from setuptools import setup

from stdio_mgr import __version__


def readme():
    with open('README.rst', 'r') as f:
        return f.read()


setup(
    name='stdio-mgr',
    version=__version__,
    packages=['stdio_mgr'],
    provides=['stdio_mgr'],
    requires=['attrs (>=17.1)'],
    install_requires=['attrs>=17'],
    python_requires='>=3',
    url='https://www.github.com/bskinn/stdio-mgr',
    license='MIT License',
    author='Brian Skinn',
    author_email='bskinn@alum.mit.edu',
    description='Context manager for mocking/wrapping stdin/stdout/stderr',
    long_description=readme(),
    classifiers=['License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3 :: Only',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Software Development :: Testing',
                 'Development Status :: 4 - Beta'],
)
