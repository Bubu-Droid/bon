import os
import subprocess


def make_tex_code(db_text: str, puid: str, separator: str, tex_sep: str) -> str:
    db_sec = db_text.split(separator)
    bon_inner_txt = tex_sep + tex_sep.join(db_sec[1:]) + tex_sep

    bon_preview_template = rf"""\documentclass[12pt]{{scrartcl}}

\usepackage{{bubu}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\title{{BON PREVIEW}}
\author{{Avigyan Chakraborty}}
\date{{\today}}

\begin{{document}}

\section*{{{puid}}}
{bon_inner_txt}
\end{{document}}"""

    return bon_preview_template


def main(
    home: str,
    terminal: str,
    tmp_path: str,
    tmp_file_name: str,
    puid: str,
    db_file_ext: str,
    separator: str,
    tex_sep: str,
) -> None:
    db_file_path = os.path.join(home, "bon/bon-db/", f"{puid}{db_file_ext}")
    tmp_file_path = os.path.join(tmp_path, tmp_file_name)

    subprocess.run(["mkdir", "-p", tmp_path], check=False)
    subprocess.run(["touch", tmp_file_path], check=False)
    with open(db_file_path, "r", encoding="utf-8") as f:
        db_text = f.read()
    with open(tmp_file_path, "w", encoding="utf-8") as f:
        f.write(make_tex_code(db_text, puid, separator, tex_sep))
    subprocess.Popen(
        [
            terminal,
            "-e",
            "zsh",
            "-c",
            f"cd {tmp_path} && latexmk -pdf -pv {tmp_file_name}",
        ]
    )
