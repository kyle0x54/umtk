import numpy as np
import torch
import torch.nn.functional as F


def zflip(img):
    return np.ascontiguousarray(img[::-1, :, :])


def yflip(img):
    return np.ascontiguousarray(img[:, ::-1, :])


def xflip(img):
    return np.ascontiguousarray(img[:, :, ::-1])


def resize(src, depth, height, width, device="cpu"):
    """ Resize an image to the given size.

    Args:
        img (ndarray): the given image.
        depth (int): target image depth in pixel.
        height (int): target image height in pixel.
        width (int): target image width in pixel.
        device (int): computation device, support "cpu" and "cuda".
            e.g. "cpu", "cuda", "cuda:0", "cuda:1"

    Returns:
        (ndarray): the resized image.
    """
    t_img = torch.from_numpy(src)
    t_img = t_img.unsqueeze(0).unsqueeze(0)
    t_img.to(device)
    t_img = F.interpolate(t_img, size=(depth, height, width), mode="trilinear")
    dst = t_img.cpu().numpy()[0, 0, ...]
    return dst


def crop(img, z, y, x, d, h, w):
    return img[z:z+d, y:y+h, x:x+w]


def center_crop(img, crop_depth, crop_height, crop_width):
    """ Crop the central part of an image.

    Args:
        img (ndarray): image to be cropped.
        crop_depth (int): depth of the crop.
        crop_height (int): height of the crop.
        crop_width (int): width of the crop.

    Return:
        (ndarray): the cropped image.
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
    x1, y1, x2, y2, z1, z2 = get_center_crop_coords(
        depth, height, width,
        crop_depth, crop_height, crop_width
    )
    return img[z1:z2, y1:y2, x1:x2]
