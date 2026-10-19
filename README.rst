minidocker
==========

Docker tools for personal or small team deveopment, especially in Python.

Installation
------------

::

    pipx install .             # a regular install
    pipx install --editable .  # source edits take effect immediately, handy while you're developing it
    pipx ensurepath            # once, so ~/.local/bin is on PATH; restart the shell afterward

Usage
-----

The module ``minidocker`` provides generic commands unrelated to the programming language of the repo:

::

    $ minidocker <command> [options]

The submodule ``minidocker.py`` provides commands related to developing a Python project:

::

    $ minidocker py <command> [options]

For most uses, you should issue the command from the root of your project repo.