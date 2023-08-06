#!/usr/bin/env python3
import mimetypes
import os
import pathlib
import re
import subprocess
import sys
import shlex
import shutil

from .utils import cprint, pad_string


class OpenerError(Exception):
    """Exception raised when command fails"""

    def __init__(self, error, message="ERROR: Failed to run"):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} {self.error}"


def browse_base(user):
    """
    Browse a user's base directory with their desired program
    """
    base_dir = user.settings["base_dir"]
    opener = shlex.split(user.settings["file_manager"])
    if opener is None:
        raise OpenerError(user.files["conf_file"])
    opener.append(base_dir)
    try:
        open_process(opener)
    except OpenerError as err:
        cprint("red", err, out_file=sys.stderr)
        return 1


def check_zip_mimetype(path: pathlib.Path):
    process = subprocess.Popen(["printf", ""])
    recheck_flag = False
    for file_path in path.glob("*.zip"):
        if mimetypes.guess_type(file_path)[0] == "application/zip":
            continue
        cprint("yellow", f"Remaking broken zip: {file_path}")
        if not recheck_flag:
            recheck_flag = True
        file_path.unlink()
        dir = file_path.as_posix().replace(".zip", "")
        process = subprocess.Popen(["bsdtar", "-caf", f"{dir}.zip", dir])
    process.wait()
    return recheck_flag


def clean_dir_name(dir: pathlib.Path):
    pattern = r"([0-9]+\.?[0-9]*)"
    match = re.search(pattern, dir.name)
    if not match:
        return
    new_name = pad_string(match.group(1))
    new = dir.parent.as_posix() + "/" + new_name
    dir.rename(new)


def create_directory(base_dir, dir):
    """
    Create the given list of directories in base_dir
    """
    dir_path = pathlib.Path(base_dir, dir)
    if dir_path.is_dir():
        return True
    elif dir_path.is_file():
        return False
    dir_path.mkdir(parents=True)
    return True


def get_dirs(path: pathlib.Path):
    # list all files and directories under the given path
    entries = os.listdir(path)
    # filter out the directories
    directories = [
        pathlib.Path(path, entry)
        for entry in entries
        if os.path.isdir(pathlib.Path(path, entry))
    ]
    return directories


def get_files(path: pathlib.Path):
    # list all files and directories under the given path
    entries = os.listdir(path)
    # filter out the directories
    files = [
        pathlib.Path(path, entry)
        for entry in entries
        if os.path.isfile(pathlib.Path(path, entry))
    ]
    return files


def make_cbz(path: pathlib.Path):
    files = get_files(path)
    for file in files:
        name = file.name.replace("zip", "cbz")
        file.rename(file.parent.as_posix() + "/" + name)


def move_cbz(dest, path: pathlib.Path):
    target_dir = pathlib.Path(dest, path.name)
    for file in os.listdir(path):
        if not file.endswith("cbz"):
            continue
        dest_file = pathlib.Path(target_dir / file)
        if dest_file.exists() and dest_file.is_file():
            dest_file.unlink()
        elif dest_file.is_dir():
            raise OSError(f"Destination is a directory {dest_file}")
        shutil.move(file, target_dir)


def move_to_raw(base_dir, path: pathlib.Path):
    move_to_x(base_dir, "raw_manga", path)


def move_to_x(base_dir, x: str, path: pathlib.Path):
    target_dir = pathlib.Path(base_dir, x, path.name)
    dirs = get_dirs(path)
    for dir in dirs:
        target_path = target_dir / dir.name
        shutil.move(dir, target_path)


def open_process(opener, out=subprocess.DEVNULL, err=subprocess.STDOUT):
    """Open a program with the given opener list"""
    try:
        subprocess.Popen(opener, stdout=out, stderr=err)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise OpenerError(opener)


def remove_directory(path: pathlib.Path):
    try:
        shutil.rmtree(path)
    except Exception as e:
        cprint("red", f"Error deleting directory {path}: {e}", out_file=sys.stderr)


def return_cmd(cmd):
    """
    Run a command and return the the output as a dict
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return {"stdout": stdout.decode("utf-8"), "stderr": stderr.decode("utf-8")}


def re_zip(user, args):
    if args.path is None:
        path = pathlib.Path().absolute()
    else:
        path = pathlib.Path(args.path)
    cprint("green", f"(Re)zipping '{path}'")
    zip_dirs_in_path(path)
    make_cbz(path)
    if args.dir is None:
        base = user.settings["base_dir"]
    else:
        base = args.dir
    if args.move:
        move_cbz(base, path)
    # if args.move is not None and args.move == "base_dir":
    #     move_to_x(user.settings["base_dir"], "", path)
    # elif args.move is not None:
    #     move_cbz_to(args.move, path)


def run_cmd(cmd):
    subprocess.run(cmd)


def zip_dirs_in_path(path: pathlib.Path):
    dir_pattern = re.compile(r".*/[0-9]+\.[0-9]$")
    # get a list of all directories in the current directory
    dirs = get_dirs(path)
    # filter the list to only include directories that match the pattern
    dirs_to_compress = filter(lambda x: dir_pattern.match(x.as_posix()), dirs)
    # compress each directory using bsdtar and subprocess
    process = subprocess.Popen(["printf", ""])
    for d in dirs_to_compress:
        dir_path, chapter = d.as_posix().rsplit("/", 1)
        if not dir_path.startswith("/"):
            cprint("red", f"ERROR: cannot zip -- '{d}'")
            continue
        process = subprocess.Popen(
            [
                "tar",
                "--sort=name",
                "-C",
                dir_path,
                "-caf",
                f"{d}.zip",
                chapter,
            ]
        )
    process.wait()
