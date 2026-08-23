"""
Usually, the Python project is the central content of the Git repo; in that case,
commands provided by this module are issued in the root directory of the Git repo.
In special cases, the Python project is wholy contained in a subdirectory of a Git repo;
in that case, commands provided by this module are issued in the said subdirectory.
For the purpose of these commands, the root or the subdirectory are referred to as the
top directory of the project. (The top directory may be called "repo" even if it's not the root
of the Git repo.)

``python3 -m minidocker.py build`` builds a Docker image for Python code development.
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


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand")
    parser.add_argument("--proj")
    arg, args = parser.parse_known_args(args)
    cmd = arg.subcommand
    proj = arg.proj
    if cmd == "build":
        from ._build import main as run_build

        run_build(args, proj=proj)
    elif cmd == "run":
        from ._run import main as run_run

        run_run(args)
    else:
        sys.exit("Unknown subcommand `%s`" % cmd)


if __name__ == "__main__":
    main(sys.argv[1:])
