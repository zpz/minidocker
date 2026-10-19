# This is an example Dockerfile for building the dev image for a Python package,
# which specifies its dependencies in `pyproject.toml`.
# This image installs dependencies of the package but not the package itself.
#
# Usually, you can retrieve the package's dependencies by
#
#   DEPS="$(minidocker py all-deps)"
#
# then pass in the values of `PARENT` and `DEPS` via `--build-args`.
#
# If you need more flexibilities, just write your own Dockerfile with ideas
# borrowed from here.

ARG PARENT
FROM ${PARENT}
USER root

ARG DEPS
RUN printf '%s\n' "$DEPS" | pip-install -r /dev/stdin

USER docker-user