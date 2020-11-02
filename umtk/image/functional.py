import numpy as np


def gamma_transform(img: np.ndarray, gamma: float) -> np.ndarray:
    img = np.power(img, gamma)
    return img
