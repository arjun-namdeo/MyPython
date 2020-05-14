#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module docs
"""
from PyQt5 import QtWidgets, QtCore, QtGui


class MyWindow(QtWidgets.QMainWindow):
    """

    """
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent=parent)
        self.setWindowTitle("Testing")


def run_application():
    import sys
    app = QtWidgets.QApplication.instance() or None
    need_app = bool(not app)
    if need_app:
        app = QtWidgets.QApplication(sys.argv)

    view = MyWindow()
    view.show()

    if need_app:
        sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()

