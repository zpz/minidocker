from ._util import run_command_for_output, CommandError


def find_local_image(name):
    if ":" in name:
        if run_command_for_output(["docker", "images", "-q", name]):
            # Exists locally.
            return name

    tags = run_command_for_output(
        ["docker", "image", "ls", name, "--format", '"{{.Tag}}"']
    )
    if not tags:
        return None

    tags = [v.strip('"') for v in tags.split("\n")]
    if "latest" in tags:
        return name + ":latest"

    # Assume tags are sortable (such as named based on datetime); take the latest.
    return name + ":" + max(tags)


def find_remote_image(name):
    if "/" not in name:
        name = "library/" + name
    NAME = name
    if ":" in NAME:
        tag = NAME.split(":")[-1]
        name = NAME[: -len(":" + tag)]
        url = "https://hub.docker.com/v2/repositories/{}/tags/{}/".format(name, tag)

        try:
            if run_command_for_output(["curl", "--silent", "-f", "--head", "-lL", url]):
                # Exists remotely.
                return NAME
        except CommandError as e:
            if not e.err:
                return None
            raise

    url = "https://hub.docker.com/v2/repositories/{}/tags/".format(NAME)
    try:
        tags = run_command_for_output(["curl", "--silent", "-f", "-lL", url])
    except CommandError as e:
        if not e.err:
            return None
        raise

    tags = (
        tags.replace("{", "")
        .replace("}", "")
        .replace("[", "")
        .replace("]", "")
        .split(",")
    )
    tags = [v for v in tags if '"name"' in v]
    if tags:
        tags = [v.replace('"', "").lstrip("name:") for v in tags]
        return NAME + ":" + max(tags)

    return None


def find_image(name):
    """
    Find the latest tag of an image, either locally or remotely,
    assuming tags are sortable. The recommended tag naming scheme is based on datetime with fixed length,
    e.g. "2024-06-01" or "2024-06-01T12-00-00".

    The sole input is the name (i.e. repository) of the image, with namespace (i.e. owner) as needed,
    e.g.

        debian
        zppz/py3

    A local image does not have to have namespace, whereas a remote image must have namespace.
    Namespace of "official" images on Docker Hub is "library", e.g. "library/debian"; however,
    the namespace "library" is not shown in the image name when pulled locally, e.g.
    the Debian official image is named "debian" on local and "library/debian" on remote.
    This can lead to confusion. For an input without namespace, this function searches locally as is
    (that is, without adding any "default" namespace), and searches remotely by adding "library/" as the default namespace.

    If the image exists both locally and remotely with different latest tags, the local or remote one with the latest tag is returned.

    If the same latest tag exists both locally and remotely, the local tag is returned.

    If the image exists only locally or remotely, the latest local or remote tag is returned.

    If the name includes a tag, e.g. "debian:latest", then it is checked for existence locally and remotely, and returned if found.

    If the named image does not exist locally nor remotely, `None` is returned.
    """

    tag_local = find_local_image(name)
    tag_remote = find_remote_image(name)
    if tag_local:
        if tag_remote and tag_remote > tag_local:
            return tag_remote
        return tag_local
    elif tag_remote:
        return tag_remote
    else:
        return None
