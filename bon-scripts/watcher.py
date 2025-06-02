import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import bon


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
    fin_list.append(db_list[0])
    fin_list.extend(tex_content.split(bon.TEX_SEP)[1:-1])
    return (bon.SEPARATOR).join(fin_list)


def start_watcher(watch_file, output_file):
    event_handler = TexChangeHandler(watch_file, output_file)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(watch_file), recursive=False)
    observer.start()
    return observer
