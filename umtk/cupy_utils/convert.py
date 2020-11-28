import cupy
from cupy.core.dlpack import toDlpack, fromDlpack
import numpy as np
import torch
from torch.utils.dlpack import to_dlpack, from_dlpack


def tensor2cupy_gpu(torch_tensor: torch.Tensor) -> cupy.ndarray:
    """ Convert a pytorch tensor to cupy array."""
    with cupy.cuda.Device(torch_tensor.device.index):
        cupy_array = fromDlpack(to_dlpack(torch_tensor))
        return cupy_array


def cupy2tensor_gpu(cupy_array: cupy.ndarray) -> torch.Tensor:
    """ Convert a cupy array to pytorch tensor."""
    return from_dlpack(toDlpack(cupy_array))


def tensor2numpy(torch_tensor: torch.Tensor) -> np.ndarray:
    """ Convert a pytorch tensor to numpy array."""
    return torch_tensor.cpu().numpy()


def cupy2numpy(cupy_array: cupy.ndarray) -> np.ndarray:
    """ Convert a cupy array to numpy array."""
    return cupy.asnumpy(cupy_array)
