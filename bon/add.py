import json
from datetime import datetime
from pathlib import Path
from string import Template
from subprocess import Popen, run

from . import watcher
from .puid import get_new_puid
from .rc import (
    ADD_TEMP,
    CATEGORY_LIST,
    DB_FILE_EXT,
    DB_LIST_FILE,
    DB_NAME,
    EDITOR,
    HOME,
    MODULE_NAME,
    PUID_LEN,
    TERMINAL,
    TMP_FILE_NAME,
    TMP_PATH,
)


def main(category: str) -> None:
    if category not in CATEGORY_LIST:
        print(f"The category {category} is not a valid one!")
        print(f"Choose one among these: {', '.join(CATEGORY_LIST.keys())}")
        return

    puid = get_new_puid(Path(HOME) / MODULE_NAME / DB_NAME / DB_LIST_FILE, PUID_LEN)
    db_file_path = (
        Path(HOME)
        / MODULE_NAME
        / DB_NAME
        / CATEGORY_LIST[category]
        / f"{puid}.{DB_FILE_EXT}"
    )
    tmp_file_path = Path(TMP_PATH) / TMP_FILE_NAME

    Path(TMP_PATH).mkdir(parents=True, exist_ok=True)
    with ADD_TEMP.open("r", encoding="utf-8") as f:
        tex_temp = Template(f.read())
    tex_temp = tex_temp.substitute(puid=puid)
    date_now = datetime.now()
    date_format = date_now.strftime("%Y-%m-%d")
    tmp_file_path.write_text(tex_temp, encoding="utf-8")

    new_entry = {
        "desc": "",
        "puid": puid,
        "source": {},
        "tags": [],
        "date": date_format,
        "hardness": "",
        "problem": "",
        "solution": [],
    }

    with db_file_path.open("w", encoding="utf-8") as f:
        json.dump(new_entry, f, indent=2)

    Popen(
        [
            TERMINAL,
            "-e",
            "zsh",
            "-c",
            f"latexmk -pdf -pvc {TMP_FILE_NAME}",
        ],
        cwd=TMP_PATH,
    )
    observer = watcher.start_watcher(tmp_file_path, db_file_path)
    run([EDITOR, tmp_file_path], check=False)
    observer.stop()
    observer.join()
