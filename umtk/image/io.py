import os
from pathlib import Path
from typing import Any, Dict, List, Union
import SimpleITK
import numpy as np


def _get_file_title(path: Union[str, Path]):
    file_title = os.path.splitext(os.path.basename(path))[0]
    if path.endswith(".nii.gz"):
        return os.path.splitext(file_title)[0]
    else:
        return file_title


def read_itk(
    path: Union[str, Path],
    keep_itk_image: bool = False
) -> Dict[str, Any]:
    """ Read an itk format image.

    Args:
        path: itk image file path.
        keep_itk_image: whether to return original itk image.

    Returns:
        dict containing volume data and dicom tags.
    """
    image_itk = SimpleITK.ReadImage(str(path))
    image = SimpleITK.GetArrayFromImage(image_itk)

    d = image_itk.GetDirection()
    direction = np.round(np.array([d[8], d[4], d[0]]))
    spacing = np.asarray(image_itk.GetSpacing())[::-1]
    origin = np.asarray(image_itk.GetOrigin())[::-1]

    vtd = {
        "series_id": _get_file_title(path),
        "instances": list(range(1, image.shape[0] + 1)),

        "image_itk": image_itk if keep_itk_image else None,
        "image_zyx": image,

        "spacing_zyx": spacing,
        "direction_zyx": direction,
        "origin_zyx": origin,
    }
    return vtd


def read_npz(path: Union[str, Path]):
    """ Read an npy/npz format image.

    Args:
        path: npy/npz image file path.

    Returns:
        dict containing volume data and dicom tags.
    """
    vtd = dict(np.load(path))
    return vtd


def read_dicoms(
    paths: List[Union[str, Path]],
    keep_itk_image: bool = False,
) -> Dict[str, Any]:
    """ Read an itk format image.

    Args:
        paths: dicom file path list.
        keep_itk_image: whether to return original itk image.

    Returns:
        dict containing volume data and dicom tags.
    """
    pass
