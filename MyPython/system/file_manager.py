#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Common methods related to file/directory and system
"""
import os
import ctypes
import platform
import platform
import shutil
import traceback

from logIO import get_logger

__CSL = None
logger = get_logger(__name__)


def windows_symlink(source, link_name):
    """
    symlink(source, link_name)
    Creates a symbolic link pointing to source named link_name

    To Run this properly, We need to setup the Permission for
    CreateSymbolicLink service. Please go to docs directory and
    see windows_symlinks.png

    """
    global __CSL

    if __CSL is None:
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        __CSL = csl
    flags = 0
    if source is not None and os.path.isdir(source):
        flags = 1

    if __CSL(link_name, source, flags) == 0:
        raise ctypes.WinError()


def read_csv(file_path, delimiter=',', quote_char='|'):
    """
    CSV File reader, This is a simple wrapper on top of python csv module which
    """
    if not validate_file_path(file_path=file_path):
        logger.warning("Invalid file-path given: '{0}'".format(file_path))
        return

    # we don't want to make this module too heavy with extra imports.
    # Better to import module when you need it.
    import csv

    with open(file_path, "r") as csv_read:
        reader = csv.reader(csv_read, delimiter=delimiter, quotechar=quote_char)
        for row in reader:
            yield row


def validate_file_path(file_path, file_extension=None, check_existence=False):
    """
    common method for validating a file_path

    @:param `file_path`         `str`   : Provide file path which you want to validate
    @:param `file_extension`    `str`   : Set this If you want to validate a specific file type. like .csv or .json
    @:param `check_existence`   `bool`  : Set this True/False if you want to check physical existence of file

    """
    if not file_path:
        logger.warning('No File Path received. Please provide correct filePath')
        return False

    if file_extension:
        if not str(file_path).endswith(str(file_extension)):
            logger.warning('Invalid File Type! Please provide a filePath with "{0}" file format.'.format(file_extension))
            return False

    if check_existence:
        if not os.path.isfile(file_path):
            logger.warning("File NOT Found. File %s does not found in location." % file_path)
            return False

    return True


def view_file(file_path=None):
    """
    Open up the file path in default browser.
    """
    if not validate_file_path(file_path=file_path, check_existence=True):
        return

    # we don't want to make this module too heavy with extra imports.
    # Better to import module when you need it.
    import webbrowser

    try:
        webbrowser.open("file://" + file_path)
    except Exception, e:
        logger.warning("Cannot start file because {0}.  File Path : {1}".format(e, file_path))


def is_windows_machine():
    """
    Check If a machine is Windows or not.

    The main reason for this method is to make sure that all of the code base is
    compatible with Windows/Linux/Mac. Linux & Mac works in very similar fashion
    but windows always creates problem. This method can be usefull in all the cases.
    """
    if str(platform.system()).lower() == "windows":
        return True
    return False


def copy_files(src_path, dst_path):
    dir_path = os.path.dirname(dst_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    shutil.copyfile(src_path, dst_path)


def create_symlinks(source, destination, override=False):
    """
    Generic method for creating symlinks for directories.

    :param source:              `str`               AbsPath for the source file/directory
    :param destination:         `str`               AbsPath for the destination file/directory
    :param override:            `bool`              Check if the desination is already exists,
                                                     if so, remove it and then create symlinks
    """
    if os.path.exists(destination):
        if override:
            # user has asked to override the previous files.
            try:
                os.rmdir(destination)
            except Exception as e:
                traceback.print_exc()
                logger.debug(traceback.format_exc())
                logger.error("Error occured during the deletion of '{0}' as '{1}'".format(destination, e))
                return
        else:
            logger.warning("Desination files already exists. Cannot continue. Please use override or force arguments")
            return False

    logger.info("Creating Links:\t\t {0} \t ==>> \t {1}".format(source, destination))
    if is_windows_machine():
        # windows have a completely different concept for sym-linking. I know, It's crazy
        return windows_symlink(source=source, link_name=destination)

    return os.symlink(source=source, link_name=destination)


def remove_file(file_path, force=True):
    """
    Remove single file, Use this method only for 1 file
    """
    if os.path.isfile(file_path):
        os.remove(file_path)


def remove_directory(directory_path, recursive=True, force=True):
    """
    Remove an entire directory
    """
    if not os.path.isdir(directory_path):
        return

    def _run_remove(method, _dir_path, method_name):
        try:
            method(_dir_path)
        except Exception, e:
            logger.debug(traceback.format_exc())
            logger.debug("Cannot delete '{0}' with {1} as ERROR: {2}".format(_dir_path, method_name, e))

        return bool(not os.path.isdir(directory_path))

    if not os.listdir(directory_path):
        success = _run_remove(method=os.rmdir, _dir_path=directory_path, method_name="os.rmdir")
        if success:
            return success

    success = _run_remove(method=shutil.rmtree, _dir_path=directory_path, method_name="shutil.rmtree")
    if success:
        return success

    if is_windows_machine():
        command = 'rd /s /q "{DIR}"'.format(DIR=directory_path)
    else:
        command = 'rm -rf "{DIR}"'.format(DIR=directory_path)

    os.system(command)
    return bool(not os.path.isdir(directory_path))


def remove_from_disk(path, recursive=True, force=True):
    if os.path.isdir(path):
        return remove_directory(directory_path=path, recursive=recursive, force=force)
    return remove_file(file_path=path, force=force)


if __name__ == "__main__":
    import logging
    logger.setLevel(logging.DEBUG)
    remove_directory(directory_path="C:\\temp\\my_python")