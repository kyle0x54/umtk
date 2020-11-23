import numpy as np


def normalize_mean_std(
    img: np.ndarray,
    mean: float,
    std: float
) -> np.ndarray:
    """ Normalize a tensor image with mean and standard deviation.

    Args:
        img (np.ndarray): image to be normalized.
        mean (float): mean.
        std (float): standard deviation.

    Returns:
        np.ndarray: normalized image.
    """
    mean = np.array(mean, dtype=np.float32)
    std = np.array(std, dtype=np.float32)

    denominator = np.reciprocal(std, dtype=np.float32)

    img = img.astype(np.float32)
    img -= mean
    img *= denominator

    return img


def normalize_adaptive(src: np.ndarray) -> np.ndarray:
    """ Rescale image intensity.

    Rescale an grayscale image's intensity range to [0.0, 1.0].

    Args:
        src (np.ndarray): image to be intensity rescaled.

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


def normalize_fixed(
    src: np.ndarray,
    in_min: float,
    in_max: float
) -> np.ndarray:
    """ Rescale image intensity.

    Rescale an grayscale image's intensity range from [min_, max_] to
    [0.0, 1.0]. Intensity value out of [min_, max_] will be clipped.

    Args:
        src (np.ndarray): image to be intensity rescaled.
        in_min (float): input min value for intensity mapping
        in_max (float): input max value for intensity mapping

    Return:
        (ndarray of type np.float32): intensity rescaled image.
    """
    assert in_min < in_max

    src = src.clip(in_min, in_max)
    src_float = src.astype(np.float32)

    a = 1. / (in_max - in_min)
    b = -in_min / (in_max - in_min)
    dst = a * src_float + b
    return dst


def imadjust(
    src: np.ndarray,
    low_pct: float = 1.,
    high_pct: float = 99.,
) -> np.ndarray:
    """ Increase image contrast.

    This function maps the intensity values in I to new values in J such that
    values between low_in and high_in map to values between 0 and 1.

    Args:
        src (np.ndarray): image to be enhanced.
        low_pct (float): low bound.
        high_pct (float): high bound.

    Return:
        (ndarray of type np.float32): the enhanced image.
    """
    low_thr, high_thr = np.percentile(src, (low_pct, high_pct))
    dst = np.clip(src, a_min=low_thr, a_max=high_thr)
    dst = normalize_adaptive(dst)
    return dst
