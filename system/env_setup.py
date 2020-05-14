#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Methods related to the env setup in host machines
"""
import os


def append_path(variable, path):
    """
    Add the given path to the system variable

    :param variable:            `str`
    :param path:                `str`
    """
    existing_paths = os.getenv(str(variable))
    if not existing_paths:
        # nothing in the system path just set it to given path
        os.environ[variable] = "{0}{1}".format(path, os.pathsep)
        return

    if path in existing_paths:
        # path is already in the system path
        return

    if existing_paths.endswith(os.pathsep):
        path_2_add = "{0}{1}".format(path, os.pathsep)
    else:
        path_2_add = "{0}{1}{2}".format(os.pathsep, path, os.pathsep)

    os.environ[variable] = "{0}{1}".format(existing_paths, path_2_add)
    return
