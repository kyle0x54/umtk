import hashlib
import os
from pathlib import Path
from typing import Union


def compute_md5_str(path: Union[str, Path]):
    if not os.path.isfile(path):
        return None

    with open(path, "rb") as f:
        m = hashlib.md5()
        m.update(f.read())
        md5_code = m.hexdigest()
        return str(md5_code).lower()
