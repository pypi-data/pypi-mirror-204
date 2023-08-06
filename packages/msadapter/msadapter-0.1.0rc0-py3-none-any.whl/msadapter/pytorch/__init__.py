#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Register MSAdapter Tensor/Parameter to MindSpore, it should be executed at the top of all.
from msadapter.pytorch._register import *
from msadapter.pytorch.common import *
from msadapter.pytorch.tensor import *
from msadapter.pytorch import nn
from msadapter.pytorch import optim
from msadapter.pytorch.functional import *
from msadapter.pytorch.utils import data
from msadapter.pytorch._ref import *
from msadapter.pytorch import cuda
from msadapter.pytorch.conflict_functional import *
import msadapter.pytorch.fft as fft
from msadapter.pytorch import autograd
from msadapter.pytorch.package_info import __version__, VERSION, version
from msadapter.pytorch.random import *
from msadapter.pytorch.storage import *
from msadapter.pytorch.serialization import *
import msadapter.pytorch.linalg as linalg
from msadapter.pytorch.linalg import lu_solve

def _assert(condition, message):
    assert condition, message

def is_tensor(obj):
    r"""Returns True if `obj` is a msadapter.pytorch tensor.

    Note that this function is simply doing ``isinstance(obj, Tensor)``.
    Using that ``isinstance`` check is better for typechecking with mypy,
    and more explicit - so it's recommended to use that instead of
    ``is_tensor``.
    """
    return isinstance(obj, Tensor)

def is_floating_point(obj):
    if not is_tensor(obj):
        raise TypeError("is_floating_point(): argument 'input' (position 1) must be Tensor, not {}.".format(type(obj)))

    return obj._dtype in (mstype.float16, mstype.float32, mstype.float64)

class Size(tuple):
    def __new__(cls, shape):
        if isinstance(shape, Tensor):
            _shape = shape.tolist()
        else:
            _shape = shape
        if not isinstance(_shape, (tuple, list)):
            raise TypeError("{} object is not supportted.".format(type(shape)))

        return tuple.__new__(Size, _shape)
