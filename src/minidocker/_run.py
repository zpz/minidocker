import getpass
import pathlib
import platform
import socket
from datetime import datetime, timezone

from ._util import run_command


def parse_args(args):
    imagename = None
    cmd = "bash"  # the command to be run within the container
    cmdargs = []  # args to `command`
    opts = []  # args to `docker run`

    # To restrict memory usage, do something like
    # --memory=8g
    # Default is unlimited.
    #
    # See https://georgeoffley.com/blog/shared-memory-in-docker.html

    # Parse arguments.
    # There are two sets of arguments: those before image-name, and those after.
    # For those before, some are parsed; the rest are forwarded to `docker run` as is.
    # For those after, the first is the command to be executed within the container;
    # the rest are arguments to the command.
    #
    # TODO: make use of `argparse` to simplify the following.
    while args:
        head = args.pop(0)
        if head == "-v":
            # volume mapping, e.g.
            #   -v /tmp/data:/home/docker-user/data
            opts.extend([head, args.pop(0)])
        elif head == "-p":
            # Port forwarding, e.g.
            #   -p 8080:8080
            opts.extend([head, args.pop(0)])
        elif head == "-e":
            # Set env var, e.g.
            #   -e MYNAME=abc
            val = args.pop(0)
            opts.extend([head, val])
        elif head.startswith("-"):
            # Every other argument is captured and passed on to `docker run`.
            # For example, if there is an option called `--volume` which sets
            # something called 'volume', you may specify it like this
            #
            #   --volume=30
            #
            # You can not do
            #
            #   --volume 30
            #
            # because `run-docker` does not explicitly capture this option,
            # hence it does not know this option has two parts.
            # The same idea applies to other options.
            opts.append(head)
        else:
            imagename = head
            if args:
                cmd = args[0]
                cmdargs = args[1:]
            break

    if not imagename:
        usage = """\
Usage:

python3 -m minidocker run [options] <image-name>[:tag] [<cmd> [cmd-args]]

where

`image-name` is either the a source repo name (optionally with appended ":dev") in `~/work/src/` or the full image name (with path and tag).

`cmd` is the command to be run within the container, followed by arguments to the command.
(Default: bash)
"""
        raise Exception("image name is missing.\n" + usage)

    return {
        "imagename": imagename,
        "cmd": cmd,
        "cmdargs": cmdargs,
        "opts": opts,
    }


def main(args):
    kwargs = parse_args(args)
    imagename = kwargs["imagename"]
    imageversion = None
    name = ""  # container's name
    IMAGENAME = None
    command = kwargs["cmd"]
    args = kwargs["cmdargs"]  # args to `command`
    opts = kwargs["opts"]  # args to `docker run`

    DOCKERHOMEDIR = "/home/docker-user"
    host_user = getpass.getuser()
    host_os = platform.system()
    host_ip = socket.gethostbyname(socket.gethostname())

    if imagename.endswith(":dev"):
        # 'dev' is a special tag used by local dev images.
        IMAGENAME = imagename
        imagename = IMAGENAME[:-4]  # remove the ':dev" tag
        imageversion = "dev"

        HOSTSRCDIR = pathlib.Path().resolve()

        DOCKERSRCDIR = f"{DOCKERHOMEDIR}/{HOSTSRCDIR.name}"
        if platform.system() == "Windows":
            # On Windows, convert the path to a form that Docker can understand.
            # See https://www.google.com/search?q=docker+run+volume+mapping+does+not+work+in+git-bash+terminal+on+windoes&oq=docker+run+volume+mapping+does+not+work+in+git-bash+terminal+on+windoes&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOTIHCAEQ6wcYQNIBCTIwMTAzajBqMagCALACAA&sourceid=chrome&ie=UTF-8

            d = HOSTSRCDIR.drive
            p = HOSTSRCDIR.as_posix().lstrip(d)
            hostsrcdir = f"//{d.rstrip(':').lower()}{p}"
        else:
            hostsrcdir = str(HOSTSRCDIR)
        opts.extend(
            [
                "-v",
                f"{hostsrcdir}/src:{DOCKERSRCDIR}/src",
                f"--workdir={DOCKERSRCDIR}",
            ]
        )
    else:
        # `imagename` is the full name.
        IMAGENAME = imagename

        imageversion = IMAGENAME[
            (IMAGENAME.index(":") + 1) :
        ]  # remove the longest substr from front
        imagename = IMAGENAME[
            : IMAGENAME.index(":")
        ]  # remove the shortest substr from back
        imagename = imagename[
            : imagename.rfind("/")
        ]  # remove namespace, keeping the last word only

    # `IMAGENAME` is the full name including url, namespace, etc.
    # ${IMAGENAME}=[namespace.../]${imagename}:${imageversion}
    # `$imagename` contains neither namespace nor tag.

    DATAVOLUME = "docker-data-volume"
    MOUNTPOINT = "{}/mnt".format(DOCKERHOMEDIR)
    opts.extend(["--mount", "source={},target={}".format(DATAVOLUME, MOUNTPOINT)])

    if not args and command in (
        "/bin/bash",
        "/bin/sh",
        "/usr/bin/bash",
        "/usr/bin/sh",
        "bash",
        "sh",
        "node",
        "npm",
        "python",
        "python3",
    ):
        opts.append("-it")

    if not any(v.startswith("--name=") for v in opts):
        # User did not specify a name for the container.
        name = "{}-{}-utc".format(
            host_user, datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        )
        opts.append("--name={}".format(name))

    if not any(v.startswith("--shm-size=") for v in opts):
        # User did not specify shared memory size.
        opts.append("--shm-size=2gb")

    if not any(v.startswith("--restart=") for v in opts) and "-d" not in opts:
        opts.append("--rm")
        # User did not specify '--restart=' or '-d'

    opts.extend(
        [
            "-e",
            "HOST_OS=" + host_os,
            "-e",
            "HOST_USER=" + host_user,
            "-e",
            "HOST_IP=" + host_ip,
            "-e",
            "IMAGE_NAME=" + imagename,
            "-e",
            "IMAGE_VERSION=" + imageversion,
            "-e",
            "TZ=America/Los_Angeles",
            "--init",
        ]
    )

    run_command(["docker", "run"] + opts + [IMAGENAME, command] + args)
