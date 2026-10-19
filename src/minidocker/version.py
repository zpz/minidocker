from datetime import datetime, timezone


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


def _make_date_version(args):
    print(make_date_version())


def _make_datetime_version(args):
    print(make_datetime_version())


def register(subparsers):
    p_make_date_version = subparsers.add_parser("make-date-version", help="Construct a version string based on date")
    p_make_date_version.set_defaults(func=_make_date_version)

    p_make_datetime_version = subparsers.add_parser("make-datetime-version", help="Construct a version string based on date and time")
    p_make_datetime_version.set_defaults(func=_make_datetime_version)