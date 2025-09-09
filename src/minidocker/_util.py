import configparser
import subprocess
from datetime import datetime, timezone


def run_command(args, **kwargs):
    subprocess.run(args, check=True, **kwargs)


def run_command_for_output(args):
    return subprocess.run(
        args, check=True, capture_output=True, text=True
    ).stdout.rstrip("\n")


def make_date_version(sep="."):
    """Generate a version string in the format 25.08.12 in UTC date.

    Default separator is a period, making it look like a software version number.
    """
    return datetime.now(timezone.utc).strftime("%y{}%m{}%d".format(sep, sep))


def make_datetime_version(sep="-"):
    """Generate a version string in the format 20250812-120849 in UTC datetime.

    Default separator is a dash, making it look like a docker image tag.
    """
    return datetime.now(timezone.utc).strftime("%Y%m%d{}%H%M%S".format(sep))


def get_git_branch():
    return run_command_for_output(["git", "branch", "--show-current"])


def get_project_name():
    """Get the name of the git project, which is usually the name of the parent directory.

    In theory, the parent directory can be renamed to be
    different from the name of the `github` repo---the name of the `github` repo is
    recorded in `.git/config` and does not rely on the name of the local parent directory.
    For this reason, we infer the project name from the file `.git/config`.

    This could be different from the "project name" in `pyproject.toml`.
    """
    config = configparser.ConfigParser()
    config.read(".git/config")
    url = config['remote "origin"']["url"]
    pkg = url[url.index("/") :][1:][:-4]
    if "_" in pkg:
        raise ValueError(
            "project name, '{}', contains understore; please use dash instead".format(
                pkg
            )
        )
    return pkg
