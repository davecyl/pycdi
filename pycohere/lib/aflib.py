from pycohere.lib.cohlib import cohlib
import arrayfire as af
import math
import numpy as np


class aflib(cohlib):
    def array(obj):
        print('not implemented')

    def dot(arr1, arr2):
        print('not implemented')

    def set_device(dev_id):
        af.device.set_device(dev_id)

    def set_backend(proc):
        af.set_backend(proc)

    def to_numpy(arr):
        return arr.to_ndarray().T

    def from_numpy(arr):
        return af.np_to_af_array(arr.T)

    def save(filename, arr):
        np.save(filename, arr.to_ndarray().T)

    def load(filename):
        arr = np.load(filename)
        return af.np_to_af_array(arr.T)

    def dtype(arr):
        return arr.dtype()

    def size(arr):
        return arr.elements()

    def hasnan(arr):
        return af.any_true(af.isnan(arr))

    def random(shape, **kwargs):
        import time
        import os

        dims = [None, None, None, None]
        for i in range(len(shape)):
            dims[i] = shape[i]

        eng = af.random.Random_Engine(engine_type=af.RANDOM_ENGINE.DEFAULT,
                                      seed=int(time.time() * 1000000) * os.getpid() + os.getpid())
        return af.random.randn(dims[0], dims[1], dims[2], dims[3], dtype=af.Dtype.c32, engine=eng)

    def fftshift(arr):
        raise NotImplementedError

    def ifftshift(arr):
        raise NotImplementedError

    def shift(arr, sft):
        raise NotImplementedError

    def fft(arr):
        raise NotImplementedError

    def ifft(arr):
        raise NotImplementedError

    def fftconvolve(arr1, arr2):
        return af.fft_convolve(arr1, arr2)

    def where(cond, x, y):
        return af.select(cond, x, y)

    def dims(arr):
        # get array dimensions
        return arr.dims()

    def absolute(arr):
        return af.abs(arr)

    def sqrt(arr):
        return af.sqrt(arr)

    def square(arr):
        return af.pow(arr, 2)

    def sum(arr, axis=None):
        return af.sum(arr)

    def real(arr):
        return af.real(arr)

    def imag(arr):
        return af.imag(arr)

    def amax(arr):
        return af.max(arr)

    def maximum(arr1, arr2):
        return af.select((arr1 > arr2), arr1, arr2)

    def argmax(arr, axis=None):
        val, idx = af.imax(arr, axis)
        return idx

    def unravel_index(indices, shape):
        return indices

    def ceil(arr):
        return af.ceil(arr)

    def fix(arr):
        return af.trunc(arr)

    def round(val):
        print ('not implemented')

    def print(arr, **kwargs):
        af.display(arr)

    def angle(arr):
        return af.atan2(af.imag(arr), af.real(arr))

    def flip(arr, axis=None):
        if axis is None:
            raise NotImplementedError
        else:
            return af.flip(arr, axis)

    def tile(arr, rep):
        print ('not implemented')

    def full(shape, fill_value, **kwargs):
        dims = [None, None, None, None]
        for i in range(len(shape)):
            dims[i] = shape[i]
        return af.constant(fill_value, dims[0], dims[1], dims[2], dims[3])

    def gaussian(shape, sigmas, **kwargs):
        raise NotImplementedError

    def center_of_mass(inarr):
        arr = af.abs(inarr)
        normalizer = af.sum(arr)
        t_dims = list(arr.dims())
        mod_dims = [None, None, None, None]
        for i in range(len(t_dims)):
            mod_dims[i] = 1
        com = []

        for dim in range(len(t_dims)):
            # swap
            mod_dims[dim] = t_dims[dim]
            t_dims[dim] = 1
            grid = af.iota(mod_dims[0], mod_dims[1], mod_dims[2], mod_dims[3], tile_dims=t_dims)
    #        print(grid)
            com.append(af.sum(grid * arr) / normalizer)
            # swap back
            t_dims[dim] = mod_dims[dim]
            mod_dims[dim] = 1

        return com

    def meshgrid(*xi):
        print ('not implemented')

    def exp(arr):
        return af.exp(arr)

    def cong(arr):
        return af.conjg(arr)

    def save(file, arr):
        nparr = arr.to_ndarray().T
        np.save(file, nparr)


