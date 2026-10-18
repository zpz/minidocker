import sys
import tomllib as toml


def parse_pyproject(path: str = None):
    return toml.load(open(path or "pyproject.toml", "rb"))


def all_deps(path=None):
    data = parse_pyproject(path)

    project = data.get("project", {})
    deps = []

    # 2. Grab the standard core dependencies
    deps.extend(project.get("dependencies", []))

    # 3. Grab all lists inside the optional-dependencies dictionary
    optional_dict = project.get("optional-dependencies", {})
    for group_deps in optional_dict.values():
        deps.extend(group_deps)

    return deps
