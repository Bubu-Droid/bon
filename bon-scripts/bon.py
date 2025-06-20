#!/usr/bin/env python3

# Bon Database Manager by Bubu
# https://github.com/Bubu-Droid/bon/tree/main

import argparse
import os

import add
import edit
import preview

HOME = os.environ.get("HOME", "/bubu/home")
EDITOR = os.environ.get("EDITOR", "nvim")
TERMINAL = os.environ.get("TERM", "alacritty")
DB_NAME = "puids.txt"
DB_FILE_EXT = ".txt"
TMP_PATH = "/tmp/preview/"
TMP_FILE_NAME = "bon-preview.tex"
PUID_LEN = 6
SEPARATOR = "\n---\n"
TEX_SEP = "\n%---%\n"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BON DB Manager")
    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="Add a problem into the database",
    )
    parser.add_argument(
        "-e",
        "--edit",
        metavar="puid",
        action="store",
        help="Edit a problem in the database",
    )
    parser.add_argument(
        "-p",
        "--preview",
        metavar="puid",
        action="store",
        help="Preview the pdf of a problem in the database",
    )

    args = parser.parse_args()

    if args.add:
        add.main(
            HOME,
            EDITOR,
            TERMINAL,
            DB_NAME,
            DB_FILE_EXT,
            TMP_PATH,
            TMP_FILE_NAME,
            PUID_LEN,
        )
    if args.edit:
        puid = args.edit
        edit.main(
            HOME,
            EDITOR,
            TERMINAL,
            TMP_PATH,
            TMP_FILE_NAME,
            puid,
            DB_FILE_EXT,
            SEPARATOR,
            TEX_SEP,
        )
    if args.preview:
        puid = args.preview
        preview.main(
            HOME,
            TERMINAL,
            TMP_PATH,
            TMP_FILE_NAME,
            puid,
            DB_FILE_EXT,
            SEPARATOR,
            TEX_SEP,
        )
