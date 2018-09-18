"""Writes DNG files."""

import ctypes
from pathlib import Path
import platform
from typing import Union

import numpy as np
from numpy.ctypeslib import ndpointer

from .types import SizedIterable

lib_path = str(Path(__file__).resolve().parent / 'dng.so')
if platform.system() == 'Linux':
    ctypes.CDLL('libtiff.so', mode=ctypes.RTLD_GLOBAL)
    lib = ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
else:
    lib = ctypes.cdll.LoadLibrary(lib_path)

lib.dng_open.argtypes = [ctypes.c_char_p]
lib.dng_open.restype = ctypes.c_void_p

lib.dng_set_matrix.argtypes = [ctypes.c_void_p,
                               ndpointer(ctypes.c_float, flags='C_CONTIGUOUS')]

lib.dng_write_data.argtypes = [ctypes.c_void_p,
                               ndpointer(ctypes.c_uint16, flags='C_CONTIGUOUS'),
                               ctypes.c_size_t,
                               ctypes.c_size_t]

lib.dng_close.argtypes = [ctypes.c_void_p]


class DNGError(Exception):
    """Indicates an error while operating on a DNG file."""


class DNG:
    """A DNG file."""
    def __init__(self, path: Union[Path, str]) -> None:
        self.dng = lib.dng_open(str(path).encode())
        if not self.dng:
            raise DNGError('Error opening file')

    def set_matrix(self, matrix: SizedIterable) -> None:
        """Sets the XYZ to RGB color conversion matrix."""
        matrix = np.float32(matrix).flatten()
        if len(matrix) != 9:
            raise ValueError('Matrix must contain 9 values')
        lib.dng_set_matrix(self.dng, matrix)

    def write_data(self, data: np.ndarray) -> None:
        """Writes a numpy array (dtype uint16) to the DNG file."""
        if data.dtype != np.uint16:
            raise ValueError('Data must be of type uint16')
        if data.ndim != 2:
            raise ValueError('Data must be 2-dimensional')
        lib.dng_write_data(self.dng, data, data.shape[1], data.shape[0])

    def close(self) -> None:
        """Closes the DNG file."""
        lib.dng_close(self.dng)
