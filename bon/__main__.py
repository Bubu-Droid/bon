# Bon Database Manager by Bubu
# https://github.com/Bubu-Droid/bon/tree/main

import argparse

from . import add, edit, preview

parser = argparse.ArgumentParser(description="BON DB Manager")
parser.add_argument(
    "-a",
    "--add",
    metavar="category",
    action="store",
    help="add a problem into the database",
)
parser.add_argument(
    "-e",
    "--edit",
    metavar="puid",
    action="store",
    help="edit a problem in the database",
)
parser.add_argument(
    "-p",
    "--preview",
    metavar="puid",
    action="store",
    help="preview the pdf of a problem in the database",
)

args = parser.parse_args()

if args.add:
    category = args.add
    add.main(category)
if args.edit:
    puid = args.edit
    edit.main(puid)
if args.preview:
    puid = args.preview
    preview.main(puid)
