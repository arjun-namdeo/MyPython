#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Custom Widgets
"""
import os
import re
import qdarkstyle
import logging
from functools import wraps

from PyQt5 import QtWidgets, QtCore, QtGui

logger = logging.getLogger(__name__)

MediaIconPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media.png")
SeriesMediaIconPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "folder.png")

SUBTITLES_EXT = (".sub", ".srt")
MEDIA_EXT = (".mp4", ".mkv", ".TS", ".avi")
INT_SIZE = 32
ICON_SIZE = QtCore.QSize(INT_SIZE, INT_SIZE)


class MediaQualityLookup(object):
    """
    Lookup table for media quality
    """
    ULTRA = 1080
    HIGH = 720
    MEDIUM = 480
    LOW = 240
    OFFLINE = 100

    ALL = [ULTRA, HIGH, MEDIUM, LOW, OFFLINE]

    @classmethod
    def convertRezToString(cls, res):
        """
        If you have the res as int, get the string rep for the same

        :param res:     `int`       Any from the MediaQualityLookup.ALL
        :return:        `str`       String repr for the size
        """
        if res == cls.ULTRA:
            return "Ultra"

        if res == cls.HIGH:
            return "High"

        if res == cls.MEDIUM:
            return "MEDIUM"

        if res == cls.LOW:
            return "LOW"

        if res == cls.OFFLINE:
            return "Offline"

        return "Unknown"


def cached_property(method):
    """
    A cached_property for caching the property data
    """
    @wraps(method)
    def get(self):
        try:
            return self._cache[method]
        except AttributeError:
            self._cache = {}
        except KeyError:
            pass
        result = self._cache[method] = method(self)
        return result
    return property(get)


def getMediaQuality(mediaFilePath):
    """
    Get the media file Quality

    :returns    `str`       One of MediaQualityLookup.ALL
    """
    if not mediaFilePath:
        return False

    if not os.path.isfile(mediaFilePath):
        return False

    info = os.stat(mediaFilePath)
    size = int(info.st_size) / 1000000.0

    if size > 2000:
        return MediaQualityLookup.ULTRA

    if size > 1000:
        return MediaQualityLookup.HIGH

    if size > 500:
        return MediaQualityLookup.MEDIUM

    if size < 100:
        return MediaQualityLookup.OFFLINE

    return MediaQualityLookup.LOW


class MovieMedia(object):
    """
    Movie media class
    """
    def __init__(self, path):
        if not os.path.exists(path):
            raise IOError("Invalid media path given : ", path)

        self.path = path
        self.name = os.path.basename(self.path)
        self.mediaPath = self.getMediaPath()

    def getMovieYear(self):
        if not self.mediaPath:
            return None

        year = re.search("\d+", self.name)
        if year:
            try:
                _grp = year.group(0)
                if int(_grp) > 1900:
                    return _grp
            except Exception as e:
                pass

        # find if the year exists in the movie name
        for eachYear in range(1900, 2100):
            if str(eachYear) in self.name:
                return eachYear

        return None

    def getMediaPath(self):
        if os.path.isfile(self.path):
            ext = os.path.splitext(self.path)[-1]
            if ext in MEDIA_EXT:
                return self.path
        else:
            for cFile in os.listdir(self.path):
                cPath = os.path.join(self.path, cFile)
                ext = os.path.splitext(cPath)[-1]
                if ext in MEDIA_EXT:
                    return os.path.join(self.path, cFile)

        return None

    @cached_property
    def isSubtitleAvailable(self):
        if not self.mediaPath:
            return False

        for ext in SUBTITLES_EXT:
            p, e = os.path.splitext(self.mediaPath)
            subTitleFile = p + ext
            if os.path.isfile(subTitleFile):
                return True
        return False

    @cached_property
    def mediaQuality(self):
        return getMediaQuality(mediaFilePath=self.mediaPath)


class MovieMediaTreeItem(QtWidgets.QTreeWidgetItem):
    """
    Custom tree widget item
    """
    def __init__(self, mediaObject, widget):
        super(MovieMediaTreeItem, self).__init__()
        self.mediaObject = mediaObject

        self.setText(0, self.mediaObject.name)
        self.setIcon(0, widget.mediaIcon)

        if self.mediaObject.mediaPath:
            self.setText(5, "Movie")
        else:
            self.setText(5, "Missing Media File")

        year = self.mediaObject.getMovieYear()
        if year:
            self.setText(1, str(year))

        if self.mediaObject.isSubtitleAvailable:
            self.setText(4, "Yes")
        else:
            self.setText(4, "No")

        self.setText(2, "{0}p".format(self.mediaObject.mediaQuality))

        if self.mediaObject.mediaQuality == MediaQualityLookup.OFFLINE:
            self.setText(3, "No")
        else:
            self.setText(3, "Yes")

        if widget.itemIsCheckable:
            self.setCheckState(0, QtCore.Qt.Unchecked)


class MovieSeriesTreeItem(QtWidgets.QTreeWidgetItem):
    """

    """
    def __init__(self, path, widget):
        super(MovieSeriesTreeItem, self).__init__()
        self.path = path
        self.widget = widget
        self.name = os.path.basename(path)

        self.setText(0, self.name)
        self.setIcon(0, self.widget.seriesIcon)


class AbstractMediaTreeView(QtWidgets.QWidget):
    """

    """
    HEADER_ITEMS = ["Name", "Year", "Quality", "Is Live", "Subtitle", "Media Type"]

    def __init__(self, inputPath=None, showMissingDirs=True, itemIsCheckable=True, parent=None):
        super(AbstractMediaTreeView, self).__init__(parent=parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setMinimumSize(1024, 800)

        self.searchFilter = QtWidgets.QLineEdit()
        self.layout().addWidget(self.searchFilter)

        self.searchFilter.setPlaceholderText("Enter here to filter movies")

        self.treeView = QtWidgets.QTreeWidget()
        self.layout().addWidget(self.treeView)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setSortingEnabled(True)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView.setIconSize(ICON_SIZE)
        self.treeView.setColumnWidth(0, 400)

        self.mediaIcon = QtGui.QIcon(MediaIconPath)
        self.seriesIcon = QtGui.QIcon(SeriesMediaIconPath)

        self.treeView.setHeaderLabels(self.HEADER_ITEMS)
        self.setWindowIcon(self.mediaIcon)
        self.setWindowTitle("Media File Manager")

        self.inputPath = inputPath
        self.showMissingDir = showMissingDirs
        self.itemIsCheckable = itemIsCheckable

        self.populateMedia(path=self.inputPath)

        self.searchFilter.textChanged.connect(self.filterMovies)

        self.treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def filterMovies(self):
        filterText = str(self.searchFilter.text()).lower()

        root = self.treeView.invisibleRootItem()
        childCount = root.childCount()

        for index in range(childCount):
            movieItem = root.child(index)
            isValid = False
            for columnIndex in range(movieItem.columnCount()):
                if filterText in str(movieItem.text(columnIndex)).lower():
                    isValid = True
                    break

            if isValid:
                movieItem.setHidden(False)
            else:
                movieItem.setHidden(True)

    def _validFolderName(self, folderName):
        folderName = str(folderName)

        if "desktop" in folderName.lower():
            return False

        if folderName.endswith(".db") or folderName.endswith(".ini"):
            return False

        # if folderName.startswith("_"):
        #     return False

        return True

    def populateMedia(self, path, parentItem=None):
        """
        Populate the treeView
        """
        if not os.path.exists(path):
            logger.warning("Input path is invalid : ", path)
            return

        parentItem = parentItem or self.treeView.invisibleRootItem()

        for child in os.listdir(path):

            if not self._validFolderName(folderName=child):
                continue

            childDirPath = os.path.join(path, child)
            videoFiles = [c for c in os.listdir(childDirPath) if c.lower().endswith(MEDIA_EXT)]

            if videoFiles:
                mediaObject = MovieMedia(path=childDirPath)
                if not mediaObject:
                    continue

                if not mediaObject.mediaPath and not self.showMissingDir:
                    print("Cannot find media path for : ", childDirPath)
                    continue

                item = MovieMediaTreeItem(mediaObject=mediaObject, widget=self)
                parentItem.addChild(item)

            else:
                seriesItem = MovieSeriesTreeItem(path=childDirPath, widget=self)
                parentItem.addChild(seriesItem)

                self.populateMedia(path=childDirPath, parentItem=seriesItem)

        if isinstance(parentItem, MovieMediaTreeItem):
            parentItem.setExpanded(True)



def run_application():
    import sys
    app = QtWidgets.QApplication.instance() or None
    need_app = bool(not app)
    if need_app:
        app = QtWidgets.QApplication(sys.argv)

    view = AbstractMediaTreeView(inputPath="D:/Entertainment/Movies")
    view.show()

    import darkThemePalette
    darkThemePalette.apply(app)

    if need_app:
        sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()

