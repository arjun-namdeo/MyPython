#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
System related operational methods
"""
import os
import sys
import subprocess
from logIO import get_logger

from my_python.system.file_manager import validate_file_path

logger = get_logger(__name__)


def open_path_with_default_app(file_path):
    """
    Open the given file path with default app.

    :param file_path:           `str`
    """
    if not validate_file_path(file_path=file_path, check_existence=True):
        logger.warning("FileNotFound: '{0}'".format(file_path))
        return

    if sys.platform == "win32":
        os.startfile(file_path)
        return

    open_exe = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([open_exe, file_path])
    return

