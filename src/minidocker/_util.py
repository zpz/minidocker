import configparser
import subprocess
import sys
import warnings
from datetime import datetime, timezone

class CommandError(RuntimeError):
    def __init__(self, cmd, err, *args, **kwargs):
        super().__init__(cmd, err, *args, **kwargs)
        self.cmd = cmd
        self.err = err
        

def run_command(args, **kwargs):
    subprocess.run(args, check=True, **kwargs)


def run_command_for_output(args):
    try:
        result = subprocess.run(
            args, check=True, capture_output=True, text=True
        )
    except FileNotFoundError as e:
        print("\nError running command:  %s\nLikely the command is not installed or not in the PATH.\n" % " ".join(args), file=sys.stderr)
        raise e
    except subprocess.CalledProcessError as e:
        # print("\nError running command:  %s" % " ".join(args), file=sys.stderr)
        # print(e.stderr, file=sys.stderr)
        # raise e
        raise CommandError(" ".join(args), e.stderr) from None
    return result.stdout.rstrip("\n")


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
    """
    This assumes the current working directory is the root directory of the repo.
    """
    return run_command_for_output(["git", "branch", "--show-current"])


def get_project_name():
    """Get the name of the git project, which is usually the name of the parent directory.

    This assumes the current working directory is the root directory of the repo.

    In theory, the parent directory can be renamed to be
    different from the name of the `github` repo---the name of the `github` repo is
    recorded in `.git/config` and does not rely on the name of the local parent directory.
    For this reason, we infer the project name from the file `.git/config`.

    This could be different from the "project name" in `pyproject.toml`.
    """
    config = configparser.ConfigParser()
    config.read(".git/config")
    url = config['remote "origin"']["url"]
    pkg = url.split("/")[-1][:-(len(".git"))]
    if "_" in pkg:
        warnings.warn(
            "project name, '{}', contains understore; it is recommended to use dash instead".format(
                pkg
            )
        )
    return pkg
