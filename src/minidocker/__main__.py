import argparse
import sys

from ._util import make_date_version, make_datetime_version
from ._find_image import find_image, find_local_image, find_remote_image


def _find_image(name):
    z = find_image(name)
    if z:
        print(z)


def _find_local_image(name):
    z = find_local_image(name)
    if z:
        print(z)


def _find_remote_image(name):
    z = find_remote_image(name)
    if z:
        print(z)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser")
    p_find_image = subparsers.add_parser("find-image")
    p_find_image.add_argument("image_name")
    p_find_local_image = subparsers.add_parser("find-local-image")
    p_find_local_image.add_argument("local_image_name")
    p_find_remote_image = subparsers.add_parser("find-remote-image")
    p_find_remote_image.add_argument("remote_image_name")
    p_make_date_version = subparsers.add_parser("make-date-version")
    p_make_date_version = subparsers.add_parser("make-datetime-version")
    args = parser.parse_args()

    cmd = args.subparser
    if cmd == "find-image":
        z = find_image(args.image_name)
        if z:
            print(z)
        else:
            sys.exit(1)
    elif cmd == "find-local-image":
        z = find_local_image(args.local_image_name)
        if z:
            print(z)
        else:
            sys.exit(1)
    elif cmd == "find-remote-image":
        z = find_remote_image(args.remote_image_name)
        if z:
            print(z)
        else:
            sys.exit(1)
    elif cmd == "make-date-version":
        print(make_date_version())
    elif cmd == "make-datetime-version":
        print(make_datetime_version())
    else:
        raise ValueError('unknown sub-command "%s"' % cmd)
