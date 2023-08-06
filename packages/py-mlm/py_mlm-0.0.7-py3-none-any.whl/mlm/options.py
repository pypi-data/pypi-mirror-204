#!/usr/bin/env python3
import argparse


def get_opts(prog_name="mlm"):
    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="""Track and watch your media library""",
        allow_abbrev=False,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-a",
        "--add",
        metavar="URL",
        action="append",
        help="""
        Download manga and track URL. Can give the --max-chapter flag to limit the
        number of chapters downloaded.
        """,
    )
    group.add_argument(
        "-b",
        "--build",
        action="store_true",
        help="""Build the LIBRARY file. Use -i to build this file interactively.""",
    )
    group.add_argument(
        "-B",
        "--browse",
        action="store_true",
        help="""
        Browse your BASE_DIR. Set your file manager of choice in the mlm.conf
        like so:
            FILE_MANAGER="st -e lf"
        TUI file managers like lf, nnn, ranger,
        etc. typically must be started in a terminal emulator.
        """,
    )
    group.add_argument(
        "-D",
        "--download-new",
        action="store_true",
        help="""
        Download new chapters of manga in your library.
        A title must have an associated url.
        By default will download all chapters after your most recent chapter.
        Use -m, --max-chapters N to limit new downloads to N more than your most
        recent chapter.
        """,
    )
    group.add_argument(
        "-l",
        "--latest",
        action="store_true",
        help="""List your latest tracked manga to resume reading.""",
    )
    group.add_argument(
        "-o",
        "--open",
        metavar="FILE",
        help="""
        This is a sort of wrapper for zathura which will also track the anime
        when closed.
        """,
    )
    group.add_argument(
        "-r",
        "--read",
        action="store_true",
        help="""
        List all titles in your library. If the chosen title is being
        tracked then the last tracked chapter will be shown in zathura.
        If this is a title that has no tracked chapter then a list
        of all chapters found in the title's dir
        will be listed for you to choose from.
        """,
    )
    group.add_argument(
        "-s",
        "--search",
        metavar="FILE",
        help="""
        Take a file path and check if it is in your BASE_DIR. Returns 0 if
        successful or 1 if the file is not in in your BASE_DIR.
        """,
    )
    group.add_argument(
        "-t",
        "--track",
        metavar="FILE",
        help="""
        This will track the given FILE. It is best if the the given FILE is the
        full path to the file. If FILE is a relative path then mlm will attempt
        to find this file in one of the dirs in your library.  If this is not
        possible you will be informed. The most likely reason that this would
        happen is that the file is in a dir that has been filtered or it is a
        new dir that has not been added to your library. In this case update
        your library and attempt to track again. FILE should be a file somewhere
        in your BASE_DIR otherwise it will be impossible to track.
        """,
    )
    group.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="""
        This will update your library file to match any new or renamed
        directories. If the directory name has not changed your tracked episodes
        will carry over. If this is not a new directory but one that has been
        renamed it will be treated as new and no episode tracking will be
        carried over.
        """,
    )
    group.add_argument(
        "-U",
        "--url",
        metavar="URL",
        action="store",
        help="""
        URL to associate with DIR.
        """,
    )
    group.add_argument(
        "-z",
        "--zip",
        action="store_true",
        help="""
        (Re)zip the PATH given by --path or the $PWD if not supplied. This will
        create a cbz file for each dir matching the following regex:
        ^.*[0-9]\\.[0-9]$
        """,
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="""
        Use this flag with -u if you do not want to keep a backup of your library.
        """,
    )
    parser.add_argument(
        "-d",
        "--dir",
        metavar="DIR",
        action="store",
        help="""
        DIR to use for other options like --url, and --move
        """,
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="""
        Use when building or updating your library.  This will make the process
        interactive. By default mlm tries to set the title of a dir to something
        sane.  See the man page or github for more detailed info about this. If
        you prefer to set the title value yourself then use this flag. If run in
        a terminal you will see what the auto generated title would be if you do
        not enter anything into the dmenu prompt by pessing ESC
        """,
    )
    parser.add_argument(
        "-m",
        "--max-chapter",
        metavar="N",
        action="store",
        help="""
        Download a max of N chapters. If downloading with --add this will
        be an absolute max. If downloading with --download-new this will be
        N more than the most recent chapter in your library.
        """,
    )
    parser.add_argument(
        "-M",
        "--min-chapter",
        metavar="N",
        action="store",
        help="""
        Download chapters starting at N. This is only used when using --add
        """,
    )
    parser.add_argument(
        "-n",
        "--new",
        action="store_true",
        help="""
        Use with --read to list manga in order of update order.
        """,
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="""
        Used with --zip. If DIR is given the zipped files will be placed in
        """,
    )
    parser.add_argument(
        "-p",
        "--page",
        action="store",
        type=int,
        default=-1,
        help="""
        Used for better accuracy when tracking a file.
        """,
    )
    parser.add_argument(
        "-P",
        "--path",
        metavar="PATH",
        action="store",
        help="""
        The PATH to --zip.
        """,
    )
    args = parser.parse_args()
    return args
