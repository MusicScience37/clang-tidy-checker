# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# pylint: disable=invalid-name,redefined-builtin,missing-module-docstring

import pathlib
import typing

import toml


# -- Project information -----------------------------------------------------

project = "clang_tidy_checker"
copyright = "2022, Kenta Kabashima"
author = "Kenta Kabashima"


def read_version() -> str:
    """Read version from pyproject.toml file."""

    this_dir = pathlib.Path(__file__).absolute().parent
    root_dir = this_dir.parent.parent
    pyproject_toml_path = root_dir / "pyproject.toml"
    config = toml.load(str(pyproject_toml_path))
    version = str(config["tool"]["poetry"]["version"])
    return version


# The full version, including alpha/beta/rc tags
release = read_version()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.todo"]

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: typing.List[str] = []


# Markdown
extensions += ["myst_parser"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
