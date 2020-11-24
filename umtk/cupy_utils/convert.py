import cupy
import torch
from torch.utils.dlpack import to_dlpack


def tensor2cupy_gpu(
        torch_tensor: torch.Tensor
) -> cupy.ndarray:
    """ Convert a pytorch tensor to cupy_utils array."""
    with cupy.cuda.Device(torch_tensor.device.index):
        cupy_array = cupy.fromDlpack(to_dlpack(torch_tensor))
        return cupy_array
