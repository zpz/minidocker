Usually, you set up the pre-commit Git hooks in the following steps:

1. In the Python project's root directory, create subdirectory `.githooks` with file `pre-commit`;
copy the content of this repo's [pre-commit](../../.githooks/pre-commit), or run that script directly:

::

    #!/usr/bin/env bash

    bash <(curl -s https://raw.githubusercontent.com/zpz/minidocker/main/.githooks/pre-commit) $@

2. In the root directory of the project, run the following commands:

::

    > git config core.hooksPath .githooks/
    > git update-index --add --chmod=+x .githooks/pre-commit


This lets `git` know this custom directory contains hooks.
(The default hooks directory is `.git/hooks`.)
This configures the hooks for the current repo. You need to do this for each new clone.

To verify this has been set successfully, use

::

    > git config --local core.hooksPath

The hooks need several Python packages. Make sure they are installed on the development machine by `pipx install`.
