import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import bon

ENVS = {
    "problem": ("\\begin{problem}", "\\end{problem}"),
    "solution": ("\\begin{soln}", "\\end{soln}"),
}


class TexChangeHandler(FileSystemEventHandler):
    def __init__(self, watch_file, output_file):
        self.watch_file = os.path.abspath(watch_file)
        self.output_file = output_file

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == self.watch_file:
            with open(self.watch_file, "r", encoding="utf-8") as f:
                tex_content = f.read()
            with open(self.output_file, "r", encoding="utf-8") as f:
                db_content = f.read()
            with open(self.output_file, "w", encoding="utf-8") as out:
                out.write(transform(db_content, tex_content))


def transform(db_content: str, tex_content: str) -> str:
    fin_list = []
    db_list = db_content.split(bon.SEPARATOR)
    prob_spos = tex_content.index(ENVS["problem"][0])
    prob_epos = tex_content.index(ENVS["problem"][1])
    prob_cont = tex_content[prob_spos : prob_epos + len(ENVS["problem"][1])]
    fin_list.append(db_list[0])
    fin_list.append(prob_cont)
    i = 0
    while tex_content[i:].find(ENVS["solution"][0]) != -1:
        j = tex_content[i:].index(ENVS["solution"][0]) + i
        j_cpos = tex_content[j:].index(ENVS["solution"][1]) + j
        fin_list.append(tex_content[j : j_cpos + len(ENVS["solution"][1])])
        i = j_cpos
    return (bon.SEPARATOR).join(fin_list)


def start_watcher(watch_file, output_file):
    event_handler = TexChangeHandler(watch_file, output_file)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(watch_file), recursive=False)
    observer.start()
    return observer
