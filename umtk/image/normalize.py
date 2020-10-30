import numpy as np


def normalize_grayscale(src: np.ndarray):
    """ Rescale image intensity.

    Rescale an grayscale image's intensity range to [0.0, 1.0].

    Args:
        src (ndarray): image to be intensity rescaled.

    Return:
        (ndarray of type np.float32): intensity rescaled image.
    """
    epsilon = 0.00001

    src_float = src.astype(np.float32)

    min_val, max_val = np.min(src_float), np.max(src_float)
    if max_val - min_val < epsilon:
        max_val += epsilon

    dst = (src_float - min_val) / (max_val - min_val)
    return dst


def imadjust_grayscale(
    im: np.ndarray,
    low_pct: float = 0.01,
    high_pct: float = 0.99,
):
    """ Increase contrast of a grayscale image.

    This function maps the intensity values in I to new values in J such that
    values between low_in and high_in map to values between 0 and 1.

    Args:
        im (np.ndarray): image to be enhanced.
        low_pct (float): low bound.
        high_pct (float): high bound.

    Return:
        (ndarray of type np.float32): the enhanced image.
    """
    assert 0.0 <= low_pct < high_pct <= 1.0

    low_loc = int(round((im.size - 1) * low_pct))
    high_loc = int(round((im.size - 1) * high_pct))

    im_flat = im.flatten()
    low_thr = im_flat[np.argpartition(im_flat, low_loc)[low_loc]]
    high_thr = im_flat[np.argpartition(im_flat, high_loc)[high_loc]]
    return normalize_grayscale(np.clip(im, a_min=low_thr, a_max=high_thr))
