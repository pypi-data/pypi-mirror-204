#!/usr/bin/env python3
import json
import pathlib
import re
import sys
from os.path import join as os_join


def auto_title(dir_name, user_system):
    """
    Generate a title from dir_name
    e.g. /path/to/[Group] Show Season 01 (1080p) [Hash info]
    returns ' - path - to - Show Season 01 (1080p)'
    """

    title = re.sub(r"\s?\[[^]]*\]\s?", "", dir_name)
    if user_system == "Windows":
        title = re.sub("\\\\", " - ", title)
    else:
        title = re.sub(r"/", " - ", title)

    return title


def add_url(url, dir, user):
    """
    Associate the given url with given dir
    """
    lib = pathlib.Path(user.files["library_file"])
    dir_name = pathlib.Path(dir).name

    def backup_library():
        lib.replace(user.files["library_bak_file"])

    with open(user.files["library_file"], "r") as data:
        library = json.load(data)
    if dir_name in library.keys():
        library[dir_name]["url"] = url
        backup_library()
        with open(user.files["library_file"], "w+") as data:
            json.dump(library, data, indent=4)
            return 0
    return 1


def cprint(color: str, string, out_file=sys.stdout):
    """
    Red: \033[31m
    Green: \033[32m
    Yellow: \033[33m
    Blue: \033[34m
    Magenta: \033[35m
    Cyan: \033[36m
    """
    format = ""
    end = "\033[0m"
    if color.lower() == "red":
        format = "\033[31m"
    elif color.lower() == "green":
        format = "\033[32m"
    elif color.lower() == "yellow":
        format = "\033[33m"
    elif color.lower() == "blue":
        format = "\033[34m"
    elif color.lower() == "magenta":
        format = "\033[35m"
    elif color.lower() == "cyan":
        format = "\033[36m"
    else:
        print(string, file=out_file)
        return
    print(format + string + end, file=out_file)


def format_string(
    raw_string: str,
    args,
) -> str:
    format_dict = {
        "page": args.page,
        "track": args.track,
    }
    ret_str = raw_string
    format_keys = re.findall("{([^}]+)}", ret_str)
    for format_key in format_keys:
        # Check if item_key is a known key
        if format_key in format_dict.keys():
            replace_str = format_dict[format_key]
            ret_str = ret_str.replace(f"{{{format_key}}}", replace_str)
    return ret_str


def join(a, b):
    return os_join(a, b)


def key_value_list(dic, search_key=None):
    """
    Take a dicionary and return two lists one for keys and one for values
    """
    # While it is easiest if dic is a true dict
    # it need not be. As long as the items in dic
    # _are_ true dicts then we can make do
    def psuedo_dic():
        for item in dic:
            if isinstance(item, dict):
                true_dic(item)

    def true_dic(d=dic):
        if search_key is None:
            keys.extend(d.keys())
            values.extend(d.values())
        else:
            for key, value in d.items():
                if key == search_key:
                    keys.append(key)
                    values.append(value)

    keys = []
    values = []
    if isinstance(dic, dict):
        true_dic()
    else:
        psuedo_dic()

    return keys, values


def merge_libraries(old_dict, new_dict):
    """Takes two dictionaries and merges them"""
    merged_dict = {}
    pop_key = None
    for new_key, new_val in new_dict.items():
        match = False
        for old_key, old_val in old_dict.items():
            if old_key == new_key:
                match = True
                old_val["chapters"] = new_val["chapters"]
                old_val["update_time"] = new_val["update_time"]
                merged_dict[old_key] = old_val
                pop_key = old_key
                break
        if match:
            old_dict.pop(pop_key, None)
            continue
        merged_dict[new_key] = new_val
    return merged_dict


def pad_string(string: str):
    # convert input string to float, then back to string with 1 decimal place
    converted_string = "{:.1f}".format(float(string))
    # pad the string with zeros on the left to make it 3 characters long
    padded_string = converted_string.zfill(5)
    return padded_string


def query_library(lib_file):
    ret = []
    with open(lib_file, "r") as data:
        library = json.load(data)
    for k, v in library.items():
        if v["url"] is None:
            continue
        ret.append((v["url"], k, float(v["chapters"][-1].split(".")[0])))
    return ret


def sort_updated_dirs(library):
    update_dict = {}
    for k in library.keys():
        update_dict[library[k]["update_time"]] = k
    update_list = list(update_dict.keys())
    update_list.sort(reverse=True)
    return [update_dict[i] for i in update_list]
