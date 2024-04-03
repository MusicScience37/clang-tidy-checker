Usage
======

Installation
------------------

Install from PyPI repository as follows:

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

Configuration files
-------------------------

This tool can be configured using configuration files written in YAML.

Configurations files are searched in the following order:

- Files given using the command line option ``-c``.
- File ``.clang-tidy-checker`` at the current directory.

Here shows an example of a configuration file with whole parameters.

.. code-block:: yaml
    :caption: An example of a configuration file.

    # ALl parameters are optional. Defaults to the values written below.

    # Name of clang-tidy executable to use.
    clang_tidy_executable: clang-tidy

    # Path of the build directory.
    build_dir: build

    # Flag to show progress.
    show_progress: true

    # Patters of checked files.
    # Write using glob patterns.
    file_patterns:
      - "**/*.c"
      - "**/*.cpp"
      - "**/*.cxx"
      - "**/*.cc"

    # Extra arguments to clang-tidy.
    extra_args: []

    # Directory in which caches of results are saved.
    # Value "null" disables caches.
    cache_dir: null

    # Maximum number of entries in the cache.
    # Ignored when "cache_dir" is null.
    max_cache_entries: 1000
