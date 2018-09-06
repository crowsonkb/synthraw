"""Writes DNG files."""

import ctypes
from pathlib import Path

import numpy as np
from numpy.ctypeslib import ndpointer


lib_path = str(Path(__file__).resolve().parent / 'dng.so')
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
    def __init__(self, path):
        self.dng = lib.dng_open(str(path).encode())
        if not self.dng:
            raise DNGError('Error opening file')

    def set_matrix(self, matrix):
        matrix = np.float32(matrix).flatten()
        if len(matrix) != 9:
            raise ValueError('Matrix must contain 9 values')
        lib.dng_set_matrix(self.dng, matrix)

    def write_data(self, data):
        if data.dtype != np.uint16:
            raise TypeError('Data must be of type uint16')
        if data.ndim != 2:
            raise TypeError('Data must be 2-dimensional')
        lib.dng_write_data(self.dng, data, data.shape[1], data.shape[0])

    def close(self):
        lib.dng_close(self.dng)
