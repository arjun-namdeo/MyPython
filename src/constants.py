#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Constants for the package
"""
import os

# Make sure to have following variables set in your env before running any of my code
PIPE_SOURCE_DIR = os.getenv("PIPE_SOURCE", None)
PIPE_BUILDS_DIR = os.getenv("PIPE_BUILDS", None)
PIPE_TESTING_DIR = os.getenv("PIPE_TESTING", None)

if not all([PIPE_SOURCE_DIR, PIPE_BUILDS_DIR, PIPE_TESTING_DIR]):
    # Remember you need to have above 3 paths in your global env variable
    # if you want to access any of my codebase.
    raise IOError("PipeSource, PipeBuilds and PipeTesting paths needs to be defined at your system.!")

PY_SOURCE_DIR = os.path.join(PIPE_SOURCE_DIR, "python")
PY_BUILDS_DIR = os.path.join(PIPE_BUILDS_DIR, "python")
PY_TESTING_DIR = os.path.join(PIPE_TESTING_DIR, "python")

BIN_BUILDS_DIR = os.path.join(PIPE_BUILDS_DIR, "bin")
BIN_TESTING_DIR = os.path.join(PIPE_TESTING_DIR, "bin")

package_setup_file = "package_setup.py"
requirements_file = "requirements.yaml"


def _create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


map(_create_directory, [PY_BUILDS_DIR, PY_SOURCE_DIR, PY_TESTING_DIR, BIN_BUILDS_DIR, BIN_TESTING_DIR])
