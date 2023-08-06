#!/usr/bin/env python3
import json
import re

from .utils import join as utils_join
from os.path import isfile


def title_search(library, title):
    """
    First perform a simple search for the chapter by checking if it is
    listed in the user's library. This may not be 100% accurate if your library
    is not up-to-date, for that reason if the simple search does not return
    anything we do a deeper search to see if the file exists in your base_dir
    in a tracked show. If all of this fails we return None
    """
    for dir in library.keys():
        if dir == title:
            return dir
    return None


def main_search(user, chapter, track=False):
    """The main search loop"""
    with open(user.files["library_file"], "r") as data:
        library = json.load(data)
    base_dir = user.settings["base_dir"]
    path = re.sub("(^.*)/.*$", r"\1", chapter)
    title = re.sub("^.*/", "", path)
    chapter = re.sub("^.*/", "", chapter)
    dir = title_search(library, title)
    if dir is None:
        return 1
    if track:
        track_chapter(dir, chapter, library, user)
    return 0


def track_chapter(dir, chapter, library, user):
    """
    Track an chapter in user's library by updating
    thier library and log file
    """
    log_file = user.files["log_file"]
    max = int(user.settings["max_history"])
    # Update library
    library[dir]["reading"] = chapter
    log = {}
    log[dir] = library[dir]
    if isfile(log_file):
        with open(log_file, "r") as data:
            old_log = json.load(data)
            if dir in old_log:
                old_log.pop(dir)
            if len(old_log) >= max:
                old_log.popitem()
            log.update(old_log)
    for dir in log.keys():
        log[dir] = library[dir]
    with open(log_file, "w+") as data:
        json.dump(log, data, indent=4)
    with open(user.files["library_file"], "w+") as data:
        json.dump(library, data, indent=4)
    return library
