#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import mindspore as ms
import mindspore.scipy.linalg as ms_linalg
from mindspore import vmap
from mindspore.ops._primitive_cache import _get_cache_prim
from msadapter.pytorch.common._inner import _out_inplace_assign
from msadapter.utils import unsupported_attr, ascend_raise_implement_error, pynative_mode_condition
from msadapter.pytorch.tensor import cast_to_ms_tensor, cast_to_adapter_tensor
from msadapter.pytorch._register_numpy_primitive import NumpyFullLstsq


def eigh(A, UPLO='L', *, out=None): # TODO use numpy api now
    A = A.numpy()
    l, q = np.linalg.eigh(A, UPLO=UPLO)
    return _out_inplace_assign(out, (ms.Tensor(l), ms.Tensor(q)), "eigh")


def solve(A, B, *, left=True, out=None):# TODO use numpy api now
    unsupported_attr(left)
    A = A.numpy()
    B = B.numpy()
    output = np.linalg.solve(A, B)
    return _out_inplace_assign(out, ms.Tensor(output), "solve")

def eig(A, *, out=None):
    input = cast_to_ms_tensor(A)
    output = _get_cache_prim(ms.ops.Eig)(compute_v=True)(input)
    return _out_inplace_assign(out, output, "eig")

def slogdet(A, *, out=None):
    A = cast_to_ms_tensor(A)
    sign, output = ms.ops.slogdet(A)
    return _out_inplace_assign(out, (sign, output), "slogdet")

def det(A, *, out=None):
    A = cast_to_ms_tensor(A)
    output = ms.ops.det(A)
    return _out_inplace_assign(out, output, "det")

def cholesky(A, *, upper=False, out=None):
    # TODO: ms.ops.cholesky to support complex type
    A = cast_to_ms_tensor(A)
    output = ms.ops.cholesky(A, upper)
    return _out_inplace_assign(out, output, "cholesky")

def inv(A, *, out=None):
    A = cast_to_ms_tensor(A)
    output = ms.ops.inverse(A)
    return _out_inplace_assign(out, output, "inv")

def matmul(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.matmul(input, other)
    return _out_inplace_assign(out, output, "matmul")

def diagonal(A, *, offset=0, dim1=-2, dim2=-1):
    A = cast_to_ms_tensor(A)
    output = ms.ops.diagonal(A, offset=offset, dim1=dim1, dim2=dim2)
    return cast_to_adapter_tensor(output)

def multi_dot(tensors, *, out=None):
    input = cast_to_ms_tensor(tensors)
    output = ms.numpy.multi_dot(input)
    return _out_inplace_assign(out, output, "multi_dot")

def householder_product(A, tau, *, out=None):
    input = cast_to_ms_tensor(A)
    input2 = cast_to_ms_tensor(tau)
    output = ms.ops.orgqr(input, input2)
    return _out_inplace_assign(out, output, "householder_product")

def lu(A, *, pivot=True, out=None):
    #TODO: Currently not supported on Ascend
    ascend_raise_implement_error("lu")
    A = cast_to_ms_tensor(A)
    if A.ndim == 2:
        p, l, u = ms_linalg.lu(A, permute_l=False, overwrite_a=False, check_finite=True)
    else:
        p, l, u = vmap(ms_linalg.lu, in_axes= (0, None, None, None))(A, False, False, True)
    p = p.astype(A.dtype)
    if pivot:
        output = (p, l, u)
    else:
        output = (l, u)
    return _out_inplace_assign(out, output, "lu")


def lu_factor(A, *, pivot=True, out=None):
    #TODO: Currently not supported on Ascend
    ascend_raise_implement_error("lu_factor")
    #TODO: Mindspore does not support pivot=False condition
    if not pivot:
        raise NotImplementedError("lu_factor currently not supported pivot=False")
    A = cast_to_ms_tensor(A)
    if A.ndim == 2:
        lu, pivots = ms_linalg.lu_factor(A, overwrite_a=False, check_finite=True)
    else:
        lu, pivots = vmap(ms_linalg.lu_factor, in_axes= (0, None, None))(A, False, True)
    pivots = pivots + 1
    output = (lu, pivots)
    return _out_inplace_assign(out, output, "lu_factor")

def lu_factor_ex(A, *, pivot=True, out=None):
    #TODO: Currently not supported on Ascend
    ascend_raise_implement_error("lu_factor_ex")
    #TODO: Mindspore does not support pivot=False condition
    if not pivot:
        raise NotImplementedError("lu_factor currently not supported pivot=False")
    A = cast_to_ms_tensor(A)
    if A.ndim == 2:
        lu, pivots = ms_linalg.lu_factor(A, overwrite_a=False, check_finite=True)
        pivots = pivots + 1
        #TODO: Mindspore not support check_errors
        info = 0
    else:
        lu, pivots = vmap(ms_linalg.lu_factor, in_axes= (0, None, None))(A, False, True)
        pivots = pivots + 1
        #TODO: Mindspore not support check_errors
        #TODO: ms.ops.zeros() currently has preblem handling input shape including 0
        info = _get_cache_prim(ms.ops.Zeros)()(A.shape[0], ms.int32)
    output = (lu, pivots) + (info,)
    return _out_inplace_assign(out, output, "lu_factor_ex")

def lu_solve(B, LU, pivots, *, left=True, adjoint=False, out=None):
    #TODO: Currently not supported on Ascend
    ascend_raise_implement_error("lu_solve")
    #TODO: Mindspore does not support left
    if not left:
        raise NotImplementedError("lu_factor currently not supported left=False")
    LU = cast_to_ms_tensor(LU)
    B = cast_to_ms_tensor(B)
    pivots = cast_to_ms_tensor(pivots).astype(ms.int32)
    pivots = pivots - 1
    A = (LU, pivots)
    trans=2 if adjoint else 0
    if LU.ndim == 2:
        output = ms_linalg.lu_solve(A, B, trans=trans)
    else:
        if pynative_mode_condition():
            output = vmap(ms_linalg.lu_solve, in_axes= (0, 0, None))(A, B, trans)
        else:
            #TODO:vmap function has bug on graph mode now
            output = []
            for i in range(B.shape[0]):
                output.append(ms_linalg.lu_solve((LU[i], pivots[i]), B[i], trans=trans))
            output = ms.ops.stack(output)
    return _out_inplace_assign(out, output, "lu_solve")

def lstsq(a, b, rcond=None, *, out=None):
    lstsq_op = NumpyFullLstsq('torch.linalg.lstsq', rcond)
    x, residuals, rank, s = lstsq_op(a, b)
    rank = int(rank)
    return _out_inplace_assign(out, (x, residuals, rank, s), "lstsq")

def qr(input, mode="reduced", *, out=None):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.qr(input_ms, mode)
    return _out_inplace_assign(out, output, "qr")

def vander(x, N=None, *, out=None):
    x = cast_to_ms_tensor(x)
    #TODO: need to use ops func
    output = ms.numpy.vander(x, N, increasing=True)
    return _out_inplace_assign(out, output, "vander")
