import json
from pathlib import Path

from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from .rc import TEX_SEP


class TexChangeHandler(FileSystemEventHandler):
    def __init__(self, watch_file: Path, output_file: Path) -> None:
        self.watch_file = watch_file.resolve()
        self.output_file = output_file

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        if Path(str(event.src_path)).resolve() == self.watch_file:
            tex_content = self.watch_file.read_text(encoding="utf-8")
            with self.output_file.open("r", encoding="utf-8") as f:
                db_content = json.load(f)
            parts = tex_content.split(TEX_SEP)
            problem = parts[1]
            solution = parts[2:-1]
            db_content["problem"] = problem.strip()
            db_content["solution"] = [soln.strip() for soln in solution]
            with self.output_file.open("w", encoding="utf-8") as f:
                json.dump(db_content, f, indent=2)


def start_watcher(watch_file: Path, output_file: Path) -> BaseObserver:
    event_handler = TexChangeHandler(watch_file, output_file)
    observer = Observer()
    observer.schedule(event_handler, path=str(watch_file.parent), recursive=False)
    observer.start()
    return observer
