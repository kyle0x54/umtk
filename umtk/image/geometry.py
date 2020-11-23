from typing import Tuple
import numpy as np
import torch
import torch.nn.functional as F


def zflip(img: np.ndarray) -> np.ndarray:
    return np.ascontiguousarray(img[::-1, :, :])


def yflip(img: np.ndarray) -> np.ndarray:
    return np.ascontiguousarray(img[:, ::-1, :])


def xflip(img: np.ndarray) -> np.ndarray:
    return np.ascontiguousarray(img[:, :, ::-1])


def resize(
    src: np.ndarray,
    size: Tuple,
    to_float: bool = False,
    mode: str = "trilinear"
) -> np.ndarray:
    """ Resize an image to the given size.

    Args:
        src: the given image.
        size: image size (in pixel) in DHW order.
        device: computation device, support "cpu" and "cuda".
            e.g. "cpu", "cuda", "cuda:0", "cuda:1".
        to_float: whether to convert the output image to float32.
        mode: interpolation mode, support "nearest" and "trilinear".

    Returns:
        the resized image.
    """
    assert mode in ("nearest", "trilinear")
    tensor = torch.from_numpy(src.astype(np.float32))
    tensor = tensor.unsqueeze(0).unsqueeze(0)
    tensor = F.interpolate(
        tensor,
        size=size,
        mode=mode,
        align_corners=None if mode == "nearest" else False
    )
    dst = tensor.numpy()[0, 0, ...]
    return dst if to_float else dst.astype(src.dtype)


def crop(
    img: np.ndarray,
    start_point: Tuple[int, int, int],
    crop_size: Tuple[int, int, int]
) -> np.ndarray:
    """ Crop a part of the input image.

    Args:
        img: image to be cropped.
        start_point: start point of the crop.
        crop_size: size of the crop.

    Returns:

    """
    z, y, x = start_point
    d, h, w = crop_size
    return img[z:z+d, y:y+h, x:x+w]


def center_crop(
    img: np.ndarray,
    crop_size: Tuple[int, int, int]
) -> np.ndarray:
    """ Crop the central part of an image.

    Args:
        img: image to be cropped.
        crop_size: size of cropped image.

    Return:
        the cropped image.
    """
    def get_center_crop_coords(d, h, w, cd, ch, cw):
        z1 = (d - cd) // 2
        z2 = z1 + cd
        y1 = (h - ch) // 2
        y2 = y1 + ch
        x1 = (w - cw) // 2
        x2 = x1 + cw
        return x1, y1, x2, y2, z1, z2

    depth, height, width = img.shape
    crop_depth, crop_height, crop_width = crop_size
    x1, y1, x2, y2, z1, z2 = get_center_crop_coords(
        depth, height, width,
        crop_depth, crop_height, crop_width
    )
    return img[z1:z2, y1:y2, x1:x2]
