import string
import argparse
from .._util import run_command
from ..project import get_project_name
from ._util import parse_pyproject


DOCKER_SRCDIR = "/tmp/src"
# Copy project repo to this location in the image.

PYPROJECT = parse_pyproject()
try:
    PKG = PYPROJECT["tool"]["flit"]["module"]["name"]
except KeyError:
    PKG = PYPROJECT["project"]["name"].lower().replace("-", "_")


def dev_dockerfile(*, parent, docker_srcdir):
    t = string.Template("""\
FROM ${PARENT}
USER root

ENV PARENT_IMAGE=${PARENT}

# If the repo needs non-Python dependencies, will need a mechanism
# to insert a block to install other things, or use user-defined Dockerfile.

# Install the package of the current repo along with all its required and optional
# dependencies. Then, uninstall the project package itself,
# leaving the dependencies in place. The source code is left in the image in order to run tests;
# otherwise it will be largely forgotten.
# Dev and test within the container will use volume-mapped live code.

COPY --chown=docker-user:docker-user . ${DOCKER_SRCDIR}

RUN pip-install ${DOCKER_SRCDIR}/[${EXTRAS}] \\
    && python -m pip uninstall -y ${NAME} \\
    && rm -rf ${DOCKER_SRCDIR}

USER docker-user
""")

    pyproj = PYPROJECT["project"]
    name = pyproj["name"]
    try:
        deps = pyproj["optional-dependencies"]
        extras = ",".join(deps.keys())
    except KeyError:
        extras = ""

    return t.substitute(
        PARENT=parent, DOCKER_SRCDIR=docker_srcdir, EXTRAS=extras, NAME=name
    )


def build_dev(*, parent, tag):
    dockerfile = dev_dockerfile(parent=parent, docker_srcdir=DOCKER_SRCDIR)
    run_command(
        ["docker", "build", "--no-cache", "-t", tag, "-f", "-", "."],
        input=dockerfile.encode(),
    )


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", required=True, help="full tag of parent image")
    args, more_args = parser.parse_known_args(args)

    return vars(args), more_args


def build(args, proj=None):
    kwargs, extra_args = parse_args(args)
    PROJ = proj or get_project_name()
    devimg = PROJ + ":dev"
    build_dev(parent=kwargs["parent"], tag=devimg)
