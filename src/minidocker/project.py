import warnings

from ._util import run_command_for_output


def get_git_branch():
    """
    This assumes the current working directory is the root directory of the repo.
    """
    return run_command_for_output(["git", "branch", "--show-current"])


def get_project_name():
    """Get the name of the git project, which is usually the name of the parent directory.

    In theory, the parent directory can be renamed to be
    different from the name of the `github` repo---the name of the `github` repo is
    recorded in `.git/config` and does not rely on the name of the local parent directory.
    For this reason, we infer the project name from the file `.git/config`.

    This could be different from the "project name" in `pyproject.toml`.
    """
    url = run_command_for_output(["git", "config", "--get", "remote.origin.url"])
    pkg = url.split("/")[-1][: -(len(".git"))]
    if "_" in pkg:
        warnings.warn(
            f"project name, '{pkg}', contains understore; it is recommended to use dash instead"
        )
    return pkg


def _get_project_name(args):
    print(get_project_name())


def _get_git_branch(args):
    print(get_git_branch())


def register(subparsers):
    p_get_project_name = subparsers.add_parser(
        "get-project-name", help="Get the name of the project"
    )
    p_get_project_name.set_defaults(func=_get_project_name)

    p_get_git_branch = subparsers.add_parser(
        "get-git-branch", help="Get the Git branch currently in"
    )
    p_get_git_branch.set_defaults(func=_get_git_branch)
