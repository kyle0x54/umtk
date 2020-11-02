from nibabel.viewers import OrthoSlicer3D
import numpy as np
import umtk


def show_mpr(img: np.ndarray) -> None:
    """ Show Multi-Planer Reconstruction of a volume.

    N.B.
        Image should be re-oriented before calling this function.
        Refer to read_itk on how to standardize image orientation.
    """
    img_trans = umtk.zflip(umtk.yflip(np.swapaxes(img, 0, 2)))
    OrthoSlicer3D(img_trans).show()
