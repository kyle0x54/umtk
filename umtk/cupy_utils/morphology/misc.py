import cupy
from cupyx.scipy.ndimage import label


def _check_dtype_supported(ar):
    if not (ar.dtype == bool or cupy.issubdtype(ar.dtype, cupy.integer)):
        raise TypeError(
            "Only bool or integer types are supported. Got %s." % ar.dtype
        )


def remove_small_objects_gpu(
    mask: cupy.ndarray,
    min_size: int
) -> None:
    """ See scikit-image remove_small_objects()

    N.B.
        Input array can be a binary mask (bool type) or
        labeled mask (int type).
        This is a inplace operation.
    """
    _check_dtype_supported(mask)

    ccs = label(mask) if mask.dtype == bool else mask
    component_sizes = cupy.bincount(ccs.ravel())
    too_small = component_sizes < min_size
    too_small_mask = too_small[ccs]
    mask[too_small_mask] = 0


def remove_small_holes_gpu(
    mask: cupy.ndarray,
    area_threshold: int,
) -> None:
    """ See scikit-image remove_small_holes()

    N.B.
        Input array must be a binary mask (bool type) or
        labeled mask (int type).
        This is a inplace operation.
    """
    _check_dtype_supported(mask)

    cupy.logical_not(mask, out=mask)
    remove_small_objects_gpu(mask, area_threshold)
    cupy.logical_not(mask, out=mask)
