import argparse
import sys


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand")
    subcommand, args = parser.parse_known_args(args)
    cmd = subcommand.subcommand
    if cmd == "build":
        from ._build import main

        main(args)
    elif cmd == "run":
        from ._run import main

        main(args)
    else:
        sys.exit("Unknown subcommand `%s`" % cmd)


if __name__ == "__main__":
    main(sys.argv[1:])