class aflib1(aflib):
    def fftshift(arr):
        return af.shift(arr, math.ceil(arr.dims()[0] / 2) - 1)

    def ifftshift(arr):
        return af.shift(arr, math.ceil(arr.dims()[0] / 2))

    def shift(arr, sft):
        return af.shift(arr, math.ceil(sft[0]))

    def fft(arr):
        return af.fft(arr)

    def ifft(arr):
        return af.ifft(arr)

    def flip(arr, axis=None):
        if axis is None:
            return af.flip(arr, 0)
        else:
            return af.flip(arr, axis)

    def gaussian(dims, sigmas, **kwargs):
        alpha = 1.0
        grid = af.constant(1.0, dims[0])
        multiplier = - 0.5 * alpha / pow(sigmas[0], 2)
        exponent = af.pow((af.range(dims[0], dim=0) - (dims[0] - 1) / 2.0), 2) * multiplier
        grid = grid * af.arith.exp(exponent)

        grid_tot = af.sum(grid, dim=0)
        grid_total = af.tile(grid_tot, dims[0])
        grid = grid / grid_total
        return grid

class aflib2(aflib):
    def fftshift(arr):
        return af.shift(arr, math.ceil(arr.dims()[0] / 2) - 1, math.ceil(arr.dims()[1] / 2) - 1)

    def ifftshift(arr):
        return af.shift(arr, math.ceil(arr.dims()[0] / 2), math.ceil(arr.dims()[1] / 2))

    def shift(arr, sft):
        return af.shift(arr, math.ceil(sft[0]), math.ceil(sft[1]))

    def fft(arr):
        return af.fft2(arr)

    def ifft(arr):
        return af.ifft2(arr)

    def flip(arr, axis=None):
        if axis is None:
            return af.flip(af.flip(arr, 0), 1)
        else:
            return af.flip(arr, axis)

    def gaussian(dims, sigmas, **kwargs):
        alpha = 1.0
        grid = af.constant(1.0, dims[0], dims[1])
        for i in range(len(sigmas)):
            multiplier = - 0.5 * alpha / pow(sigmas[i], 2)
            exponent = af.pow((af.range(dims[0], dims[1], dim=i) - (dims[i] - 1) / 2.0), 2) * multiplier
            grid = grid * af.arith.exp(exponent)

        grid_tot = af.sum(af.sum(grid, dim=0), dim=1)
        grid_total = af.tile(grid_tot, dims[0], dims[1])
        grid = grid / grid_total
        return grid


class aflib3(aflib):
    def fftshift(arr):
        return af.shift(arr, math.ceil(arr.dims()[0] / 2) - 1, math.ceil(arr.dims()[1] / 2) - 1,
                        math.ceil(arr.dims()[2] / 2) - 1)

    def ifftshift(arr):
        return af.shift(arr, math.ceil(arr.dims()[0] / 2), math.ceil(arr.dims()[1] / 2), math.ceil(arr.dims()[2] / 2))

    def shift(arr, sft):
        return af.shift(arr, math.ceil(sft[0]), math.ceil(sft[1]), math.ceil(sft[2]))

    def fft(arr):
        return af.fft3(arr)

    def ifft(arr):
        return af.ifft3(arr)

    def flip(arr, axis=None):
        if axis is None:
            return af.flip(af.flip(af.flip(arr, 0), 1), 2)
        else:
            return af.flip(arr, axis)

    def gaussian(dims, sigmas, **kwargs):
        alpha = 1.0
        grid = af.constant(1.0, dims[0], dims[1], dims[2])
        for i in range(len(sigmas)):
            multiplier = - 0.5 * alpha / pow(sigmas[i], 2)
            exponent = af.pow((af.range(dims[0], dims[1], dims[2], dim=i) - (dims[i] - 1) / 2.0), 2) * multiplier
            grid = grid * af.arith.exp(exponent)

        grid_tot = af.sum(af.sum(af.sum(grid, dim=0), dim=1), dim=2)
        grid_total = af.tile(grid_tot, dims[0], dims[1], dims[2])
        grid = grid / grid_total
        return grid

