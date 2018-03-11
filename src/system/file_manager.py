#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Common methods related to file/directory and system
"""
import os
import ctypes
import platform
import shutil
import traceback

__CSL = None


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
                # shutil.rmtree(destination)
                os.rmdir(destination)
            except Exception as e:
                traceback.print_exc()
                print "Error occured during the deletion of '{0}' as '{1}'".format(destination, e)
                return
        else:
            print "Desination files already exists. Cannot continue. Please use override or force arguments"
            return False

    print "Creating Links:\t\t {0} \t ==>> \t {1}".format(source, destination)
    if is_windows_machine():
        # windows have a completely different concept for sym-linking. I know, It's crazy
        return windows_symlink(source=source, link_name=destination)

    return os.symlink(source=source, link_name=destination)
