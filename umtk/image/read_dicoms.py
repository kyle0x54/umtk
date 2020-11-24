from functools import partial
import math
from pathlib import Path
from typing import Any, Dict, List, Union
import numpy as np
import pydicom
import SimpleITK
from .utils import isdicom
import umtk.error_handling as exc


def _read_dicom_headers(
        paths: List[Union[str, Path]]
) -> List[pydicom.dataset.FileDataset]:
    headers = []

    read = partial(pydicom.dcmread, stop_before_pixels=True, force=True)
    for path in paths:
        try:
            header = read(path)
        except Exception as e:
            raise exc.ReadDicomHeaderError(
                "Failed to read dicom header [{}]".format(path)
            )
        headers.append(header)

    return headers


def _sort_headers(headers: List[pydicom.dataset.FileDataset]) -> None:
    try:
        headers.sort(key=lambda x: float(x.ImagePositionPatient[2]))
    except Exception as e:
        raise exc.MissingImagePositionTagError(
            "Missing or incorrect image position tag, SeriesId=[{}]".
                format(headers[0].SeriesInstanceUID)
        )


def _get_series_id(headers: List[pydicom.dataset.FileDataset]) -> str:
    series_ids = set()

    for header in headers:
        try:
            series_ids.add(header.SeriesInstanceUID)
        except Exception as e:
            raise exc.MissingSeriesUidTagError(
                "Failed to get series id [{}]".format(header.filename)
            )

    if len(series_ids) != 1:
        raise exc.MultipleInputSeriesError(
            "Unsupported multiple series, num-series=[{}], series list={}".
                format(len(series_ids), series_ids)
        )

    return series_ids.pop()


def _get_instance_numbers(
    headers: List[pydicom.dataset.FileDataset],
    allow_missing_slices: bool,
) -> List[int]:
    numbers = []

    for header in headers:
        try:
            number = int(header.InstanceNumber)
        except Exception as e:
            raise exc.MissingInstanceNumberTagError(
                "Failed to get instance number [{}]".format(header.filename)
            )
        numbers.append(number)

    if not allow_missing_slices:
        start = min(numbers)
        ref_number_set = set(range(start, start + len(numbers)))
        missing = ref_number_set - set(numbers)
        if len(missing) != 0:
            raise exc.InconsistentInstanceNumberError(
                "Inconsistant Instance number, SeriesId=[{}], "
                "num-missing=[{}], Missing list={}".format(
                    headers[0].SeriesInstanceUID, len(missing), missing
                )
            )

    return numbers


def _get_pixel_spacing(
    headers: List[pydicom.dataset.FileDataset],
    allow_missing_slices: bool
) -> np.ndarray:
    try:
        spacing_xy = headers[0].PixelSpacing
    except Exception as e:
        raise exc.MissingPixelSpacingTagError(
            "Failed to get xy-spacing [{}]".format(headers[0].filename)
        )
    spacing_x, spacing_y = float(spacing_xy[0]), float(spacing_xy[1])

    spacing_zs = [
        float("%.2f" % (headers[i+1].ImagePositionPatient[2] -
                  headers[i].ImagePositionPatient[2]))
        for i in range(len(headers) - 1)
    ]

    spacing_zs, unique_counts = np.unique(spacing_zs, return_counts=True)
    if not allow_missing_slices:
        if len(spacing_zs) != 1:
            raise exc.InconsistentZPixelSpacingError(
                "Inconsistent z-spacing, SeriesId=[{}], "
                "Num-unique-zspacing=[{}], zspacing list={}".format(
                    headers[0].SeriesInstanceUID, len(spacing_zs), spacing_zs
                )
            )
        # TODO: check consistency between z-spacing and image-position?

    spacing_z = spacing_zs[unique_counts.argmax()]

    if math.isclose(spacing_z, 0.0):
        raise exc.IncorrectZPixelSpacingError(
            "Incorrect z-spacing, SeriesId=[{}], z-spacing=[{}], ".format(
                headers[0].SeriesInstanceUID, spacing_z
            )
        )

    return np.array([spacing_z, spacing_y, spacing_x])


def _get_origin(
    headers: List[pydicom.dataset.FileDataset]
) -> np.ndarray:
    origin_zyx = list(reversed(headers[0].ImagePositionPatient))
    return np.array([float(x) for x in origin_zyx])


def _get_direction(
    headers: List[pydicom.dataset.FileDataset]
) -> np.ndarray:
    try:
        d = headers[0].ImageOrientationPatient
        x = int(round(float(d[0])))
        y = int(round(float(d[4])))
    except Exception as e:
        x, y = 1, 1

    return np.array([1, y, x])


def read_dicoms(
    paths: List[Union[str, Path]],
    min_num_slices: int = 20,
    allow_missing_layers: bool = False
) -> Dict[str, Any]:
    """ Read an itk format image.

    Args:
        paths: dicom file path list.
        min_num_slices: minimum number of instances allowed.
        allow_missing_layers: whether to allow input containing
            missing layers.

    Returns:
        dict containing volume data and dicom tags.

    N.B.
        Mandatory tags:
            - SeriesInstanceUid
            - InstanceNumber
            - ImagePosition
            - PixelSpacing
        Optional tags:
            - ImageOrientation [Default=(1, 1, 1)]
    """
    assert isinstance(paths, (list, tuple)) and len(paths) != 0

    # dicom validation
    paths = [path for path in paths if isdicom(path)]

    # read dicom headers
    headers = _read_dicom_headers(paths)
    series_id = _get_series_id(headers)  # make sure dicom has series id
    _sort_headers(headers)
    instance_numbers = _get_instance_numbers(headers, allow_missing_layers)

    spacing_zyx = _get_pixel_spacing(headers, allow_missing_layers)
    origin_zyx = _get_origin(headers)
    direction_zyx = _get_direction(headers)

    # validation
    if len(paths) < min_num_slices:
        raise exc.NotEnoughSlicesError(
            "Not enough slices, SeriesId={}, Num-slices=[{}]".
                format(series_id, len(paths))
        )

    # load image data
    try:
        img_itk = SimpleITK.ReadImage([header.filename for header in headers])
        img_zyx = SimpleITK.GetArrayFromImage(img_itk)
    except Exception as e:
        raise exc.ReadDicomDataError(
            "Failed to read dicom data, SeriesId=[{}]".format(series_id)
        )

    return {
        "series_id": series_id,
        "instances": instance_numbers,
        "sorted_paths": [header.filename for header in headers],

        "image_itk": img_itk,
        "image_zyx": img_zyx,

        "spacing_zyx": spacing_zyx,
        "direction_zyx": direction_zyx,
        "origin_zyx": origin_zyx,
    }
