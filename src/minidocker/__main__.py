import argparse
import sys

from . import image, project, py, version


def main():
    parser = argparse.ArgumentParser(prog="minidocker")
    subparsers = parser.add_subparsers(dest="subparser", metavar="<command>")

    image.register(subparsers)
    project.register(subparsers)
    version.register(subparsers)
    py.register(subparsers)

    arg, extra = parser.parse_known_args()
    arg.extra = extra

    if hasattr(arg, "func"):
        arg.func(arg)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
