#!/usr/bin/env python
# pylint: disable=import-error
"""A CLI tool for generating files from Jinja2 templates and environment
variables."""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)  # pylint: disable=duplicate-code
from os import environ
import sys
import argparse
import template.filters
import template.functions

# I ignore import errors here and fail on them later in the main function so
# the module can be imported by the setup.py with jinja missing so the
# docstring can be used as the package description.
try:  # nosemgrep: rules.bandit.B110
    from jinja2 import Environment
except ImportError:
    pass


__version__ = "0.7.6"


def render(template_string):
    """Render the template."""
    env = Environment(autoescape=True)
    # Add all functions in template.filters as Jinja filters.
    # pylint: disable=invalid-name
    for tf in filter(
        lambda x: callable(getattr(template.filters, x))
        and not x.startswith("_"),
        dir(template.filters),
    ):
        env.filters[tf] = getattr(template.filters, tf)
    functions = {
        x: getattr(template.functions, x)
        for x in dir(template.functions)
        if callable(getattr(template.functions, x)) and not x.startswith("_")
    }
    t = env.from_string(template_string, globals=functions)
    return t.render(environ)


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "filename",
        help="Input filename",
        type=argparse.FileType("r"),
        nargs="?",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output to filename",
        type=argparse.FileType("w"),
    )
    parser.add_argument(
        "-V",
        "--version",
        help="Template version",
        action="store_true",
    )
    args = parser.parse_args()
    if args.version:
        print("Template version {}.".format(__version__))
        sys.exit()
    infd = args.filename if args.filename else sys.stdin
    outfd = args.output if args.output else sys.stdout
    print(render(infd.read()), file=outfd)


if __name__ == "__main__":
    if "Environment" not in dir():
        print(
            "Failed to import jinja2, is the package installed?",
            file=sys.stderr,
        )
        sys.exit(2)
    main()
