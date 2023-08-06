#!/usr/bin/env python3
import json
import mimetypes
import os
import pathlib
from platform import system
from promptx import (
    PromptXCmdError,
    PromptXError,
    PromptXSelectError,
)
import re
import sys
from .utils import cprint, merge_libraries
from .prompts import user_choice, InputError, InvalidCmdPrompt


def filter_directory(dir, filters):
    """
    Filter a directory based on a filter list.
    Optionally recursive
    """
    escape_dir = re.escape(dir)
    for item in filters:
        escape_item = re.escape(item)
        if re.search(f"{escape_item}$", escape_dir):
            return True
    return False


def is_cbz(file: str):
    """
    Test if the given file is a video
    """
    return file.endswith("cbz")
    # mimestart = mimetypes.guess_type(file)[0]
    # if mimestart is not None:
    #     mimestart = mimestart.split("/")[0]
    #     if mimestart == "application":
    #         return True
    # return False


def pre_build_check(user, prompt=True):
    """Check for existing user library"""

    # Create a config Path object
    library = pathlib.Path(user.files["library_file"])

    def backup_library():
        library.replace(user.files["library_bak_file"])

    # prompt_user only runs when prompt is True
    def prompt_user():
        # Ask user if they want to backup their library
        # This prompt should only run when building
        # User should not be prompted when updating
        choice = user_choice(["Yes", "No"], user, prompt="Backup library? ")
        if choice == "Yes":
            cprint("green", "Backing up library")
            backup_library()
        else:
            cprint("yellow", "Overwriting library")

    # Check if the file exists, if not create it
    if not library.is_file():
        library.touch()
        # When building this should return True
        # When updating this should return False
        return prompt
    elif prompt:
        if library.stat().st_size != 0:
            prompt_user()
        return True
    else:
        if library.stat().st_size != 0:
            backup_library()
            return True
        else:
            return False


def update_library(user, args):
    """Update a user's library"""

    # If the user's library needs to be created or is of size
    # '0' then just build the library, else update
    if not pre_build_check(user, prompt=False):
        return build_main(user, args)
    # Get a fresh library
    new_library = build_main(user, args, write=False)
    # Get the old library
    with open(user.files["library_bak_file"], "r") as old_data:
        old_library = json.load(old_data)
    # Merge the two libraries
    merged_library = merge_libraries(old_library, new_library)
    # Write updated library
    with open(user.files["library_file"], "w") as new_data:
        json.dump(
            merged_library,
            new_data,
            indent=4,
        )
    return 0


def walk_path(user, args):
    """
    Walk the base dir and return a dict with valid dirs and episodes
    Create a valid_dirs dict. This will store the raw dirs
    as the key for a show. Here is the structure
    {
        "path/to/manga": {
            "reading": "currently reading",
            "url": "https://mangadex.org/title/4edaaece-5b66-4fd5-a7e2-01f7a017ccdb/gekkan-shoujo-nozaki-san"
        }
    }
    """
    chapters = {}
    dirs = []
    valid_dirs = {}
    skip_dir = True
    base_dir = user.settings["base_dir"]
    contents = os.scandir(base_dir)
    for item in contents:
        if (
            filter_directory(item.name, user.stored["filters_file"])
            or not item.is_dir()
        ):
            continue
        chapters[item.name] = []
        files = os.scandir(item.path)
        for file in files:
            if not file.is_file():
                continue
            if is_cbz(file=file.path):
                if skip_dir:
                    skip_dir = False
                chapters[item.name].append(file.name)
        if skip_dir:
            continue
        chapters[item.name].sort()
        dirs.append(item.name)
    dirs.sort()
    for dir in dirs:
        valid_dirs[dir] = {}
        valid_dirs[dir]["reading"] = None
        valid_dirs[dir]["url"] = None
        valid_dirs[dir]["chapters"] = chapters[dir]
        mtime = pathlib.Path(base_dir, dir).lstat().st_mtime
        valid_dirs[dir]["update_time"] = mtime
    return valid_dirs


def build_main(user, args, write=True):
    """
    The main build loop for a user's library
    """

    try:
        pre_build_check(user)
    except (
        InvalidCmdPrompt,
        InputError,
        KeyboardInterrupt,
        PromptXCmdError,
        PromptXError,
        PromptXSelectError,
    ) as err:
        cprint("red", err, out_file=sys.stderr)
        return 1
    try:
        valid_dirs = walk_path(user, args)
    except (
        InvalidCmdPrompt,
        InputError,
        KeyboardInterrupt,
        PromptXCmdError,
        PromptXError,
        PromptXSelectError,
    ) as err:
        cprint("red", err, out_file=sys.stderr)
        return 1
    if write:
        with open(user.files["library_file"], "w") as data:
            json.dump(valid_dirs, data, indent=4)
    else:
        return valid_dirs
    return 0
