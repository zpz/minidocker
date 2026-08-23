import tomllib as toml


def parse_pyproject():
    return toml.load(open("pyproject.toml", "rb"))
