from . import project


def register(subparsers):
    p = subparsers.add_parser("py", help="Python project commands")
    sub = p.add_subparsers(dest="py_cmd", required=True, metavar="<command>")
    project.register(sub)
