from pycohere.lib.cohlib import cohlib
import cupy as cp
import cupyx as cpx
import math
import numpy as np
from cupyx.scipy import ndimage


class cplib(cohlib):

    def set_device(dev_id):
        cp.cuda.Device(dev_id).use()

    def set_backend(proc):
        pass

    def to_numpy(arr):
        return cp.asnumpy(arr).T

    def from_numpy(arr):
        return cp.array(arr.T)

    def dtype(arr):
        return arr.dtype

    def size(arr):
        return arr.size

    def random(shape, **kwargs):
        import time
        import os

        seed = np.array([time.time()* 10000 * os.getpid(), os.getpid()])
        rs = cp.random.RandomState(seed=seed)
        return cp.random.random(shape, dtype=cp.float32) + 1j * cp.random.random(shape, dtype=cp.float32)

    def fftshift(arr):
        return cp.fft.fftshift(arr)

    def ifftshift(arr):
        return cp.fft.fftshift(arr)

    def shift(arr, sft):
        sft = [int(s) for s in sft]
        return cp.roll(arr, sft)

    def fft(arr):
        return cp.fft.fftn(arr)

    def ifft(arr):
        return cp.fft.ifftn(arr)

    def fftconvolve(arr1, arr2):
        #return cpx.scipy.signal.convolve(arr1, arr2)
        return ndimage.convolve(arr1, arr2)

    def where(cond, x, y):
        return cp.where(cond, x, y)

    def dims(arr):
        # get array dimensions
        return arr.shape

    def absolute(arr):
        return cp.absolute(arr)

    def sqrt(arr):
        return cp.sqrt(arr)

    def square(arr):
        return cp.square(arr)

    def sum(arr):
        return cp.sum(arr)

    def real(arr):
        return cp.real(arr)

    def imag(arr):
        return cp.imag(arr)

    def max(arr):
        return cp.amax(arr)

    def print(arr, **kwargs):
        print(arr)

    def arctan2(arr1, arr2):
        return cp.arctan2(arr1, arr2)

    def flip(arr, axis=None):
        return cp.flip(arr, axis)

    def full(shape, fill_value, **kwargs):
        return cp.full(shape, fill_value)

    def gaussian(shape, sigmas, **kwargs):
        inarr = cp.full(shape, 1.0)
        return ndimage.gaussian_filter(inarr, sigmas)

    def center_of_mass(inarr):
        return cpx.scipy.ndimage.center_of_mass(cp.absolute(inarr))
