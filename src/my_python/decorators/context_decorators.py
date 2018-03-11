#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Common decorators and Context Managers
"""
import os
import datetime
from functools import wraps

from logIO import get_logger

logger = get_logger(__name__)


class ContextDecorator(object):
    """
    Abstract context manager + decorator
    """
    def __init__(self, **kwargs):
        self.label = "Unknown"
        self.__dict__.update(kwargs)

    def __enter__(self):
        # Running self means that in "with ... as x". x will be self
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def __call__(self, user_function):
        @wraps(user_function)
        def wrapper(*args, **kwargs):
            with self:
                return user_function(*args, **kwargs)
        return wrapper


class TimeIt(ContextDecorator):
    """
    time_it context manager

    Usage:  The reason I designed this in such a way so that we can sue this
            as decorator or context manager. For instance

            with TimeIt(label="running_something"):
                do_your_stuff()
            or

            @TimeIt(label="running_something")
            def do_your_stuff()
                pass
    """

    def __enter__(self):
        self.start_time = datetime.datetime.now()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        end_time = datetime.datetime.now()
        string = "INFO : Process '{0}' completed in {1} sec".format(self.label, end_time - self.start_time)
        logger.info(string)


class BusyCursor(ContextDecorator):
    """
    Busy Cursor Context manager

        Usage:  The reason I designed this in such a way so that we can sue this
                as decorator or context manager. For instance

                with BusyCursor():
                    do_your_stuff()
                or

                @BusyCursor()
                def do_your_stuff()
                    pass
    """
    def __enter__(self):
        from PyQt4 import QtWidgets, QtCore
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        from PyQt4 import QtWidgets
        QtWidgets.QApplication.restoreOverrideCursor()


class RunFromPath(ContextDecorator):
    """
    This will let you run code from a different path. This will change the path and run the given
    function and switch back the path to original path

    Usage:  The reason I designed this in such a way so that we can sue this
            as decorator or context manager. For instance

            with RunFromPath(path="/run/from/this/path"):
                do_your_stuff()
            or

            @RunFromPath(path="/run/from/this/path")
            def do_your_stuff()
                pass
    """
    def __enter__(self):
        self.init_work_directory = os.getcwd()
        self._path_changed = False
        if hasattr(self, 'path'):
            if self.path and os.path.exists(self.path) and self.path != os.getcwd():
                path = self.path if os.path.isdir(self.path) else os.path.dirname(self.path)
                os.chdir(path)
                self._path_changed = True
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._path_changed:
            os.chdir(self.init_work_directory)


class ClassPropertyDescriptor(object):
    """
    Python Class Property descriptor
    """
    def __init__(self, method_get, method_set=None):
        self.method_get = method_get
        self.method_set = method_set

    def __get__(self, obj, m_class=None):
        """
        Internal getter
        """
        if m_class is None:
            m_class = type(obj)
        return self.method_get.__get__(obj, m_class)()

    def __set__(self, obj, value):
        """
        Internal setter
        """
        if not self.method_set:
            raise AttributeError("Can't set attribute")
        type_ = type(obj)
        return self.method_set.__get__(obj, type_)(value)

    def setter(self, method):
        if not isinstance(method, (classmethod, staticmethod)):
            method = classmethod(method)
        self.method_set = method
        return self


def classproperty(func):
    """
    class property decorator for python use cases
    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)

