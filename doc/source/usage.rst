Usage
======

Installation
------------------

Install from PyPI repository.

.. code-block:: bash

    pip install clang-tidy-checker

Command
------------

Invoke ``clang-tidy-checker`` command with options you want.

Command usage can be seen with option ``--help`` as follows:

.. code-block:: console

    $ clang-tidy-checker --help
    Usage: clang-tidy-checker [OPTIONS]

      Check files using clang-tidy.

    Options:
      -c, --config TEXT     Configuration file path.
      -b, --build_dir TEXT  Build directory.
      -p, --pattern TEXT    Checked file pattern.
      --extra_arg TEXT      Extra argument to clang-tidy command.
      --cache_dir TEXT      Cache directory.
      --no-ascii            Prevent writing ASCII escape sequences.
      --help                Show this message and exit.

.. todo:: More comprehensive documentation.
