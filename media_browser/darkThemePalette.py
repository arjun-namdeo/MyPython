#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
from PyQt5 import QtGui, QtCore


def getColor(r, g, b):
    c = QtGui.QColor()
    c.setRgbF(r, g, b)
    return c


def getGrayColor(value):
    return getColor(value, value, value)


class DarkThemePalette(QtGui.QPalette):
    """Dark palette for a Qt application meant to be used with the Fusion theme."""

    def __init__(self, *__args):
        super().__init__(*__args)

        color = getGrayColor(0.175)
        self.setColor(QtGui.QPalette.Window, color)
        self.setColor(QtGui.QPalette.Button, color)

        color = getGrayColor(0.70)
        self.setColor(QtGui.QPalette.Text, color)
        self.setColor(QtGui.QPalette.ButtonText, color)
        self.setColor(QtGui.QPalette.WindowText, color)
        self.setColor(QtGui.QPalette.BrightText, color)

        color = getColor(0.6, 0.6, 0.8)
        self.setColor(QtGui.QPalette.Link, color)


        self.setColor(QtGui.QPalette.Base,   getGrayColor(0.215))
        self.setColor(QtGui.QPalette.Shadow, getGrayColor(0.0))

        color = getGrayColor(0.26)
        self.setColor(QtGui.QPalette.AlternateBase,   color)
        self.setColor(QtGui.QPalette.Midlight,        color)

        self.setColor(QtGui.QPalette.Dark,  getGrayColor(0.13))
        self.setColor(QtGui.QPalette.Mid,   getGrayColor(0.21))
        self.setColor(QtGui.QPalette.Light, getGrayColor(0.40))

        self.setColor(QtGui.QPalette.Highlight, getColor(0.25, 0.29, 0.34))

        color = getGrayColor(0.46)
        self.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, color)
        self.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, color)
        self.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, color)

        self.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, getGrayColor(0.55))


def apply(application):
    application.setStyle("Fusion")
    application.setPalette(DarkThemePalette())
