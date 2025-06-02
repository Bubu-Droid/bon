import os
from datetime import datetime
from subprocess import Popen, run

import watcher
from puid_gen import gen_puid


def main(
    home: str,
    editor: str,
    terminal: str,
    db_name: str,
    db_file_ext: str,
    tmp_path: str,
    tmp_file_name: str,
    puid_len: int,
) -> None:
    puid = gen_puid(os.path.join(home, "bon/bon-scripts/", db_name), puid_len)
    db_file_path = os.path.join(home, "bon/bon-db/", f"{puid}{db_file_ext}")
    tmp_file_path = os.path.join(tmp_path, tmp_file_name)
    bon_add_template = rf"""\documentclass[12pt]{{article}}

\usepackage[min]{{bubu}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\title{{BON PREVIEW}}
\author{{Avigyan Chakraborty}}
\date{{\today}}

\begin{{document}}

\section*{{{puid}}}

%---%
\begin{{problem}}
  
\end{{problem}}
%---%
\begin{{soln}}
  
\end{{soln}}
%---%

\end{{document}}"""
    date_now = datetime.now()
    date_format = date_now.strftime("%Y-%m-%d")
    db_file_template = rf"""desc: 
puid: {puid}
source: []
tags: []
date: {date_format}
hardness: 
---

---

"""

    run(["touch", db_file_path], check=False)
    with open(db_file_path, "w", encoding="utf-8") as f:
        f.write(db_file_template)
    run(["mkdir", "-p", tmp_path], check=False)
    run(["touch", tmp_file_path], check=False)
    with open(tmp_file_path, "w", encoding="utf-8") as f:
        f.write(bon_add_template)
    Popen(
        [
            terminal,
            "-e",
            "zsh",
            "-c",
            f"cd {tmp_path} && latexmk -pdf -pvc {tmp_file_name}",
        ]
    )
    observer = watcher.start_watcher(tmp_file_path, db_file_path)
    run([editor, tmp_file_path], check=False)
    observer.stop()
    observer.join()
