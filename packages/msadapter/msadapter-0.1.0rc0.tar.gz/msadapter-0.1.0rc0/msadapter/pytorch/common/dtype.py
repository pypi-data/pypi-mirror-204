#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from mindspore import dtype as mstype


inf = float('inf')
nan = float('nan')

float = mstype.float32
double = mstype.float64
float16 = mstype.float16
# TODO: mindspore to support mstype.bfloat16
bfloat16 = mstype.float32
float32 = mstype.float32
float64 = mstype.float64
int8 = mstype.int8
int16 = mstype.int16
int32 = mstype.int32
int64 = mstype.int64
uint8 = mstype.uint8
bool_ = mstype.bool_
complex64 = mstype.complex64
complex128 = mstype.complex128
long = mstype.int64
cfloat = mstype.complex64
cdouble = mstype.complex128
half = mstype.half
short = mstype.short
int = mstype.int32
bool = mstype.bool_
char = mstype.uint8


all_int_type = (mstype.int8, mstype.int16, mstype.int32, mstype.int64, mstype.uint8, )


_TypeDict = {mstype.float16: np.float16,
             mstype.float32: np.float32,
             mstype.float64: np.float64,
             mstype.int8: np.int8,
             mstype.int16: np.int16,
             mstype.int32: np.int32,
             mstype.int64: np.int64,
             mstype.uint8: np.uint8}

class iinfo:
    def __init__(self, dtype):
        if dtype in (mstype.uint8, mstype.int8, mstype.int16, mstype.int32, mstype.int64):
            np_iinfo = np.iinfo(_TypeDict[dtype])
            self.bits = np_iinfo.bits
            self.max = np_iinfo.max
            self.min = np_iinfo.min
        else:
            raise ValueError("iinfo currently only supports torch.uint8/torch.int8/torch.int16/torch.int32/"
                             "torch.int64 as the input, but get a", dtype)

class finfo:
    def __init__(self, dtype):
        if dtype in (mstype.float16, mstype.float32, mstype.float64):
            np_finfo = np.finfo(_TypeDict[dtype])
            self.bits = np_finfo.bits
            self.eps = np_finfo.eps
            self.max = np_finfo.max
            self.min = np_finfo.min
            self.tiny = np_finfo.tiny
            # TODO: numpy vision >= 1.23
            # self.smallest_normal = np_finfo.smallest_normal
            self.resolution = np_finfo.resolution
        else:
            raise ValueError("finfo currently only supports torch.float16/torch.float32/"
                             "torch.float64 as the input, but get a", dtype)
