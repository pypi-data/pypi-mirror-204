#!/usr/bin/env python
# -*- coding: utf-8 -*-

from msadapter.pytorch.common.dtype import *
from msadapter.pytorch.common.device import *

# Variables with simple values, from math.py.
e = 2.718281828459045

pi = 3.141592653589793

tau = 6.28318530717958


__all__ = ["float", "double",
           "float16", "float32",
           "float64", "int8",
           "int16", "int32",
           "int64", "uint8",
           "bool_", "complex64",
           "complex128", "long",
           "bfloat16", "cfloat",
           "cdouble", "half",
           "short", "int",
           "bool", "iinfo",
           "finfo", "Device",
           "nan", "inf",
           "e", "pi", "tau",
]
