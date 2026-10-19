import tomllib as toml


def all_deps(path=None):
    with open(path or "pyproject.toml", "rb") as f:
        data = toml.load(f)

    project = data.get("project", {})
    deps = []

    # 2. Grab the standard core dependencies
    deps.extend(project.get("dependencies", []))

    # 3. Grab all lists inside the optional-dependencies dictionary
    optional_dict = project.get("optional-dependencies", {})
    for group_deps in optional_dict.values():
        deps.extend(group_deps)

    return deps


def _all_deps(args):
    deps = all_deps(args.path)
    print("\n".join(deps))


def register(subparsers):
    p_all_deps = subparsers.add_parser(
        "all-deps", help="Retrieve all dependencies from the package's pyproject.toml"
    )
    p_all_deps.add_argument("path", nargs="?")
    p_all_deps.set_defaults(func=_all_deps)
