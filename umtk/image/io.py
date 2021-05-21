import os
from pathlib import Path
from typing import Any, Dict, Union
import numpy as np
import h5py
import SimpleITK
import pydicom
import umtk.error_handling as exc


def _get_file_title(path: Union[str, Path]):
    file_title = os.path.splitext(os.path.basename(path))[0]
    if path.endswith(".nii.gz"):
        return os.path.splitext(file_title)[0]
    else:
        return file_title


def read_itk(
        path: Union[str, Path],
) -> Dict[str, Any]:
    """ Read an itk format image.

    Args:
        path: itk image file path.

    Returns:
        dict containing volume data and dicom tags.
    """
    try:
        image_itk = SimpleITK.ReadImage(str(path))
        image = SimpleITK.GetArrayFromImage(image_itk)
    except Exception as e:
        raise exc.ReadDicomDataError(
            "Failed to read dicom data, file path=[{}]".format(path)
        )

    d = image_itk.GetDirection()
    direction = np.round(np.array([d[8], d[4], d[0]]))
    spacing = np.asarray(image_itk.GetSpacing())[::-1]
    origin = np.asarray(image_itk.GetOrigin())[::-1]

    vtd = {
        "series_id": _get_file_title(path),
        "instances": list(range(1, image.shape[0] + 1)),

        "image_itk": image_itk,
        "image_zyx": image,

        "spacing_zyx": spacing,
        "direction_zyx": direction,
        "origin_zyx": origin,
    }
    return vtd


def read_npz(path: Union[str, Path]):
    """ Read a npy/npz format image.

    Args:
        path: npy/npz image file path.

    Returns:
        dict containing volume data and dicom tags.
    """
    vtd = dict(np.load(path))
    return vtd


PLACEHOLDER = np.NAN


def __array_fill_in(unequal_length_arr):
    """ Fill arrays of different shapes to uniform length

    Args:
        unequal_length_arr: [arr1, arr2, arr3, ...], the shape of the array can be unequal, but the depth must be equal

    Returns:

    """
    unequal_length_arr = list(unequal_length_arr)

    shapes = [np.shape(arr) if len(arr) > 0 else [] for arr in unequal_length_arr]
    depths = np.array([len(shape) for shape in shapes])
    shapes = np.array(shapes)[depths != 0]
    depths = np.unique(depths[depths != 0])
    assert len(depths) <= 1, 'The depth of the array must be equal.'

    if len(shapes) != 0:
        shapes = np.array(list(shapes))
        shape_max = np.max(shapes, axis=0)
    else:
        return unequal_length_arr

    equal_length_arr = []
    for arr in unequal_length_arr:
        arr_fill = np.ones(shape_max) * PLACEHOLDER
        if len(arr) != 0:
            arr_fill[np.where(arr)] = np.array(arr).flatten()
        equal_length_arr.append(arr_fill)
    return np.array(equal_length_arr)


def _generate_h5_file(f, key, data, compression='gzip'):
    if not isinstance(data, dict):
        if isinstance(data, list):
            data = np.array(data)
        if isinstance(data, np.ndarray):
            if data.dtype.hasobject:
                # 将变长list，填补为等长数组. list中矩阵的深度必须一致
                data = __array_fill_in(data)
            f.create_dataset(key, data=data, compression=compression)
        else:
            if isinstance(data, (np.str_, pydicom.uid.UID)):
                data = str(data)
            f[key] = data
    else:
        group = f.create_group(key)
        for k, v in data.items():
            if v is not None:
                _generate_h5_file(group, k, v)


def _get_h5_dict(f, new_dict=None):
    if new_dict is None:
        new_dict = {}
    for k, v in f.items():
        if type(v) is not h5py.Group:
            new_dict[k] = v.value
        else:
            new_dict[k] = _get_h5_dict(v)
    return new_dict


def read_h5(data_path: Union[str, Path]) -> dict:
    """ Read an h5 format image as dict.

    Args:
        data_path: h5 image file path.

    Returns:
        dict containing volume data, dicom tags and annotations.

    """
    with h5py.File(data_path, 'r') as f:
        return _get_h5_dict(f)


def write_h5(data_path: Union[str, Path], data_dict: dict, compression='gzip'):
    """ write dict as an h5 format image.

    Args:
        data_path: h5 image file path.
        data_dict: dict containing volume data, dicom tags and annotations.
        compression: compression type.

    Returns:

    """
    with h5py.File(data_path, 'w') as f:
        for k, v in data_dict.items():
            _generate_h5_file(f, k, v, compression)
