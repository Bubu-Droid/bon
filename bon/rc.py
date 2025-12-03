import os
from pathlib import Path

HOME = os.environ.get("HOME", "/bubu/home")
EDITOR = os.environ.get("EDITOR", "nvim")
TERMINAL = os.environ.get("TERM", "alacritty")
MODULE_NAME = "bon"
DB_NAME = "bon-db"
DB_LIST_FILE = "puids.json"
DB_FILE_EXT = "json"
TMP_PATH = "/tmp/preview/"
TMP_FILE_NAME = "bon-preview.tex"
PUID_LEN = 6
TEX_SEP = "%---%"
ADD_TEMP = Path(HOME) / MODULE_NAME / MODULE_NAME / "templates" / "add.txt"
EDIT_TEMP = Path(HOME) / MODULE_NAME / MODULE_NAME / "templates" / "edit.txt"
PREVIEW_TEMP = Path(HOME) / MODULE_NAME / MODULE_NAME / "templates" / "preview.txt"
CATEGORY_LIST = {
    "seq": "calculus/seq/",
    "cont": "calculus/cont/",
    "diff": "calculus/diff/",
    "int": "calculus/int/",
    "geo": "geo/",
    "alg": "alg/",
    "nt": "nt/",
    "combi": "combi/",
}
