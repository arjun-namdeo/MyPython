#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data Model Assets for the package
"""
import re
import os
import json
import requests

CACHE_FILE = "mediaInfo.db"
DB_Schema = "1.0"


def scan_movies(root_path):
    """
    for each_dir in all_directory/subdirectory:
        if CACHE_FILE in each_dir:
            print CACHE_FILE

        if ["mp4, wmv, mov"] file in each_dir:
            it's movie directory with no info.
            fetch_online info and create CACHE_FILE
            print CACHE_FILE
    """
    valid_file_types = (".mp4", ".mov", ".wmv", ".avi", CACHE_FILE)
    for dirName, subDirList, fileList in os.walk(root_path):
        mediaFiles = [f for f in fileList if f.endswith(valid_file_types)]
        if not mediaFiles:
            # print("This is probably just an empty directory")
            continue

        if CACHE_FILE in mediaFiles:
            # this already has a CACHE_FILE
            continue

        # now this is probably a movie directory, so before we create a PyObject for Media
        # we need to find as much info as we can such as name, year, category, bollywood/hollywood and all
        kw_args = dict()
        kw_args["name"] = os.path.basename(dirName)
        kw_args["path"] = dirName
        kw_args["languages"] = list()
        kw_args["tags"] = list()

        if "bollywood" in dirName.lower():
            kw_args["tags"].append("Bollywood")
            kw_args["languages"].append("Hindi")
        else:
            kw_args["languages"].append("English")

        if "hindi" in dirName.lower() or "dual" in dirName.lower():
            if "Hindi" not in kw_args.get("languages"):
                kw_args["languages"].append("Hindi")

        mediaClass = GenericMovieMedia(**kw_args)
        mediaClass.build_information(write_db=False)


def is_website_accessible(web_url):
    try:
        requests.get(web_url, timeout=1)
        return True
    except Exception as e:
        print("Cannog access {0}, please check your internet connection".format(web_url))
        return False


def get_db_file(path):
    """
    Get the db file from given path

    :param: path        `str`       directory path where we need to find db file
    """
    if not os.path.exists(path):
        return False

    file_path = os.path.join(path, CACHE_FILE)
    if not os.path.isfile(file_path):
        return False

    return file_path


class MediaDB(object):
    """
    PyObject to handle the CacheConfFile
    """

    def __init__(self, **kwargs):
        self.schema = DB_Schema
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_db_file(cls, path):
        if path.endswith(CACHE_FILE):
            file_path = path
        else:
            file_path = get_db_file(path=path)

        if not file_path:
            raise IOError("Cannot find db file to read from")

        try:
            with open(file_path, "r") as read_db:
                data = json.load(read_db)

            return cls(**data)

        except Exception as e:
            raise IOError(e)

    def to_db_file(self, dir_path=None):
        dir_path = dir_path or getattr(self, "path", None)
        file_path = get_db_file(path=dir_path)
        if not file_path:
            raise IOError("Cannod find file path to export data")

        data = vars(self)
        try:
            with open(file_path, "w") as write_db:
                json.dump(write_db, data, indent=4)

            return True

        except Exception as e:
            raise IOError(e)


class AbstractMediaClass(object):
    """
    generic abstract media class
    """
    MediaType = "AbstractMedia"

    def __init__(self, name, path, year=None, languages=None, category=None, tags=None, hiddenTags=None, image=None):
        self.attr_name = name
        self.attr_path = path
        self.attr_year = year
        self.attr_languages = languages or list()
        self.attr_category = category or list()
        self.attr_tags = tags or list()
        self.attr_hiddenTags = hiddenTags or list()
        self.attr_image = image

        print (self.get_all_attributes())

    @property
    def attr_mediaType(self):
        return self.MediaType

    @property
    def cache_file(self):
        return get_db_file(path=self.get_path())

    def get_all_attributes(self):
        return {k: self.get_value(k) for k in dir(self) if str(k).startswith("attr_")}

    def get_value(self, attribute):
        if "attr_" in attribute:
            return getattr(self, attribute, None)
        return getattr(self, "attr_{0}".format(attribute), None)

    def get_name(self):
        return self.get_value("name")

    def get_path(self):
        return self.get_value("path")

    def get_year(self):
        return self.get_value("year")

    def get_tags(self):
        return self.get_value("tags")

    def get_hiddenTags(self):
        return self.get_value("hiddenTags")

    def get_image(self):
        return self.get_value("image")

    def write_cache(self):
        kw_args = dict()

        for key, value in self.get_all_attributes():
            key = key.replace("attr_", "")
            kw_args[key] = value

        db = MediaDB(**kw_args)
        db.to_db_file(dir_path=self.get_path())
        return True

    def read_cache(self):
        if not self.isCacheAvailable():
            print("Cache data not available.")
            return None
        return self.__cache_media_data

    def __cache_media_data(self):
        return MediaDB.from_db_file(path=self.cache_file)

    def build_information(self, write_db=True):
        """
        This should basically add the information for the current
        media class

        If Internet conenction and onlineResource is available
            try and fetch the information about the current media
            save the data into the class attributes
            do a media.write_cache() so that those information

        else:
            first check if there's any cached info saved out previously
            if not then put local logic and add as much info as you can
            do a media.write_cache() so that those information
        """
        if self.isInternetConnectionAvailable() and self.isOnlineResourceAvailable():
            


    def isCacheAvailable(self):
        if not os.path.isfile(self.cache_file):
            return False
        try:
            if self.__cache_media_data:
                return True
            return False
        except:
            return False

    def isInternetConnectionAvailable(self):
        for webURL in [self.online_resource, "https://www.google.com", "https://www.bing.com", "https://www.yahoo.com"]:
            if is_website_accessible(web_url=webURL):
                return True
        return False

    def isOnlineResourceAvailable(self):
        if not self.isInternetConnectionAvailable():
            return False
        return is_website_accessible(web_url=self.online_resource)

    @property
    def online_resource(self):
        return "http://www.omdbapi.com"


class GenericMovieMedia(AbstractMediaClass):
    """
    Class for Generic Movie
    """
    MediaTYpe = "Movie"

    def __init__(self, *args, **kwargs):
        # director = kwargs.pop("director")
        # cast = kwargs.pop("cast")
        super(GenericMovieMedia, self).__init__(*args, **kwargs)
        # self.attr_director = director
        # self.attr_cast = cast or list()


class GenericTutorialMedia(AbstractMediaClass):
    """
    Class for Generic Movie
    """
    MediaType = "Tutorials"

    def __init__(self, *args, **kwargs):
        author = kwargs.pop("author")
        school = kwargs.pop("school")
        super(GenericTutorialMedia, self).__init__(*args, **kwargs)
        self.attr_author = author
        self.attr_school = school


class GenericTvSeriesMedia(GenericMovieMedia):
    """
    Class for TV Series
    """
    MediaType = "Television"

    def __init__(self, *args, **kwargs):
        season = kwargs.pop("season")
        super(GenericTvSeriesMedia, self).__init__(*args, **kwargs)
        self.attr_season = season




scan_movies(root_path="D:/Movie/Movies")
