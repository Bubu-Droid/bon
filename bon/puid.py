import hashlib
import json
import random
import string
from datetime import datetime
from pathlib import Path

from .config import DB_FILE_EXT, DB_NAME, HOME, MODULE_NAME

letters = []
letters.extend(i for i in string.ascii_uppercase)
letters.extend(i for i in string.digits)


def gen_puid(puid_len: int) -> str:
    sample_txt = ""
    sample_txt = "".join(random.sample(letters, k=puid_len))
    puid = (
        "Z"
        + (hashlib.sha256(sample_txt.encode("ascii")).hexdigest())[
            0 : (puid_len - 1)
        ].upper()
    )
    return puid


def get_new_puid(puid_file: Path, puid_len: int) -> str:
    with puid_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    puid_list = [entry["puid"] for entry in data]

    new_puid = gen_puid(puid_len)
    while new_puid in puid_list:
        new_puid = gen_puid(puid_len)

    new_entry = {
        "puid": new_puid,
        "created_at": datetime.now().isoformat(),
    }

    data.append(new_entry)
    with puid_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return new_puid


def fetch_file(puid: str) -> Path:
    target = f"{puid}.{DB_FILE_EXT}"
    base = Path(HOME) / MODULE_NAME / DB_NAME

    for path in base.rglob(target):
        return path

    return Path("")
