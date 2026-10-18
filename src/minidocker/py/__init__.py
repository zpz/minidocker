"""
Usually, the Python project is the central content of the Git repo; in that case,
commands provided by this module are issued in the root directory of the Git repo.
In special cases, the Python project is wholy contained in a subdirectory of a Git repo;
in that case, commands provided by this module are issued in the said subdirectory.
For the purpose of these commands, the root or the subdirectory are referred to as the
top directory of the project. (The top directory may be called "repo" even if it's not the root
of the Git repo.)

``minidocker py build`` builds a Docker image for Python code development.
This command handles two scenarios, namely, the repo develops a Python "package" or a Python "project".

In the case of a Python "package", it is assumed that (1) the package's dependencies are all specified in
``pyproject.toml``, and (2) there is no Dockerfile in the repo.

In the case of a Python "project", it is assumed that (1) the file ``pyproject.toml`` in the repo does not
specify **any** dependency; (2) there exists subdirectory ``docker`` under the root of the repo, and
the subdirectory contains ``Dockerfile`` as well as any dependencies needed for building the Docker image;
the process of building the Docker image does not make use of anything outside of the subdirectory ``docker``.
"""

import argparse
import sys


def _main(arg):
    parser = argparse.ArgumentParser(prog='minidocker py')
    parser.add_argument("subcommand")
    ns, rest = parser.parse_known_args(arg.extra)
    cmd = ns.subcommand
    if cmd == 'all-deps':
        from ._util import all_deps
        print('\n'.join(all_deps(*rest)))
    else:
        sys.exit("Unknown subcommand `%s`" % cmd)


def register(subparsers):
    p = subparsers.add_parser("py", add_help=False, help="Python project commands")
    p.set_defaults(func=_main)