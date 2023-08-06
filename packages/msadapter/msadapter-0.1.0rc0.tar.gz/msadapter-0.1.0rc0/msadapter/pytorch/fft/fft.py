#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import mindspore as ms
from msadapter.pytorch.tensor import cast_to_ms_tensor
from msadapter.pytorch.common._inner import _out_inplace_assign

def fft(input, n=None, dim=-1, norm=None, out=None):
    input = cast_to_ms_tensor(input)
    input = input.asnumpy()
    output = np.fft.fft(input, n, axis=dim, norm=norm)
    return _out_inplace_assign(out, ms.Tensor(output), "fft")


def rfft(input, n=None, dim=- 1, norm=None, *, out=None):
    input = cast_to_ms_tensor(input)
    input = input.asnumpy()
    output = np.fft.rfft(input, n, axis=dim, norm=norm)
    return _out_inplace_assign(out, ms.Tensor(output), "rfft")
