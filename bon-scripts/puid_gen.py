import hashlib
import random
import string

letters = []
letters.extend(i for i in string.ascii_uppercase)
letters.extend(i for i in string.digits)


def check_puid(puid_file: str, puid: str) -> bool:
    puid_list = []
    res = False
    with open(puid_file, "r", encoding="utf-8") as f:
        for i in f.readlines():
            if i.strip():
                puid_list.append(i.strip())
    if puid in puid_list:
        res = False
    else:
        res = True
    return res


def gen_puid(puid_file: str, puid_len: int) -> str:
    sample_txt = ""
    sample_txt = "".join(random.sample(letters, k=puid_len))
    puid = (
        "Z"
        + (hashlib.sha256(sample_txt.encode("ascii")).hexdigest())[
            0 : (puid_len - 1)
        ].upper()
    )
    while not check_puid(puid_file, puid):
        sample_txt = ""
        sample_txt = "".join(random.sample(letters, k=puid_len))
        puid = (
            "Z"
            + (hashlib.sha256(sample_txt.encode("ascii")).hexdigest())[
                0 : (puid_len - 1)
            ].upper()
        )

    with open(puid_file, "a", encoding="utf-8") as f:
        print(puid, file=f)
    return puid
