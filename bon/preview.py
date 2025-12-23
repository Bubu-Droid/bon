import json
from pathlib import Path
from string import Template
from subprocess import Popen

from .config import (
    HOME,
    MODULE_NAME,
    PREVIEW_TEMP,
    TERMINAL,
    TEX_SEP,
    TMP_FILE_NAME,
    TMP_PATH,
)
from .puid import fetch_file


def make_tex_code(db_content: dict, puid: str, tex_sep: str) -> str:
    bon_inner_txt = (
        tex_sep
        + "\n"
        + db_content["problem"]
        + "\n"
        + tex_sep
        + "\n"
        + ("\n" + tex_sep + "\n").join(db_content["solution"])
        + "\n"
        + tex_sep
    )

    if db_content["source"]:
        source_list = []
        for source in db_content["source"]:
            if next(iter(source.values())):
                source_list.append(
                    f"\\href{{{next(iter(source.values()))}}}{{{next(iter(source))}}}"
                )
            else:
                source_list.append(next(iter(source)))
        source = " (" + ", ".join(source_list) + ")"
    else:
        source = ""

    with PREVIEW_TEMP.open("r", encoding="utf-8") as f:
        bon_preview_temp = Template(f.read())
    bon_preview_temp = bon_preview_temp.substitute(
        puid=puid, source=source, bon_inner_txt=bon_inner_txt
    )
    return bon_preview_temp


def main(puid: str) -> None:
    if fetch_file(puid) == Path(""):
        print("PUID does not exist!")
        return
    db_file_path = Path(HOME) / MODULE_NAME / fetch_file(puid)
    tmp_file_path = Path(TMP_PATH) / TMP_FILE_NAME

    Path(TMP_PATH).mkdir(parents=True, exist_ok=True)
    with db_file_path.open("r", encoding="utf-8") as f:
        db_content = json.load(f)
    tmp_file_path.write_text(make_tex_code(db_content, puid, TEX_SEP), encoding="utf-8")

    Popen(
        [
            TERMINAL,
            "-e",
            "zsh",
            "-c",
            f"latexmk -pdf -pv {TMP_FILE_NAME}",
        ],
        cwd=TMP_PATH,
    )
