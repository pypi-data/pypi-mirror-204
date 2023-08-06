#!/usr/bin/env python3
import os
from loadconf import Config


class NoBaseDirExists(Exception):
    """Exception raised when user has a base directory set
    but it does not exist.
    """

    def __init__(self, conf_file, message="ERROR: Base directory is set to"):
        self.file = conf_file
        self.message = message

    def __str__(self):
        return f'{self.message} "{self.file}" which does not exist'


class NoBaseDir(Exception):
    """Exception raised when user has not set a base directory"""

    def __init__(self, conf_file, message="ERROR: Base directory not set in"):
        self.file = conf_file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} "{self.file}"'


def get_user_settings(program, args):
    # Create user object to read files and get settings
    user = Config(program=program)
    # Define some basic settings, files, etc.
    user_settings = {
        "base_dir": None,
        "debug": False,
        "extra_conf": False,
        "file_manager": None,
        "language": "",
        "max_history": 20,
        "not_found": False,
        "opener": "zathura",
        "prompt_cmd": "fzf",
        "prompt_args": "",
        "track_cmd": "znp -e 'quit' -g {page} {track}",
        "zip_util": "tar",
    }
    config_files = {
        "conf_file": "mlm.conf",
        "log_file": "log.json",
        "filters_file": "filters.conf",
        "library_file": "library.json",
        "library_bak_file": "library.json.bak",
        "gdl_file": "gdl_config.json",
    }
    files = [
        "conf_file",
        "filters_file",
        "library_file",
    ]
    settings = list(user_settings.keys())
    # Fill out user object
    user.define_settings(settings=user_settings)
    user.define_files(user_files=config_files)
    user.create_files(create_files=files)
    user.read_conf(user_settings=settings, read_files=["conf_file"])
    user.store_files(files=["filters_file"])
    # Check that the required settings are defined
    if user.settings["base_dir"] is None:
        raise NoBaseDir(conf_file=user.settings["base_dir"])
    elif not os.path.isdir(user.settings["base_dir"]):
        raise NoBaseDirExists(conf_file=user.settings["base_dir"])

    return user, args
