#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
# from functools import lru_cache
import mindspore as ms
from mindspore import context
from mindspore.ops.primitive import _primexpr


_GLOBAL_LRU_CACHE_SIZE = 4
_GLOBAL_LRU_CACHE_SIZE_NN = 256


def unsupported_attr(attr):
    """
    To mark the attribute that is not currently supported.
    """
    return attr

@_primexpr
def pynative_mode_condition():
    return context.get_context("mode") == context.PYNATIVE_MODE

@_primexpr
def graph_mode_condition():
    return context.get_context("mode") == context.GRAPH_MODE

@_primexpr
def get_backend():
    return context.get_context("device_target")

@_primexpr
def is_under_gpu_context():
    return get_backend() == 'GPU'

@_primexpr
def is_under_ascend_context():
    return get_backend() == 'Ascend'

@_primexpr
def is_under_cpu_context():
    return get_backend() == 'CPU'

@_primexpr
def ascend_raise_implement_error(func):
    if is_under_ascend_context():
        raise NotImplementedError(func + " currently not support on Ascend")

@_primexpr
def set_name_tuple(name):
    return collections.namedtuple(name, 'values, indices')

_AscendGenernalConvertDict = {
    ms.float64: ms.float32,
    ms.int8: ms.float16,
    ms.int16: ms.float16,
    ms.int32: ms.float32,
    ms.int64: ms.float32,
    ms.uint8: ms.float16,
    ms.bool_: ms.float16,
    ms.double: ms.float32,
}

def _ascend_tensor_general_cast(input, conver_dicts={}):
    """
    Example:
        >>> import msadapter.pytorch as torch
        >>> from msadapter.utils import _ascend_tensor_general_cast
        >>> a = torch.tensor(2)
        >>> print(a.dtype)
        Int64
        >>> b = _ascend_tensor_general_cast(a)
        >>> print(b.dtype)
        Float32
        >>> c = _ascend_tensor_general_cast(a, conver_dicts={torch.int64: torch.int32})
        >>> print(b.dtype)
        Int32
    """
    value = conver_dicts.get(input.dtype)
    if value:
        return input.astype(value)

    _to_dtype = _AscendGenernalConvertDict.get(input.dtype)
    if _to_dtype:
        return input.astype(_to_dtype)
    return input


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE)
def _infer_size(shape, numel):
    if len(shape) == 1 and isinstance(shape[0], tuple):
        shape = shape[0]

    dim = None
    newsize = 1
    for i, d in enumerate(shape):
        if d == -1:
            if dim is not None:
                raise RuntimeError("only one dimension can be inferred")
            dim = i
        elif d >= 0:
            newsize *= d
        else:
            raise RuntimeError(f"invalid shape dimension {d}")

    if not (numel == newsize or (dim is not None and newsize > 0 and numel % newsize == 0)):
        raise RuntimeError(f"shape '{list(shape)}' is invalid for input of size {numel}")

    if dim is not None:
        if newsize == 0:
            raise RuntimeError(f"cannot reshape tensor fo 0 elements into shape {shape} because the "
                               "unspecified dimension size -1 can be any value and is ambiguous.")
        shape = list(shape)
        shape[dim] = numel // newsize
    return tuple(shape)