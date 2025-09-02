import configparser
from datetime import datetime, timezone
from pathlib import Path


def make_date_version(sep='.'):
    """Generate a version string in the format 25.08.12 in UTC date.
    
    Default separator is a period, making it look like a software version number.
    """
    return datetime.now(timezone.utc).strftime('%y{}%m{}%d'.format(sep, sep))


def make_datetime_version(sep='-'):
    """Generate a version string in the format 20250812-120849 in UTC datetime.
    
    Default separator is a dash, making it look like a docker image tag.
    """
    return datetime.now(timezone.utc).strftime('%Y%m%d{}%H%M%S'.format(sep))


def get_project_name():
    """Get the name of the project, which is usually the name of the parent directory.

    In theory, the parent directory can be renamed to be
    different from the name of the `github` repo---the name of the `github` repo is
    recorded in `.git/config` and does not rely on the name of the local parent directory.
    For this reason, we infer the project name from the file `.git/config`.
    """
    config = configparser.ConfigParser()
    config.read('.git/config')
    url = config['remote "origin"']['url']
    pkg = url[url.index('/'): ][1: ][:-4]
    if '_' in pkg:
        raise ValueError("project name, '{}', contains understore; please use dash instead".format(pkg))
    return pkg


def get_package_name():
    """
    Infer the package name.
    This is the name of the package code directory under `src/`, also the "import" name.
    This does not need to be the "project" name defined in `pyproject.toml`, which is for `pypi` and `pip`,
    related to install/uninstall.

    Here, we only consider one scenrio, that is, the package name contains dash,
    and the dash is replaced by underscore in the import name of the package. Specifically,
    the import name of the package is the name of the sole child directory of `src/`.
    """
    subs = [p for p in Path('src/').iterdir() if p.is_dir()]
    assert len(subs) == 1
    return subs[0]
    