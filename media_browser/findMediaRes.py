#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
import os
import sys
from pymediainfo import MediaInfo

MEDIA_FILE_TYPES    = [".mp4", ".avi", ".mkv"]
IGNORE_FILE_TYPES   = [".srt", ".txt", ".jpg", ".sub"]


MEDIA_DIR_PATH      = r"E:\PrepareToEnter"


class MediaMetadata(object):
    """

    """
    def __init__(self, media_path=None):
        self.media_path = media_path
        self.media_info = self.parse_media_info()

        self.video_track = None

    def parse_media_info(self):
        self.media_info = MediaInfo.parse(self.media_path)
        self._getVideoTrack()
        return self.media_info

    @classmethod
    def from_media(cls, media_path):
        return cls(media_path=media_path)

    def _getVideoTrack(self):
        for track in self.media_info.tracks or []:
            if track.track_type == "Video":
                self.video_track = track
                return self.video_track
        print("Cannot find video track in media : %s" % self.media_path)
        return None

    def getMediaResolution(self):
        if not self.video_track:
            self._getVideoTrack()

        if not self.video_track:
            return False

        return [self.video_track.width, self.video_track.height]

    def getMediaDuration(self, in_minutes=True):
        if not self.video_track:
            self._getVideoTrack()

        if not self.video_track:
            return False

        duration = [d for d in self.video_track.to_data().get("other_duration", []) if ":" in str(d)]
        for d in duration or []:
            if len(d) == 12:
                if in_minutes:
                    h, m, s = str(d).split(":")
                    total_time = (float(h) * 60) + float(m) + (float(s) / 60)
                    return total_time
                else:
                    return d

        print("ERROR: Cannot parse media duration :  %s " % self.media_path)
        return False


class FilterMovies(object):
    """
    """
    SHORT_MEDIA_TIME = 20   # (minutes) less then SHORT_MEDIA_TIME will be calculated as Short Media
    LOW_RES_WIDTH    = 900  # (pixels)  less then LOW_RES_WIDTH will be calculated as Low Res Media

    def __init__(self, media_dir_path=None):
        self.media_dir_path  = media_dir_path or MEDIA_DIR_PATH
        self.media_info_dict = dict()

        self.load_media_from_dir()

    def load_media_from_dir(self):
        for root, dirs, files in os.walk(self.media_dir_path):
            if not files:
                continue

            for each_file in files:
                file_path = os.path.join(root, each_file)

                is_subtitle = [e for e in IGNORE_FILE_TYPES if file_path.endswith(e)]
                if is_subtitle:
                    continue

                is_media = [e for e in MEDIA_FILE_TYPES if file_path.endswith(e)]
                if not is_media:
                    continue

                obj = MediaMetadata(file_path)
                self.media_info_dict[file_path] = obj

    def getLowResMedia(self):
        if not self.media_info_dict:
            self.load_media_from_dir()

        for media_path, media_obj in self.media_info_dict.items():
            width, height = media_obj.getMediaResolution()

            if width < self.LOW_RES_WIDTH:
                print(width, height, media_path)

    def getShortDurationMedia(self):
        if not self.media_info_dict:
            self.load_media_from_dir()

        for media_path, media_obj in self.media_info_dict.items():
            duration = media_obj.getMediaDuration(in_minutes=True)

            if float(duration) < self.SHORT_MEDIA_TIME:
                print(media_path)
                os.startfile(os.path.dirname(media_path))




x = FilterMovies(r"E:\Movies")
x.getLowResMedia()







