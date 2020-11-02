import cupy


def remove_small_objects_gpu(
    mask: cupy.ndarray,
    min_size: int
) -> None:
    """ See scikit-image remove_small_objects()

    N.B.
        Input array must be a labeled mask.
        This is a inplace operation.
    """
    component_sizes = cupy.bincount(mask.ravel())
    too_small = component_sizes < min_size
    too_small_mask = too_small[mask]
    mask[too_small_mask] = 0
