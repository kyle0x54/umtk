import os
from pathlib import Path
from typing import Union


def isdicom(path: Union[str, Path]) -> bool:
    """ Judge whether a given file is a valid dicom.

    Args:
        path(str or Path): given file path.

    Returns:
        (bool): True if given path is a valid dicom, otherwise False.
    """
    if not os.path.isfile(path):
        return False

    # read preamble and magic code
    with open(path, 'rb') as f:
        header = f.read(132)

    if not header:
        return False

    # magic code of a dicom file should be 'DICM'
    return False if header[128:132] != b'DICM' else True
