#!/usr/bin/env python
"""Filters for the template CLI."""
# pylint: disable=import-error, import-outside-toplevel


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)  # pylint: disable=duplicate-code


def run(*argv, **kwargs):
    """
    Runs a command and returns the stdout, stderr and returncode
    using `run
    <https://docs.python.org/3.5/library/subprocess.html?highlight=popen#subprocess.run>`_.
    >>> run('ls')["returncode"] == 0
    True
    >>> 'SHELL' not in run('echo $SHELL', shell=True)['stdout']
    True
    >>> run(['ls', 'foo'])['returncode'] > 0
    True
    """
    import sys

    if sys.version_info[0] < 3:  # nosec
        import subprocess32 as subprocess
    else:
        import subprocess  # nosemgrep: rules.bandit.B40

    defaults = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
    defaults.update(kwargs)
    proc = subprocess.run(  # nosec, pylint: disable=subprocess-run-check
        *argv, **defaults
    ).__dict__
    if "text" not in kwargs or kwargs["text"]:
        proc["stdout"] = proc["stdout"].decode()
        proc["stderr"] = proc["stderr"].decode()
    return proc


def readfile(path):
    """
    Opens a file, returns the contents.

    >>> readfile("/dev/null")
    ''
    >>> foo = "foo"
    >>> with open("/tmp/foo", "w") as f:
    ...     _ = f.write(foo)
    >>> foo == readfile("/tmp/foo")
    True
    """

    with open(path, "r") as f:  # pylint: disable=invalid-name
        return f.read()
