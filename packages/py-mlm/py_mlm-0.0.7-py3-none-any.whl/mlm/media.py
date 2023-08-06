#!/usr/bin/env python3
import json
import os
import sys
from .utils import cprint, sort_updated_dirs, key_value_list, join
from .prompts import user_choice, InvalidCmdPrompt, InputError
from .system import open_process


def opener_cmd(item, user, path=None):
    """
    Return a command list to feed to system.open_process
    if a path to the item is given the two will be joined
    """

    opener_list = [user.settings["opener"]]
    if user.settings["extra_conf"]:
        opener_list.extend(["-c", user.config_dir])
    if path is not None:
        item = os.path.join(path, item)
    opener_list.append(item)
    return opener_list


def read_manga(user, latest=False, new=False):
    """
    Watch a show from the user's library
    """

    def ask_user(options, user, prompt):
        """
        Ask a user something and handle any errors, return False if the user
        reponds with nothing or error is caught
        """
        try:
            choice = user_choice(options=options, user=user, prompt=prompt)
        except (InvalidCmdPrompt, InputError, KeyboardInterrupt) as err:
            cprint("red", err, sys.stderr)
            return False
        if choice is None:
            return False
        return choice

    # If latest update log so we don't prompt for shows that don't exist anymore
    if latest:
        update_log(
            log_file=user.files["log_file"],
            library_file=user.files["library_file"],
        )
        with open(user.files["log_file"], "r") as data:
            library = json.load(data)
    else:
        with open(user.files["library_file"], "r") as data:
            library = json.load(data)

    # Get vars for prompting user and selecting the desired file to watch
    dirs, values = key_value_list(library)
    _, reading = key_value_list(values, search_key="reading")
    _, chapters = key_value_list(values, search_key="chapters")

    if new:
        ask_dirs = sort_updated_dirs(library)
    else:
        ask_dirs = dirs
    choice = ask_user(options=ask_dirs, user=user, prompt="Read: ")
    if not choice:
        return 1

    index = dirs.index(choice)
    path = join(user.settings["base_dir"], dirs[index])

    # If manga is does not have a recently read chapter ask user which chapter
    # to read
    if reading[index] is None:
        opts = chapters[index]
        chapter = ask_user(options=opts, user=user, prompt="Read")
        if not chapter:
            return 1
    else:
        chapter = reading[index]

    # Get the opener command and open manga
    cmd = opener_cmd(item=chapter, path=path, user=user)

    open_process(opener=cmd)

    return 0


def update_log(log_file, library_file):
    """
    Update user log before displaying
    """

    # Compare log file and library modification
    # times. Only update log if library has been
    # modified more recently than log
    log_time = os.path.getmtime(log_file)
    lib_time = os.path.getmtime(library_file)
    if lib_time < log_time:
        return None

    # Open log and library and load to objects
    with open(log_file, "r") as data:
        log = json.load(data)
    with open(library_file, "r") as data:
        library = json.load(data)

    # Create blank log
    lib_keys = list(library.keys())
    log_keys = list(log.keys())

    # Loop over log file and check if show is
    # still in library
    for dir in log_keys:
        if not dir in lib_keys:
            log.pop(dir)

    with open(log_file, "w+") as data:
        json.dump(log, data, indent=4)


# def zathura_cmd(item, user, path=None):
#     """
#     Return a command list to feed to system.open_process
#     if a path to the item is given the two will be joined
#     """

#     z_list = ["zathura"]
#     if user.settings["zathura_conf"]:
#         z_list.extend(["-c", user.config_dir])
#     if path is not None:
#         item = os.path.join(path, item)
#     z_list.append(item)
#     return z_list
