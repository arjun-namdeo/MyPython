#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
General module with common functional procedures
"""
import os
from my_python import constants
from logIO import get_logger

logger = get_logger(__name__)


class PyProject(object):
    """
    A simple class for which contains attribute related to a specific project
    """
    def __init__(self, name, root_path):
        self.name = str(name)
        self.root_path = str(root_path)

    @property
    def is_source_package(self):
        return constants.PY_SOURCE_DIR in self.root_path

    @property
    def is_build_package(self):
        return constants.PY_BUILDS_DIR in self.root_path

    @property
    def is_testing_package(self):
        return constants.PY_TESTING_DIR in self.root_path

    def get_requirements_file(self):
        """
        Get the requirements file if any for the project, Returns None if nothing.

        :return             `str`           Requirements file path if found else None
        """
        req_file = os.path.join(self.root_path, constants.requirements_file)
        if os.path.isfile(req_file):
            return req_file
        logger.debug("Cannot find requirements file for '{0}' project.".format(self.name))
        return None

    def get_package_setup_file(self):
        """
        Get the package_setup file if any for the project, Returns None if nothing.

        :return             `str`           package_setup file path if found else None
        """
        setup_file = os.path.join(self.root_path, constants.package_setup_file)
        if os.path.isfile(setup_file):
            return setup_file
        logger.error("Cannot find package_setup file for '{0}' project.".format(self.name))
        return None

    def setup_project(self):
        """
        This method should basically read the package_setup and update the env_paths
        respectively.

        Also just a note, We need to make this compatible for cross platform uses i.e. for Windows/Linux/Mac
        """
        raise NotImplementedError("This have not been implemented yet. But I need to do it sometime later.")


def get_project_root_from_path(source_path):
    """
    Generic method to get the project root path from given path. The func can be really handy
    for all the projects as you can get the project root directory from a given path

    i.e.
        Lets assume you have a path where your files are there

        /local/scm_tools/src/
                            /scm_tools
                                /__init__.py
                                /common.py


        Now you'd want to know the root directory of project for many reason such as get the
        package_setup.py file, read the requirement.txt file etc.

        With this method you can pass any of following paths and It will return you the PyProject object which
        contains lots of useful attributes.

    :param source_path:         `str`                       AbsPath for the project
    :return:                    `PyProjectInstance`         PyProject Instance for given path of found else None
    """
    def _get_root_directory(src_path, path_checked=None):
        path_checked = list() if path_checked is None else path_checked
        if src_path is None or not os.path.exists(src_path):
            return None

        if src_path in path_checked:
            # It's repeating this path, If this path was root directory, The function would have returned the
            # path so no need to waste checking it again.
            return None

        if os.path.isfile(src_path):
            src_path = os.path.dirname(src_path)

        if constants.package_setup_file in os.listdir(src_path):
            return src_path

        path_checked.append(src_path)
        return _get_root_directory(src_path=os.path.dirname(src_path), path_checked=path_checked)

    root_path = _get_root_directory(src_path=source_path)
    if root_path is None:
        logger.warning("Given path is not a valid project.")
        return None

    root_name = os.path.basename(root_path)
    return PyProject(name=root_name, root_path=root_path)

