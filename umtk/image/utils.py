import os
from pathlib import Path
from typing import Any, Dict, Union
import numpy as np


def isdicom(path: Union[str, Path]) -> bool:
    """ Judge whether a given file is a valid dicom.

    Args:
        path: given file path.

    Returns:
        True if given path is a valid dicom, otherwise False.
    """
    if not os.path.isfile(path):
        return False

    # read preamble and magic code
    with open(path, "rb") as f:
        header = f.read(132)

    if not header:
        return False

    # magic code of a dicom file should be "DICM"
    return False if header[128:132] != b"DICM" else True


def get_reorient_image(vtd: Dict[str, Any]) -> np.ndarray:
    return np.flip(
        vtd["image_zyx"],
        np.where(vtd["direction_zyx"] < 0)[0]
    )
