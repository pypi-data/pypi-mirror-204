#!/usr/bin/env python3
import shlex
import sys


from .build import build_main, update_library
from .config import NoBaseDir, NoBaseDirExists, get_user_settings
from .g_dl import bulk_new, bulk_latest
from .media import read_manga
from .options import get_opts
from .search import main_search
from .system import browse_base, open_process, re_zip
from .utils import add_url, cprint, format_string


__license__ = "GPL-v3.0"
__program__ = "mlm"


def process_opts(user, args):
    """
    Opts handler for main
    """
    if args.build:
        cprint("green", "Building")
        return build_main(user, args)
    elif args.browse:
        return browse_base(user)
    elif args.open is not None:
        cprint("green", "Opening the given file")
    elif args.search is not None:
        return main_search(user, chapter=args.search)
    elif args.track is not None:
        main_search(user, chapter=args.track, track=True)
        cmd = shlex.split(format_string(user.settings["track_cmd"], args))
        # cmd = shlex.split(f"znp -e 'quit' -g '{args.page}' '{args.track}'")
        return open_process(opener=cmd)
    elif args.update:
        cprint("green", "Updating library")
        return update_library(user, args)
    elif args.read or args.latest:
        return read_manga(user, latest=args.latest, new=args.new)
    elif args.url is not None and args.dir is not None:
        return add_url(url=args.url, dir=args.dir, user=user)
    elif args.add is not None:
        return bulk_new(user=user, args=args)
    elif args.download_new:
        return bulk_latest(user=user, args=args)
    elif args.zip:
        return re_zip(user=user, args=args)
    else:
        cprint("green", "Updating library")
        return update_library(user, args)


def main():
    """
    Command line application to view and track media
    """
    # Set and get command line args
    args = get_opts(__program__)

    try:
        # Creates a UserSettings object. This will be used by various function
        # to access file paths, settings, filters, and command line args
        user, args = get_user_settings(program=__program__, args=args)
    except (NoBaseDir, NoBaseDirExists) as err:
        cprint("red", err.message, out_file=sys.stderr)
        return 1

    # Execute the appropriate function based on command line options
    return process_opts(user, args=args)


if __name__ == "__main__":
    sys.exit(main())
