#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module docs
"""

import os
import sys
import shutil
import traceback
import datetime, os


DIR_PATH = r"E:\PrepareToEnter"



UNWANTED_WORDS = [".avi","1.4","5.1","-","DVDRip","BRRip","XviD","1CDRip","aXXo", "18+", "[Phantoms]", "+AG", "+YTS"
    "x264","720p","StyLishSaLH (StyLish Release)","DvDScr","MP3","HDRip","WebRip",
    "ETRG","YIFY","StyLishSaLH","StyLish Release","TrippleAudio","EngHindiIndonesian",
    "385MB","CooL GuY","a2zRG","x264","Hindi","AAC","AC3","MP3"," R6","HDRip","H264","ESub","AQOS",
    "ALLiANCE","UNRATED","ExtraTorrentRG","BrRip","mkv","mpg","DiAMOND","UsaBitcom","AMIABLE",
    "BRRIP","XVID","AbSurdiTy","DVDRiP","TASTE","BluRay","HR","COCAIN","_",".","BestDivX","MAXSPEED",
    "Eng","500MB","FXG","Ac3","Feel","Subs","S4A","BDRip","FTW","Xvid","Noir","1337x","ReVoTT",
    "GlowGaze","mp4","Unrated","hdrip","ARCHiViST","TheWretched","www","torrentfive",".com",
    "1080p","1080","SecretMyth","Kingdom","Release","RISES","DvDrip","ViP3R","RISES","BiDA","READNFO",
    "HELLRAZ0R","tots","BeStDivX","UsaBit","FASM","NeroZ","576p","LiMiTED","Series","ExtraTorrent","DVDRIP","~",
    "BRRiP","699MB","700MB","greenbud","B89","480p","AMX","007","DVDrip","h264","phrax","ENG","TODE","LiNE",
    "XVid","sC0rp","PTpower","OSCARS","DXVA","MXMG","3LT0N","TiTAN","4PlayHD","HQ","HDRiP","MoH","MP4","BadMeetsEvil",
    "XViD","3Li","PTpOWeR","3D","HSBS","CC","RiPS","WEBRip","R5","PSiG","'GokU61","GB","GokU61","NL","EE","Rel","NL",
    "PSEUDO","DVD","Rip","NeRoZ","EXTENDED","DVDScr","xvid","WarrLord","SCREAM","MERRY","XMAS","iMB","7o9",
    "Exclusive","171","DiDee","v2", "SPRiNTER", "X264", "USABIT", "YTS", "750 MB", "950MB", "MkvCage", "iExTV",
    "MovieMp4", "Net", "[","]","(",")","{","}","{{","}}", "WEB", "HD", "+Team", "+IcTv", "+CAM", "+TuttyFruity",
    "UNCUT", "Ozlem", "BRrip", "Harshad", "Dual", "Audio", "BLiTZCRiEG"
    ]

FIRST_YEAR = 1900
LAST_YEAR = datetime.date.today().year + 1

def get_movie_name(input_media_name):
    year = None
    # find if the year exists in the movie name
    for eachYear in range(FIRST_YEAR, LAST_YEAR):
        if str(eachYear) in input_media_name:
            year = eachYear
            break

    if year:

        split_by_year = str(input_media_name).split(str(year))
        if len(split_by_year) > 1:
            prefix, suffix = split_by_year
            input_media_name = input_media_name.replace(suffix, "")

    input_media_name = input_media_name.replace(str(year), " ")

    # remove unwanted words from the media name.
    for word in UNWANTED_WORDS:
        input_media_name = input_media_name.replace(word, " ")

    input_media_name = input_media_name.replace(".", " ")
    input_media_name = input_media_name.strip();

    while "  " in input_media_name:
        input_media_name = input_media_name.replace("  ", " ")

    if year:
        input_media_name += " (%s)" % year

    return input_media_name



def moveMediaToTheirRespectiveDirectory(movieDirPath=None):
    movieDirPath = movieDirPath or DIR_PATH

    for child in os.listdir(movieDirPath):
        filePath = os.path.join(movieDirPath, child)
        if not os.path.isfile(filePath):
            continue

        movieDir = get_movie_name(filePath)

        if not os.path.isdir(movieDir):
            os.makedirs(movieDir)

        newMoviePath = os.path.join(movieDir, os.path.basename(filePath))

        try:
            shutil.move(filePath, newMoviePath)
        except Exception as e:
            print(e)
            traceback.print_exc()



def clearMovieDirNames(movieDirPath=None):
    """
    """
    movieDirPath = movieDirPath or DIR_PATH

    for movieDir in os.listdir(movieDirPath):

        if movieDir.startswith("_"):
            continue

        dirPath = os.path.join(movieDirPath, movieDir)
        if not os.path.isdir(dirPath):
            moveMediaToTheirRespectiveDirectory(movieDirPath=movieDirPath)

        newMoviePath = get_movie_name(dirPath)

        try:
            os.rename(dirPath, newMoviePath)
        except Exception as e:
            print(e)
            traceback.print_exc()


