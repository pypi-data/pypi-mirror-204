#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functional interface"""
import math
import warnings
from typing import Iterable
# from functools import lru_cache
import numpy as np
import mindspore as ms
import mindspore.nn as nn
from mindspore.ops.primitive import _primexpr
from mindspore.ops.operations.nn_ops import TripletMarginLoss as TripletMarginLossOp
from mindspore.ops._primitive_cache import _get_cache_prim
from mindspore.ops.function.math_func import _expand, _check_same_type

# from msadapter.utils import unsupported_attr, is_under_ascend_context, _GLOBAL_LRU_CACHE_SIZE_NN
from msadapter.utils import unsupported_attr, is_under_ascend_context
from msadapter.pytorch.tensor import Tensor, cast_to_ms_tensor, cast_to_adapter_tensor
from msadapter.pytorch.common._inner import _inplace_assign_pynative
from msadapter.pytorch.common.dtype import all_int_type
from msadapter.pytorch.nn.modules.utils import _do_pad, _is_zero_paddings, _pair,\
                                                _repeat_tuple

all = [
    'smooth_l1_loss',
    'log_softmax',
    'logsigmoid',
    'elu',
    'elu_',
    'relu',
    'relu_',
    'upsample',
    'rrelu',
    'rrelu_',
    'selu',
    'celu',
    'gelu',
    'mish',
    'softshrink',
    'hardtanh',
    'hardtanh_',
    'hardswish',
    'relu6',
    'leaky_relu',
    'softmax',
    'softmin',
    'softsign',
    'tanh',
    'tanhshrink',
    'glu',
    'softplus',
    'sigmoid',
    'hardsigmoid',
    'silu',
    'gumbel_softmax',
    'threshold',
    'threshold_',
    'hardshrink',

    'conv1d',
    'conv2d',
    'conv3d',

    'normalize',
    'local_response_norm',

    'l1_loss',
    'cross_entropy',
    'ctc_loss',
    'gaussian_nll_loss',
    'hinge_embedding_loss',
    'margin_ranking_loss',
    'multilabel_margin_loss',
    'multilabel_soft_margin_loss',
    'nll_loss',
    'kl_div',
    'binary_cross_entropy',
    'binary_cross_entropy_with_logits',
    'upsample_nearest',
    'poisson_nll_loss',
    'triplet_margin_with_distance_loss',

    'pairwise_distance',
    'cosine_similarity',
    'pdist',

    'dropout1d',
    'dropout2d',
    'dropout3d',
    'dropout',
    'alpha_dropout',
    'feature_alpha_dropout'
    'huber_loss',
    'soft_margin_loss',
    'cosine_embedding_loss',

    'pixel_shuffle',
    'pixel_unshuffle',
    'one_hot',

    'embedding',
    'max_pool2d',

    'fold',
    'unfold',

    'multi_head_attention_forward'
]

@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_adaptive_pool_args(input_shape, output_size):
    _, _, h, w = input_shape
    if isinstance(output_size, int):
        output_size = [output_size, ] * 2
    condition = [0, ] * 2
    out_h = output_size[0] + condition[0] * h
    out_w = output_size[1] + condition[1] * w
    stride_h = math.floor(h / out_h)
    kernel_h = h - (out_h - 1) * stride_h
    stride_w = math.floor(w / out_w)
    kernel_w = w - (out_w - 1) * stride_w
    return kernel_h, kernel_w, stride_h, stride_w

def adaptive_avg_pool1d(input, output_size):
    input = cast_to_ms_tensor(input)
    ndim = input.ndim
    if ndim == 2:
        input = input.expand_dims(0)
        output = ms.ops.adaptive_avg_pool1d(input, output_size)
        output = output.squeeze(0)
    else:
        output = ms.ops.adaptive_avg_pool1d(input, output_size)
    return cast_to_adapter_tensor(output)

def adaptive_avg_pool2d(input, output_size):
    kernel_h, kernel_w, stride_h, stride_w = _get_adaptive_pool_args(input.shape, output_size)
    avg_pool = _get_cache_prim(ms.ops.AvgPool)(kernel_size=(kernel_h, kernel_w),
                                               strides=(stride_h, stride_w),
                                               pad_mode="valid",
                                               data_format="NCHW")

    input = cast_to_ms_tensor(input)
    out = avg_pool(input)
    return cast_to_adapter_tensor(out)

def adaptive_avg_pool3d(input, output_size):
    input = cast_to_ms_tensor(input)
    output = ms.ops.adaptive_avg_pool3d(input, output_size)
    return cast_to_adapter_tensor(output)

@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_adaptive_max_pool1d_const(input_shape, output_size):
    _, _, width = input_shape
    stride = width // output_size
    kernel_size = width - (output_size - 1) * stride
    stride = (1, width // output_size)
    kernel_size = (1, kernel_size)
    return kernel_size, stride

def adaptive_max_pool1d(input, output_size, return_indices=False):
    input = cast_to_ms_tensor(input)
    ndim = input.ndim
    if ndim == 2:
        input = input.expand_dims(0)

    if return_indices:
        input_shape = ms.ops.shape(input)
        _kernel_size, _stride = _get_adaptive_max_pool1d_const(input_shape, output_size)
        max_pool = _get_cache_prim(ms.ops.MaxPoolWithArgmaxV2)(kernel_size=_kernel_size, strides=_stride,
                                                               pads=0, dilation=(1, 1), argmax_type=ms.int32)
        input = input.expand_dims(-2)
        out, idx = max_pool(input)
        out = out.squeeze(-2)
        idx = idx.squeeze(-2)
        if ndim == 2:
            out = out.squeeze(0)
            idx = idx.squeeze(0)
        output = (out, idx)
    else:
        # TODO: ms.ops.adaptive_max_pool1d has some bug, use it in the future
        input_shape = ms.ops.shape(input)
        _kernel_size, _stride = _get_adaptive_max_pool1d_const(input_shape, output_size)
        max_pool_ = _get_cache_prim(ms.ops.MaxPool)(kernel_size=_kernel_size, strides=_stride)
        input = input.expand_dims(-2)
        out = max_pool_(input)
        out = out.squeeze(-2)
        if ndim == 2:
            out = out.squeeze(0)
        output = out

    return cast_to_adapter_tensor(output)


def adaptive_max_pool2d(input, output_size, return_indices=False):
    input = cast_to_ms_tensor(input)
    output = ms.ops.adaptive_max_pool2d(input, output_size, return_indices)
    return cast_to_adapter_tensor(output)

@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_adaptive_max_pool3d_output_size(input_shape, output_size):
    if not isinstance(output_size, Iterable):
        output_size = [output_size, ] * 3
    condition = [0,] * 3
    if None in output_size:
        output_size = list(output_size)
        if output_size[0] is None:
            condition[0] = 1
            output_size[0] = 0
        if output_size[1] is None:
            condition[1] = 1
            output_size[1] = 0
        if output_size[2] is None:
            condition[2] = 1
            output_size[2] = 0
    _, _, d, h, w = input_shape
    out_d = output_size[0] + condition[0] * d
    out_h = output_size[1] + condition[1] * h
    out_w = output_size[2] + condition[2] * w
    return out_d, out_h, out_w

@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_adaptive_max_pool3d_stride(input_shape, output_size):
    out_d, out_h, out_w = output_size
    _, _, d, h, w = input_shape
    stride_d = d // out_d
    kernel_d = d - (out_d - 1) * stride_d
    stride_h = h // out_h
    kernel_h = h - (out_h - 1) * stride_h
    stride_w = w // out_w
    kernel_w = w - (out_w - 1) * stride_w

    return kernel_d, kernel_h, kernel_w, stride_d, stride_h, stride_w

def adaptive_max_pool3d(input, output_size, return_indices=False):
    input = cast_to_ms_tensor(input)
    input_shape = ms.ops.shape(input)
    _output_size = _get_adaptive_max_pool3d_output_size(input_shape, output_size)

    if is_under_ascend_context():
        # TODO: Ascend not support ms.ops.adaptive_max_pool3d, use MaxPool3D instead
        # MaxPool3D result is not the same as adaptive_max_pool3d, but the shape.
        # Implement below do not affect the converge of trainning.
        if return_indices:
            raise NotImplementedError("For adaptive_max_pool3d, return_indices is not supported yet.")

        kernel_d, kernel_h, kernel_w, stride_d, stride_h, stride_w = \
            _get_adaptive_max_pool3d_stride(input_shape, _output_size)

        avg_pool = ms.ops.MaxPool3D(kernel_size=(kernel_d, kernel_h, kernel_w),
                                    strides=(stride_d, stride_h, stride_w),
                                    pad_mode="valid", data_format="NCDHW")
        output = avg_pool(input)
    else:
        output = ms.ops.adaptive_max_pool3d(input, _output_size, return_indices)

    return cast_to_adapter_tensor(output)

def pad(input, pad, mode="constant", value=0):
    if mode == "replicate":
        mode = "edge"

    value = ms.Tensor(value, dtype=input.dtype)
    dims = len(input.shape)
    list_pad = [pad[i:i+2] for i in range(0, len(pad), 2)]
    list_pad.reverse()
    new_pad = [[0,0],] * int((dims - len(pad) /2))
    new_pad.extend(list_pad)

    input = cast_to_ms_tensor(input)
    # TODO: -> ms.ops.PadV3, Padv3 is not supported on Ascend now.
    # output =  ms.ops.operations.nn_ops.PadV3(mode=mode)(input, pad, value)
    output = ms.numpy.pad(input, new_pad, mode=mode, constant_values=value)
    return cast_to_adapter_tensor(output)

def log_softmax(input, dim=None, _stacklevel=3, dtype=None):
    unsupported_attr(_stacklevel)
    # MS dim default is -1
    if dim is None:
        warnings.warn("Implicit dimension choice for log_softmax has been deprecated. "
                      "Change the call to include dim=X as an argument")
        dim = -1

    input = cast_to_ms_tensor(input)
    if dtype is not None:
        input = ms.ops.cast(input, dtype)

    out = ms.ops.log_softmax(input, dim)
    return cast_to_adapter_tensor(out)

def logsigmoid(input):
    input = cast_to_ms_tensor(input)
    sigmoid_op = _get_cache_prim(ms.ops.Sigmoid)()
    sigmoid_out= sigmoid_op(input)
    ret = ms.ops.log(sigmoid_out)
    return cast_to_adapter_tensor(ret)

def elu(input, alpha=1.0, inplace=False):
    input_ms = cast_to_ms_tensor(input)
    if alpha == 1:
        out = ms.ops.elu(input_ms, alpha)
    else:
        cond = ms.ops.gt(input_ms, 0)
        out = alpha * (ms.ops.exp(input_ms) - 1)
        out = ms.ops.select(cond, input_ms, out)
    return _inplace_assign_pynative(input, inplace, out, "elu")


def rrelu(input, lower=1.0/8, upper=1.0/3, training=False, inplace=False):
    if training:
        raise ValueError("training '{}' is not currently supported.".format(training))

    input_ms = cast_to_ms_tensor(input)
    #TODO： nn.RReLU should be replaced
    out = nn.RReLU(lower=lower, upper=upper)(input_ms)
    return _inplace_assign_pynative(input, inplace, out, "rrelu")


def selu(input, inplace=False):
    input_ms = cast_to_ms_tensor(input)
    out = ms.ops.selu(input_ms)
    return _inplace_assign_pynative(input, inplace, out, "selu")


def celu(input, alpha=1.0, inplace=False):
    input_ms = cast_to_ms_tensor(input)
    out = ms.ops.celu(input_ms, alpha)
    return _inplace_assign_pynative(input, inplace, out, "celu")


def gelu(input, approximate='none'):
    input_x = cast_to_ms_tensor(input)
    out = ms.ops.gelu(input_x, approximate)
    return cast_to_adapter_tensor(out)


def mish(input, inplace=False):
    input_ms = cast_to_ms_tensor(input)
    out = ms.ops.mish(input_ms)
    return _inplace_assign_pynative(input, inplace, out, "mish")

def softshrink(input, lambd=0.5):
    input = cast_to_ms_tensor(input)
    #TODO: if switch the mindspore version, change the code to
    # out = ms.ops.softshrink(input, lambd)
    out = ms.ops.soft_shrink(input, lambd)
    return cast_to_adapter_tensor(out)


def relu(input, inplace=False):
    input_ms = cast_to_ms_tensor(input)
    out = ms.ops.relu(input_ms)
    return _inplace_assign_pynative(input, inplace, out, "relu")


def hardtanh(input, min_val=-1.0, max_val=1.0, inplace=False):

    input_ms = cast_to_ms_tensor(input)
    out = nn.Hardtanh(min_val, max_val)(input_ms)
    return _inplace_assign_pynative(input, inplace, out, "hardtanh")


def hardswish(input, inplace=False):

    input_ms = cast_to_ms_tensor(input)
    out = ms.ops.hardswish(input_ms)
    return _inplace_assign_pynative(input, inplace, out, "hardswish")


def relu6(input, inplace=False):

    input_ms = cast_to_ms_tensor(input)
    out = ms.ops.relu6(input_ms)
    return _inplace_assign_pynative(input, inplace, out, "relu6")


def leaky_relu(input, negative_slope=0.01, inplace=False):

    input_ms = cast_to_ms_tensor(input)
    #TODO：nn.LeakyReLU should be replaced.
    out = nn.LeakyReLU(alpha=negative_slope)(input_ms)
    return _inplace_assign_pynative(input, inplace, out, "leaky_relu")


def upsample(input, size=None, scale_factor=None, mode='nearest',
        align_corners=False):

    if size is None and scale_factor is None:
        raise ValueError("either size or scale_factor should be defined")

    if size is not None and scale_factor is not None:
        raise ValueError("only one of size or scale_factor should be defined")

    def linear_func(input):
        _size =_upsample_common_process_size(size, scale_factor, input.shape)

        input = cast_to_ms_tensor(input)
        out = ms.ops.interpolate(input, scale_factor=None, size=_size,
                                 align_corners=align_corners, mode=mode)

        return cast_to_adapter_tensor(out)

    def bllinear_func(input):
        return upsample_bilinear(input, size=size, scale_factor=scale_factor, align_corners=align_corners)

    def resize_nearest_neighbor_func(input):
        return upsample_nearest(input, size=size, scale_factor=scale_factor)

    mode_func = {'linear': linear_func,
                 'bilinear': bllinear_func,
                 'nearest': resize_nearest_neighbor_func}

    if mode not in mode_func:
        raise ValueError("Until now, `mode` beside 'linear', 'bilinear', 'nearest' are not supported")

    func = mode_func[mode]

    out = func(input)
    return out

@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_softmax_dim(ndim):
    if ndim in (0, 1, 3):
        ret = 0
    else:
        ret = 1
    return ret


def softmax(input, dim=None, _stacklevel=3, dtype=None):
    unsupported_attr(_stacklevel)
    # MS dim default is -1
    if dim is None:
        dim = -1

    input = cast_to_ms_tensor(input)
    if dtype is not None:
        input = ms.ops.cast(input, dtype)
    out = ms.ops.softmax(input, axis=dim)
    return cast_to_adapter_tensor(out)


def softmin(input, dim=None, dtype=None):
    # MS dim default is -1
    # TODO
    # ms.ops.softmax should be replaced by ms.ops.softmin
    if dim is None:
        dim = _get_softmax_dim(input.dim())

    input = cast_to_ms_tensor(input)
    if dtype is not None:
        input = ms.ops.cast(input, dtype)
    x = -input
    out = ms.ops.softmax(x, axis=dim)
    return cast_to_adapter_tensor(out)


def softsign(input):
    input = cast_to_ms_tensor(input)
    output =  ms.ops.functional.softsign(input)
    return cast_to_adapter_tensor(output)


def tanh(input):
    input = cast_to_ms_tensor(input)
    if not input.is_floating_point():
        input = input.astype(ms.float32)
    output = ms.ops.tanh(input)
    return cast_to_adapter_tensor(output)


def tanhshrink(input):
    input = cast_to_ms_tensor(input)
    output = input - ms.ops.functional.tanh(input)
    return cast_to_adapter_tensor(output)


def glu(input, dim=-1):
    if input.dim() == 0:
        raise RuntimeError("glu does not support scalars because halving size must be even")
    if input.shape[dim] % 2 == 1:
        raise RuntimeError("Halving dimension must be even, but dimension {} is size {}".format(dim,input.shape[dim]))
    halflen = input.shape[dim]//2
    input = cast_to_ms_tensor(input)
    data_a = input.narrow(axis=dim, start=0, length=halflen)
    data_b = input.narrow(axis=dim, start=halflen, length=halflen)

    sigmoid_data_b = ms.ops.sigmoid(data_b)
    out = ms.ops.mul(data_a, sigmoid_data_b)
    return cast_to_adapter_tensor(out)


def normalize(input, p=2.0, dim=1, eps=1e-12, out=None):
    #the type of 'p' in ms.ops.functional.norm should be 'int'
    input = cast_to_ms_tensor(input)
    input_p = ms.ops.pow(abs(input), p)
    input_p_sum = input_p.sum(axis = dim, keepdims=True)

    norm = ms.ops.pow(input_p_sum, 1.0/p)
    min_value = ms.Tensor(eps, ms.float32)
    denom = ms.ops.clip_by_value(norm, min_value)
    denom = denom.expand_as(input)
    output = ms.ops.functional.div(input, denom)

    if out is not None:
        ms.ops.assign(out, output)
        return out
    return cast_to_adapter_tensor(output)


def softplus(input, beta=1, threshold=20):
    input = cast_to_ms_tensor(input)
    input_x = beta * input
    dtype_op = _get_cache_prim(ms.ops.DType)()
    cast_op = _get_cache_prim(ms.ops.Cast)()
    alpha_array = cast_op(ms.ops.functional.scalar_to_tensor(threshold), dtype_op(input))

    mask = ms.ops.less(alpha_array, input_x)
    input_mask = ms.ops.masked_fill(input_x, mask, 0)

    out_mask = ms.ops.exp(input_mask)
    out_mask_log = ms.ops.log1p(out_mask)
    ret_mask = out_mask_log/beta

    ret = ms.ops.select(mask, input, ret_mask)
    return cast_to_adapter_tensor(ret)


def sigmoid(input):
    input = cast_to_ms_tensor(input)
    if is_under_ascend_context() and input.dtype == ms.float64:
        input = input.astype(ms.float32)
        out = ms.ops.sigmoid(input)
        out = out.astype(ms.float64)
    else:
        out = ms.ops.sigmoid(input)
    return cast_to_adapter_tensor(out)


def hardsigmoid(input, inplace=False):
    input_ms = cast_to_ms_tensor(input)
    hardsigmoid_op = _get_cache_prim(ms.ops.HSigmoid)()
    out = hardsigmoid_op(input_ms)
    return _inplace_assign_pynative(input, inplace, out, "hardsigmoid")


def silu(input, inplace=False):
    input_ms = cast_to_ms_tensor(input)
    sigmoid_op = _get_cache_prim(ms.ops.Sigmoid)()
    out = sigmoid_op(input_ms) * input_ms
    return _inplace_assign_pynative(input, inplace, out, "silu")


def gumbel_softmax(logits, tau=1.0, hard=False, eps=1e-10, dim=-1):
    if eps != 1e-10:
        warnings.warn("`eps` parameter is deprecated and has no effect.")
    logits = cast_to_ms_tensor(logits)
    out = ms.ops.gumbel_softmax(logits, tau, hard, dim)
    return cast_to_adapter_tensor(out)


def threshold(input, threshold, value, inplace=False):
    #TODO: threshold---function name and input name is same will raise error on Graph mode.
    input_ms = cast_to_ms_tensor(input)
    out = ms.ops.threshold(input_ms, threshold, value)
    return _inplace_assign_pynative(input, inplace, out, "threshold")


rrelu_ = rrelu
relu_ = relu
elu_ = elu
hardtanh_ = hardtanh
leaky_relu_ = leaky_relu
threshold_ = threshold

@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_reduce_string(size_average, reduce):
    if size_average is None:
        size_average = True
    if reduce is None:
        reduce = True

    if size_average and reduce:
        ret = 'mean'
    elif reduce:
        ret = 'sum'
    else:
        ret = 'none'

    warning = "size_average and reduce args will be deprecated, please use reduction='{}' instead."
    warnings.warn(warning.format(ret))
    return ret


def smooth_l1_loss(input, target, size_average=None, reduce=None, reduction='mean', beta=1.0):
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)

    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    output = ms.ops.smooth_l1_loss(input, target, beta, reduction)
    if reduction != 'none' and len(output.shape) == 1:
        return cast_to_adapter_tensor(output[0])
    return cast_to_adapter_tensor(output)

def _get_loss(x, reduction):
    """
    Computes the loss.
    """
    if reduction is None or reduction == 'none':
        return x

    def _get_axis(x):
        shape = ms.ops.shape(x)
        length = ms.ops.tuple_len(shape)
        perm = ms.ops.make_range(0, length)
        return perm

    input_dtype = x.dtype
    x = ms.ops.cast(x, ms.float32)
    if reduction == 'mean':
        reduce_mean_op = _get_cache_prim(ms.ops.ReduceMean)()
        x = reduce_mean_op(x, _get_axis(x))
    if reduction == 'sum':
        x = ms.ops.reduce_sum(x, _get_axis(x))
    x = ms.ops.cast(x, input_dtype)
    return x


def l1_loss(input, target, size_average=None, reduce=None, reduction="mean"):
    """
    Function that takes the mean element-wise absolute value difference.
    """
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)

    def _l1_loss_function(input, target, reduction):
        x = ms.ops.abs(input - target)
        return _get_loss(x, reduction)

    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    # TODO: Replace with ms.ops.l1_loss
    result = _l1_loss_function(input, target, reduction)
    return cast_to_adapter_tensor(result)


def mse_loss(input, target, size_average=None, reduce=None, reduction="mean"):
    """
    Measures the element-wise mean squared error.
    """
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)

    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    x = ms.ops.square(input - target)
    result = _get_loss(x, reduction)
    return cast_to_adapter_tensor(result)

def cross_entropy(input, target, weight=None, size_average=None, ignore_index=-100,
                  reduce=None, reduction="mean", label_smoothing=0.0):
    """
    This criterion computes the cross entropy loss between input logits and target.
    """
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)

    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    weight = cast_to_ms_tensor(weight)
    result = ms.ops.cross_entropy(input, target, weight, ignore_index, reduction, label_smoothing)
    return cast_to_adapter_tensor(result)

def ctc_loss(log_probs, targets, input_lengths, target_lengths, blank=0, reduction='mean', zero_infinity=False):
    log_probs = cast_to_ms_tensor(log_probs)
    targets = cast_to_ms_tensor(targets)
    #TODO: length do not support tuple
    if not isinstance(input_lengths, Tensor) or not isinstance(target_lengths, Tensor):
        raise TypeError("'input_lengths' and 'target_lengths' only support Tensor now")
    if isinstance(input_lengths, Tensor) and isinstance(target_lengths, Tensor):
        input_lengths = cast_to_ms_tensor(input_lengths)
        target_lengths = cast_to_ms_tensor(target_lengths)

    if targets.dtype not in (ms.int32, ms.int64) \
            or not (targets.dtype == input_lengths.dtype and targets.dtype == target_lengths.dtype):
        targets = targets.astype(ms.int64)
        input_lengths = input_lengths.astype(ms.int64)
        target_lengths = target_lengths.astype(ms.int64)
    result, _ = ms.ops.ctc_loss(log_probs, targets, input_lengths, target_lengths, blank, reduction, zero_infinity)
    return cast_to_adapter_tensor(result)

def gaussian_nll_loss(input, target, var, full=False, eps=1e-06, reduction='mean'):
    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    var = cast_to_ms_tensor(var)
    rlt = ms.ops.gaussian_nll_loss(input, target, var, full, eps, reduction)
    return cast_to_adapter_tensor(rlt)

def hinge_embedding_loss(input, target, margin=1.0, size_average=None, reduce=None, reduction='mean'):
    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)
    rlt = ms.ops.hinge_embedding_loss(input, target, float(margin), reduction)
    return cast_to_adapter_tensor(rlt)

def margin_ranking_loss(input1, input2, target, margin=0, size_average=None, reduce=None, reduction='mean'):
    input1 = cast_to_ms_tensor(input1)
    input2 = cast_to_ms_tensor(input2)
    target = cast_to_ms_tensor(target)
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)
    rlt = ms.ops.margin_ranking_loss(input1, input2, target, float(margin), reduction)
    return cast_to_adapter_tensor(rlt)

def multilabel_margin_loss(input, target, size_average=None, reduce=None, reduction='mean'):
    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    if target.dtype != ms.int32:
        target = target.astype(ms.int32)
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)
    rlt = ms.ops.multilabel_margin_loss(input, target, reduction)
    return cast_to_adapter_tensor(rlt)

def multilabel_soft_margin_loss(input, target, weight=None, size_average=None, reduce=None, reduction='mean'):
    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    if isinstance(weight, Tensor):
        weight = cast_to_ms_tensor(weight)
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)
    rlt = ms.ops.multilabel_soft_margin_loss(input, target, weight, reduction)
    return cast_to_adapter_tensor(rlt)

def nll_loss(input, target, weight=None, size_average=None, ignore_index=-100,
             reduce=None, reduction="mean"):
    """
    The negative log likelihood loss.
    """
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)

    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    weight = cast_to_ms_tensor(weight)
    result = ms.ops.nll_loss(input, target, weight, ignore_index, reduction, label_smoothing=0.0)
    return cast_to_adapter_tensor(result)

def kl_div(input, target, size_average=None, reduce=None, reduction="mean", log_target=False):
    """
    The `Kullback-Leibler divergence Loss.
    <https://en.wikipedia.org/wiki/Kullback-Leibler_divergence>`
    """
    if size_average is not None or reduce is not None:
        reduction = _get_reduce_string(size_average, reduce)

    # TODO
    if log_target is True:
        raise ValueError('`log_target` in `{}` can not support True'.format(kl_div.__name__))

    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    result = ms.ops.kl_div(input, target, reduction)
    return cast_to_adapter_tensor(result)

def binary_cross_entropy(input, target, weight=None, size_average=None, reduce=None, reduction="mean"):
    """
    Function that measures the Binary Cross Entropy between the target and input probabilities.
    """
    if size_average is not None or reduce is not None:
        reduction = _get_reduce_string(size_average, reduce)

    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    weight = cast_to_ms_tensor(weight)
    result = ms.ops.binary_cross_entropy(input, target, weight, reduction)
    return cast_to_adapter_tensor(result)

def binary_cross_entropy_with_logits(input, target, weight=None, size_average=None,
                                     reduce=None, reduction="mean", pos_weight=None):
    """
    Function that measures Binary Cross Entropy between target and input logits.
    """
    if size_average is not None or reduce is not None:
        reduction = _get_reduce_string(size_average, reduce)

    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    weight = cast_to_ms_tensor(weight)
    pos_weight = cast_to_ms_tensor(pos_weight)
    if weight is None or pos_weight is None:
        ones_input = ms.ops.ones_like(input)
        if weight is None:
            weight = ones_input
        if pos_weight is None:
            pos_weight = ones_input

    result = ms.ops.binary_cross_entropy_with_logits(input, target, weight, pos_weight, reduction)
    return cast_to_adapter_tensor(result)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _upsample_common_check(size, scale_factor):
    if size is None and scale_factor is None:
        raise ValueError("either size or scale_factor should be defined.")

    if size is not None and scale_factor is not None:
        raise ValueError("only one of size or scale_factor should be defined.")

@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _upsample_common_process_size(size, scale_factor, shape):
    input_shape = list(shape)
    input_rank = len(shape)
    if scale_factor is not None:
        size_ = input_shape[2:]
        for i, _ in enumerate(size_):
            size_[i] *= scale_factor
            size_[i] = int(size_[i])
    else:
        if not isinstance(size, (int, list, tuple)):
            raise TypeError("`size` should be in types of int, list and tuple.")
        if isinstance(size, int):
            size_ = [size for i in range(2, input_rank)]
        else:
            if len(size) != input_rank - 2:
                raise ValueError(
                    "Input and output must have the same number of spatial dimensions, but got "
                    f"input with spatial dimensions of {list(input_shape[2:])} and output size of {size}. "
                    "Please provide input tensor in (N, C, d1, d2, ...,dK) format and "
                    "output size in (o1, o2, ...,oK) format.")
            size_ = size
    return tuple(size_)

def upsample_nearest(input, size=None, scale_factor=None):
    _upsample_common_check(size, scale_factor)
    input_shape = input.shape
    _input_rank = len(input_shape)
    size_ = _upsample_common_process_size(size, scale_factor, input_shape)

    if _input_rank == 4:
        _op = _get_cache_prim(ms.ops.ResizeNearestNeighbor)(size_, align_corners=False)
    elif _input_rank == 5:
        _op = _get_cache_prim(ms.ops.UpsampleNearest3D)(size_)
    else:
        raise ValueError(f"upsample_nearest only support 4D or 5D input, but got {_input_rank}D.")

    input = cast_to_ms_tensor(input)
    result = _op(input)
    return cast_to_adapter_tensor(result)

def upsample_bilinear(input, size=None, scale_factor=None, *, align_corners=True):
    input_shape = input.shape

    if len(input_shape) != 4:
        raise ValueError("Until now, upsample_bilinear only support 4-D input.")

    _upsample_common_check(size, scale_factor)
    size_ = _upsample_common_process_size(size, scale_factor, input_shape)

    input = cast_to_ms_tensor(input)

    result = ms.ops.interpolate(input, size=size_, align_corners=align_corners, mode="bilinear")
    return cast_to_adapter_tensor(result)

def pairwise_distance(x1, x2, p=2.0, eps=1e-06, keepdim=False):
    x1 = cast_to_ms_tensor(x1)
    x2 = cast_to_ms_tensor(x2)
    input = x1-x2+eps
    input_p = ms.ops.pow(ms.ops.abs(input), p)
    input_p_sum = input_p.sum(axis=-1, keepdims=keepdim)
    out = ms.ops.pow(input_p_sum, 1.0 / p)
    return cast_to_adapter_tensor(out)


def cosine_similarity(x1, x2, dim=1, eps=1e-08):
    x1 = cast_to_ms_tensor(x1)
    x2 = cast_to_ms_tensor(x2)
    while x1.ndim < x2.ndim:
        x1 = x1.expand_dims(0)
    while x2.ndim < x1.ndim:
        x2 = x2.expand_dims(0)
    if x1.size < x2.size:
        x1 = ms.ops.broadcast_to(x1, x2.shape)
    if x2.size < x1.size:
        x2 = ms.ops.broadcast_to(x2, x1.shape)

    min_value = ms.Tensor(eps, ms.float32)

    x1_norm = ms.ops.pow(x1, 2)
    x1_norm = x1_norm.sum(axis=dim)
    x1_norm = ms.ops.pow(x1_norm, 1.0/2)
    x1_norm = ms.ops.clip_by_value(x1_norm, min_value)
    x2_norm = ms.ops.pow(x2, 2)
    x2_norm = x2_norm.sum(axis=dim)
    x2_norm = ms.ops.pow(x2_norm, 1.0/2)
    x2_norm = ms.ops.clip_by_value(x2_norm, min_value)

    denom = ms.ops.mul(x1_norm, x2_norm)
    out = ms.ops.mul(x1, x2).sum(axis=dim)/denom
    return cast_to_adapter_tensor(out)

def pdist(input, p=2):
    inp_dim = input.dim()
    if inp_dim != 2:
        raise RuntimeError(f"pdist only supports 2D tensors, got: {inp_dim}D")
    if p < 0:
        raise RuntimeError("pdist only supports non-negative p values")

    input = cast_to_ms_tensor(input)
    n, m = input.shape
    x = input.broadcast_to((n, n, m)).astype(ms.float32)
    y = x.transpose(1, 0, 2)
    norm = ms.ops.pow(ms.ops.abs(x-y), p)
    norm = norm.sum(axis=-1)
    if p > 0:
        norm = ms.ops.pow(norm, 1.0/p)
    select = np.ones([n, n])
    select = np.triu(select, 1).astype(np.bool8)
    select_t = ms.Tensor(select)
    out = ms.ops.masked_select(norm, select_t)
    return cast_to_adapter_tensor(out)


def dropout1d(input, p = 0.5, training = True, inplace = False):
    if p < 0.0 or p > 1.0:
        raise ValueError("dropout probability has to be between 0 and 1, " "but got {}".format(p))
    inp_dim = input.dim()
    if inp_dim not in (2, 3):
        raise RuntimeError(f"dropout1d: Expected 2D or 3D input, but received a {inp_dim}D input. "
                           "Note that dropout1d exists to provide channel-wise dropout on inputs with 1 "
                           "spatial dimension, a channel dimension, and an optional batch dimension "
                           "(i.e. 2D or 3D inputs).")
    # is_batched = inp_dim == 3
    if not training:
        return input

    input_ms = cast_to_ms_tensor(input)
    out = ms.ops.dropout1d(input_ms, p)
    return _inplace_assign_pynative(input, inplace, out, "dropout1d")


def dropout2d(input, p=0.5, training=True, inplace=False):
    if p < 0.0 or p > 1.0:
        raise ValueError("dropout probability has to be between 0 and 1, " "but got {}".format(p))
    inp_dim = input.dim()
    if inp_dim not in (3, 4):
        warn_msg = (f"dropout2d: Received a {inp_dim}-D input to dropout2d, which is deprecated "
                    "and will result in an error in a future release. To retain the behavior "
                    "and silence this warning, please use dropout instead. Note that dropout2d "
                    "exists to provide channel-wise dropout on inputs with 2 spatial dimensions, "
                    "a channel dimension, and an optional batch dimension (i.e. 3D or 4D inputs).")
        warnings.warn(warn_msg)
    if not training:
        return input
    if inp_dim == 3:
        warnings.warn("dropout2d: Received a 3D input to dropout2d and assuming that channel-wise "
                      "1D dropout behavior is desired - input is interpreted as shape (N, C, L), where C "
                      "is the channel dim. This behavior will change in a future release to interpret the "
                      "input as one without a batch dimension, i.e. shape (C, H, W). To maintain the 1D "
                      "channel-wise dropout behavior, please switch to using dropout1d instead.")
        return dropout1d(input, p, training, inplace)

    input_ms = cast_to_ms_tensor(input)
    out = ms.ops.dropout2d(input_ms, p)
    return _inplace_assign_pynative(input, inplace, out, "dropout2d")


def dropout3d(input, p=0.5, training=True, inplace=False):
    if p < 0.0 or p > 1.0:
        raise ValueError("dropout probability has to be between 0 and 1, " "but got {}".format(p))
    inp_dim = input.dim()
    if inp_dim not in (4, 5):
        warn_msg = (f"dropout3d: Received a {inp_dim}-D input to dropout3d, which is deprecated "
                    "and will result in an error in a future release. To retain the behavior "
                    "and silence this warning, please use dropout instead. Note that dropout3d "
                    "exists to provide channel-wise dropout on inputs with 3 spatial dimensions, "
                    "a channel dimension, and an optional batch dimension (i.e. 4D or 5D inputs).")
        warnings.warn(warn_msg)
    if not training:
        return input

    is_batched = inp_dim == 5

    input_ms = cast_to_ms_tensor(input)
    if not is_batched:
        input_ms = ms.ops.expand_dims(input_ms, 0)
    out = ms.ops.dropout3d(input_ms, p)
    if not is_batched:
        out = ms.ops.squeeze(out, 0)

    return _inplace_assign_pynative(input, inplace, out, "dropout3d")


def dropout(input, p=0.5, training=True, inplace=False):
    if p < 0.0 or p > 1.0:
        raise ValueError("dropout probability has to be between 0 and 1, " "but got {}".format(p))

    if not training:
        return input

    input_ms = cast_to_ms_tensor(input)
    shape = input_ms.shape
    random_array_np = np.random.rand(input_ms.size).reshape(shape)
    random_array = ms.Tensor(random_array_np, ms.float32)
    mask = (random_array > ms.Tensor(p, ms.float32))
    out = mask * 1.0 / (1.0-p) * input_ms

    return _inplace_assign_pynative(input, inplace, out, "dropout")


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_alpha_dropout_const(p):
    mean = 0.0
    var = 1.0
    scale = 1.0507009873554804934193349852946
    alpha = 1.6732632423543772848170429916717
    alpha_ = -scale * alpha
    q = 1.0 - p
    a = math.sqrt(var/(q*var + q*(1.0-q)*(alpha_-mean)*(alpha_-mean)))
    b = mean - a*(q*mean + (1.0-q)*alpha_)
    return alpha_, a, b

def alpha_dropout(input, p=0.5, training=False, inplace=False):
    if p < 0.0 or p > 1.0:
        raise ValueError("dropout probability has to be between 0 and 1, " "but got {}".format(p))
    if not training:
        return input

    alpha_, a, b = _get_alpha_dropout_const(p)

    input_x = cast_to_ms_tensor(input)
    # mean = input.mean()
    # var = input.var()
    shape = input_x.shape
    random_array_np = np.random.rand(input_x.size).reshape(shape)
    random_array = ms.Tensor(random_array_np, ms.float32)
    mask = (random_array > ms.Tensor(p, ms.float32))

    value = ms.ops.fill(input_x.dtype, shape, alpha_)
    out = input_x * mask
    out = ms.ops.select(mask, out, value)
    out = out * a + b
    return _inplace_assign_pynative(input, inplace, out, "alpha_dropout")


def feature_alpha_dropout(input, p=0.5, training=False, inplace=False):
    if p < 0.0 or p > 1.0:
        raise ValueError("dropout probability has to be between 0 and 1, " "but got {}".format(p))
    if not training:
        return input

    alpha_, a, b = _get_alpha_dropout_const(p)

    input_x = cast_to_ms_tensor(input)
    # mean = input.mean()
    # var = input.var()
    shape = input_x.shape
    random_array_np = np.random.rand(shape[0], shape[1])
    random_array = ms.Tensor(random_array_np, ms.float32)

    if input_x.dim() > 2:
        random_array = random_array.expand_dims(2)
        random_array = random_array.expand_as(input_x.reshape(shape[0], shape[1], -1)).reshape(shape)
    mask = (random_array > ms.Tensor(p, ms.float32))

    value = ms.ops.fill(input_x.dtype, input_x.shape, alpha_)
    out = input_x * mask
    out = ms.ops.select(mask, out, value)
    out = out * a + b
    return _inplace_assign_pynative(input, inplace, out, "feature_alpha_dropout")


def hardshrink(input, lambd=0.5):
    input = cast_to_ms_tensor(input)
    out = ms.ops.hardshrink(input, lambd)
    return cast_to_adapter_tensor(out)

def huber_loss(input, target, reduction='mean', delta=1.0):
    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)

    delta_half = 0.5 * delta

    z = ms.ops.abs(ms.ops.sub(input, target))
    condition = ms.ops.less(z, delta)
    l1 = ms.ops.mul(0.5, ms.ops.square(z))
    l2 = ms.ops.mul(delta, ms.ops.sub(z, delta_half))
    loss = ms.ops.select(condition, l1, l2)
    loss = _get_loss(loss, reduction)
    return cast_to_adapter_tensor(loss)

def soft_margin_loss(input, target, size_average=None, reduce=None, reduction='mean'):
    if size_average is not None or reduce is not None:
        reduction = _get_reduce_string(size_average, reduce)

    input = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)

    ops = ms.ops.SoftMarginLoss(reduction)
    loss = ops(input, target)
    return cast_to_adapter_tensor(loss)

def cosine_embedding_loss(
    input1,
    input2,
    target,
    margin=0,
    size_average=None,
    reduce=None,
    reduction="mean",
):
    if margin < -1.0 or margin > 1.0:
        raise ValueError(f"'cosine_embedding_loss': `margin` should be from -1 to 1, but got {margin}")

    if size_average is not None or reduce is not None:
        reduction = _get_reduce_string(size_average, reduce)

    input1 = cast_to_ms_tensor(input1)
    input2 = cast_to_ms_tensor(input2)
    target = cast_to_ms_tensor(target)

    ndim = input1.ndim
    if ndim == 1:
        input1 = input1.expand_dims(0)
        input2 = input2.expand_dims(0)
        target = target.expand_dims(0)

    reduce_sum = _get_cache_prim(ms.ops.ReduceSum)()
    maximum = _get_cache_prim(ms.ops.Maximum)()

    prod_sum = reduce_sum(input1 * input2, (1,))
    square1 = reduce_sum(ms.ops.square(input1), (1,))
    square2 = reduce_sum(ms.ops.square(input2), (1,))
    denom = ms.ops.sqrt(square1) * ms.ops.sqrt(square2)
    cosine = prod_sum / denom

    pos_value = 1.0 - cosine
    neg_value = maximum(cosine - margin, 0.0)
    zeros = ms.ops.zeros_like(cosine)
    pos_part = ms.ops.select(target == 1, pos_value, zeros)
    neg_part = ms.ops.select(target == -1, neg_value, zeros)
    output_unreduced = pos_part + neg_part
    loss = _get_loss(output_unreduced, reduction)
    if ndim == 1 and reduction == 'none':
        loss = loss.squeeze(0)
    return cast_to_adapter_tensor(loss)

def triplet_margin_loss(
    anchor,
    positive,
    negative,
    margin=1.0,
    p=2,
    eps=1e-6,
    swap=False,
    size_average=None,
    reduce=None,
    reduction="mean",
):

    if size_average is not None or reduce is not None:
        reduction = _get_reduce_string(size_average, reduce)

    anchor, positive, negative = cast_to_ms_tensor((anchor, positive, negative))
    ndim = anchor.ndim
    if ndim == 1:
        anchor = anchor.expand_dims(0)
        positive = positive.expand_dims(0)
        negative = negative.expand_dims(0)

    margin = ms.ops.scalar_to_tensor(margin)
    # TODO: 'TripletMarginLossOp' is a inner interface, should be change to public api in the future
    triplet_margin_loss = _get_cache_prim(TripletMarginLossOp)(p=p, swap=swap, eps=eps, reduction=reduction)
    loss = triplet_margin_loss(anchor, positive, negative, margin)
    if ndim == 1 and reduction == 'none':
        loss = loss.squeeze(0)
    return cast_to_adapter_tensor(loss)

def multi_margin_loss(
    input,
    target,
    p=1,
    margin=1,
    weight=None,
    size_average=None,
    reduce=None,
    reduction="mean",
):

    if size_average is not None or reduce is not None:
        reduction = _get_reduce_string(size_average, reduce)

    if p not in (1, 2):
        raise ValueError("only p == 1 and p == 2 supported")

    input, target = cast_to_ms_tensor((input, target))

    if weight is not None:
        if weight.dim() != 1:
            raise ValueError("weight must be one-dimensional")
        weight = cast_to_ms_tensor(weight)
        loss = ms.ops.multi_margin_loss(input, target, p=p, margin=margin, weight=weight, reduction=reduction)
        return cast_to_adapter_tensor(loss)

    loss = ms.ops.multi_margin_loss(input, target, p=p, margin=margin, weight=weight, reduction=reduction)
    return cast_to_adapter_tensor(loss)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_avg_pool2d_const(kernel_size, stride, padding):
    if stride is None:
        stride = kernel_size

    padding = padding if isinstance(padding, tuple) else _pair(padding)
    return kernel_size, stride, padding

def avg_pool2d(input, kernel_size, stride=None, padding=0, ceil_mode=False,
               count_include_pad=True, divisor_override=None):
    unsupported_attr(ceil_mode)
    unsupported_attr(count_include_pad)
    unsupported_attr(divisor_override)

    _kernel_size, _stride, _padding = _get_avg_pool2d_const(kernel_size, stride, padding)

    # TODO: to use ms.ops.avgpool with `pad_mode` supported 'pad'
    avg_pool_ops = _get_cache_prim(ms.ops.AvgPool)(kernel_size=_kernel_size, strides=_stride, pad_mode='valid')
    ndim = input.ndim
    input = cast_to_ms_tensor(input)

    if _is_zero_paddings(padding):
        if ndim == 3:
            input = input.expand_dims(0)
            out = avg_pool_ops(input)
            out = out.squeeze(0)
        else:
            out = avg_pool_ops(input)
    else:
        if ndim == 3:
            input = input.expand_dims(0)
            input = _do_pad(input, _padding)
            out = avg_pool_ops(input)
            out = out.squeeze(0)
        else:
            input = _do_pad(input, _padding)
            out = avg_pool_ops(input)
    return cast_to_adapter_tensor(out)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_local_response_norm_const(x_dim, size):
    if x_dim < 3:
        raise ValueError("Expected 3D or higher dimensionality"
                         f"input (got {x_dim} dimensions)")

    if x_dim == 3:
        return ((size//2, (size-1)//2), (0, 0))

    return ((size//2, (size-1)//2), (0, 0), (0, 0))

def local_response_norm(input, size, alpha=0.0001, beta=0.75, k=1.0):
    if len(input.shape) == 0:
        return input

    dim = input.dim()
    _pad = _get_local_response_norm_const(dim, size)

    input = cast_to_ms_tensor(input)
    div = ms.ops.mul(input, input).expand_dims(axis=1)
    if dim == 3:
        div = _do_pad(div, _pad)
        div = ms.ops.avg_pool2d(div, (size, 1), stride=1).squeeze(1)
    else:
        shape = input.shape
        div = div.view(shape[0], 1, shape[1], shape[2], -1)
        div = _do_pad(div, _pad)
        div = _get_cache_prim(ms.ops.AvgPool3D)((size, 1, 1), strides=1)(div).squeeze(1)
        div = div.view(shape)
    div = div * alpha + k
    div = ms.ops.pow(div, beta)
    output = input / div
    return cast_to_adapter_tensor(output)


def one_hot(input, num_classes=-1):
    if num_classes == -1:
        depth = int(input.asnumpy().max()) + 1
    else:
        depth = num_classes

    input = cast_to_ms_tensor(input)
    on_value = ms.Tensor(1.0, ms.float32)
    off_value = ms.Tensor(0.0, ms.float32)
    out = ms.ops.one_hot(input, depth, on_value, off_value).astype(ms.int64)
    return cast_to_adapter_tensor(out)


def pixel_shuffle(input, upscale_factor):
    dim = input.dim()
    if dim < 3:
        raise RuntimeError("pixel_shuffle expects input to have at least 3 dimensions, "
                           "but got input with {} dimension(s)".format(dim))

    input = cast_to_ms_tensor(input)
    if dim == 3:
        input = input.expand_dims(0)
    shape_in = list(input.shape)
    tmp = input.reshape(-1, shape_in[-3], shape_in[-2], shape_in[-1])
    c = int(tmp.shape[-3] / upscale_factor / upscale_factor)
    if c * upscale_factor * upscale_factor != tmp.shape[-3]:
        raise RuntimeError(
            "pixel_shuffle expects its input's 'channel' dimension to be divisible by the square of upscale_factor,"
            "but input.size(-3)={} is not divisible by {}".format(tmp.shape[-3], upscale_factor*upscale_factor))
    h = tmp.shape[-2]
    w = tmp.shape[-1]

    tmp = tmp.reshape(-1, c, upscale_factor, upscale_factor, h, w).transpose(0, 1, 4, 2, 5, 3)
    out = tmp.reshape(-1, c, h * upscale_factor, w * upscale_factor)

    shape_in[-3] = c
    shape_in[-2] = h * upscale_factor
    shape_in[-1] = w * upscale_factor
    out = out.reshape(shape_in)
    if dim == 3:
        out = out.squeeze(0)
    return cast_to_adapter_tensor(out)


def pixel_unshuffle(input, downscale_factor):
    dim = input.dim()
    if dim < 3:
        raise RuntimeError("pixel_shuffle expects input to have at least 3 dimensions, "
                           "but got input with {} dimension(s)".format(dim))

    input = cast_to_ms_tensor(input)
    if dim == 3:
        input = input.expand_dims(0)
    shape_in = list(input.shape)
    tmp = input.reshape(-1, shape_in[-3], shape_in[-2], shape_in[-1])
    c = tmp.shape[-3]
    h = int(tmp.shape[-2] / downscale_factor)
    w = int(tmp.shape[-1] / downscale_factor)
    if h * downscale_factor != tmp.shape[-2]:
        raise RuntimeError(
            "pixel_unshuffle expects height to be divisible by downscale_factor, "
            "but input.size(-2)={} is not divisible by {}".format(tmp.shape[-2], downscale_factor))
    if w * downscale_factor != tmp.shape[-1]:
        raise RuntimeError(
            "pixel_unshuffle expects width to be divisible by downscale_factor, "
            "but input.size(-1)={} is not divisible by {}".format(tmp.shape[-1], downscale_factor))

    tmp = tmp.reshape(-1, c, h, downscale_factor, w, downscale_factor).transpose(0, 1, 3, 5, 2, 4)
    out = tmp.reshape(-1, c * downscale_factor * downscale_factor, h, w)

    shape_in[-3] = c * downscale_factor * downscale_factor
    shape_in[-2] = h
    shape_in[-1] = w
    out = out.reshape(shape_in)
    if dim == 3:
        out = out.squeeze(0)
    return cast_to_adapter_tensor(out)

def interpolate(input,
                size=None,
                scale_factor=None,
                mode='nearest',
                align_corners=None,
                recompute_scale_factor=None,
                antialias=False):

    unsupported_attr(recompute_scale_factor)
    unsupported_attr(antialias)

    if mode in ("nearest", "area", "nearest-exact"):
        if align_corners is not None:
            raise ValueError(
                "align_corners option can only be set with the "
                "interpolating modes: linear | bilinear | bicubic | trilinear"
            )
        align_corners = False
    else:
        if align_corners is None:
            align_corners = False

    if recompute_scale_factor is not None and recompute_scale_factor:
        # TODO: not support these two arguments until now
        pass

    if antialias:
        raise NotImplementedError("antialias in interpolate is not supported to True.")

    # TODO:　not support `antialias` until now.
    if antialias and not (mode in ("bilinear", "bicubic") and input.ndim == 4):
        raise ValueError("Anti-alias option is only supported for bilinear and bicubic modes")

    # TODO: 'nearest' only support 4D, 5D input. 3D is not support until now.
    if mode == 'nearest':
        if input.dim() not in (4, 5):
            raise NotImplementedError(f"For now, 'nearest' only 4D, 5D input are supported, but got {input.dim()}D")

        return upsample_nearest(input, size, scale_factor)

    # TODO: 'bilinear' only support 4D input. 3D, 5D are not support until now.
    if mode == 'bilinear':
        if input.dim() != 4:
            raise NotImplementedError(f"For now, 'bilinear' only 4D input is supported, but got {input.dim()}D")

        return upsample_bilinear(input, size, scale_factor, align_corners=align_corners)

    if mode == 'linear':
        if input.dim() != 3:
            raise ValueError(f"'linear' mode only support 3D input, but got {input.dim()}D")

        _size =_upsample_common_process_size(size, scale_factor, input.shape)

        input = cast_to_ms_tensor(input)
        out = ms.ops.interpolate(input, scale_factor=None, size=_size,
                                 align_corners=align_corners, mode=mode)
        return cast_to_adapter_tensor(out)

    if mode in ['bicubic', 'trilinear', 'area', 'nearest-exact']:
        raise NotImplementedError(f"For interpolate: currently not support mode '{mode}'")

    raise NotImplementedError(
        "Input Error: Only 3D, 4D and 5D input Tensors supported"
        " (got {}D) for the modes: nearest | linear | bilinear | bicubic | trilinear | area | nearest-exact"
        " (got {})".format(input.dim(), mode)
    )


def embedding(
    input,
    weight,
    padding_idx=None,
    max_norm=None,
    norm_type=2.0,
    scale_grad_by_freq=False,
    sparse=False
):
    unsupported_attr(scale_grad_by_freq)
    unsupported_attr(sparse)

    if padding_idx:
        raise NotImplementedError("nn.Embedding: `padding_idx` is not supported until now.")

    input = cast_to_ms_tensor(input)

    # TODO: to support padding_idx in the future
    # if padding_idx is not None:
    #     if padding_idx > 0:
    #         if padding_idx >= weight.shape[0]:
    #             raise ValueError("Padding_idx must be within num_embeddings")
    #     elif padding_idx < 0:
    #         if padding_idx < -weight.shape[0]:
    #             raise ValueError("Padding_idx must be within num_embeddings")
    #         padding_idx = weight.shape[0] + padding_idx

    # TODO: norm_type only support '2', others are not supported yet
    if norm_type != 2:
        raise NotImplementedError("`norm_type` beside 2 is not supported until now.")

    # TODO: Try to let 'weight[padding_idx]' not updating by gradient, but pynative didn't work.
    # Actually, when use "weight[padding_idx] = ...", it will create ops 'TensorScatterUpdate'
    # And 'TensorScatterUpdate''s backprop can meet that it would not pass gradient to weight[padding_idx].
    # However, when directly use 'TensorScatterUpdate', ops will be eliminated in graph optimization.
    # So, that is the problem to solve, which means the 'padding_idx' will be supported in the future.

    if max_norm:
        weight = _get_cache_prim(ms.nn.ClipByNorm)(axis=1)(weight, clip_norm=ms.ops.scalar_to_tensor(max_norm))

    out = ms.ops.gather(weight, input, axis=0)

    return cast_to_adapter_tensor(out)


def grid_sample(input, grid, mode='bilinear', padding_mode='zeros', align_corners=None):
    input = cast_to_ms_tensor(input)
    grid = cast_to_ms_tensor(grid)
    if align_corners is None:
        align_corners = False
    output = ms.ops.grid_sample(input, grid, mode=mode,
                                padding_mode=padding_mode, align_corners=align_corners)
    output = cast_to_adapter_tensor(output)
    return output


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _check_conv1d_input_shape(input_shape):
    if len(input_shape) != 3:
        raise ValueError(f"For 'conv1d', the dimension of input must be 3d, but got {len(input_shape)}.")


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_conv1d_const(stride, padding, dilation):
    if isinstance(stride, tuple):
        stride = stride[0]
    pad_mode = "pad"
    if isinstance(padding, int):
        padding = (0, padding)
    elif isinstance(padding, tuple):
        padding = (0, padding[0])
    else:
        pad_mode = padding
        padding = 0
    if isinstance(dilation, tuple):
        dilation = dilation[0]
    dilation = (1, dilation)
    return pad_mode, stride, padding, dilation


def conv1d(input, weight, bias=None, stride=1, padding=0, dilation=1, groups=1):
    # TODO: not support float64, change to float32 now
    input_ms = cast_to_ms_tensor(input)
    # do not cast weight because will lose gradient
    # weight_ms = cast_to_ms_tensor(weight)
    weight_ms = weight
    is_float64 = False
    if input_ms.dtype in (ms.float64, ms.double):
        input_ms = input_ms.astype(ms.float32)
        weight_ms = weight_ms.astype(ms.float32)
        is_float64 = True

    input_shape = input_ms.shape
    _check_conv1d_input_shape(input_shape)
    _pad_mode, _stride, _padding, _dilation = _get_conv1d_const(stride, padding, dilation)
    input_ms = ms.ops.expand_dims(input_ms, 2)
    weight_ms = ms.ops.expand_dims(weight_ms, 2)
    output = ms.ops.conv2d(input_ms, weight_ms, None, _stride, _pad_mode, _padding, _dilation, groups)
    if bias is not None:
        # TODO: ms.ops.biasadd also not support float64
        if bias.dtype != output.dtype:
            bias = bias.astype(output.dtype)
        output = ms.ops.bias_add(output, bias)
    output = ms.ops.squeeze(output, 2)

    if is_float64:
        output = output.astype(ms.float64)

    return cast_to_adapter_tensor(output)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_conv2d_const(stride, padding, dilation):
    if isinstance(stride, int):
        stride = (stride, stride)
    elif len(stride)==1:
        stride = (stride[0], stride[0])
    pad_mode = "pad"
    if isinstance(padding, int):
        padding = (padding, padding)
    elif isinstance(padding, tuple):
        if len(padding)==1:
            padding = (padding[0], padding[0])

    else:
        pad_mode = padding
        padding = 0
    if isinstance(dilation, int):
        dilation = (dilation, dilation)
    elif len(dilation) == 1:
        dilation = (dilation[0], dilation[0])
    return pad_mode, stride, padding, dilation


def conv2d(input, weight, bias=None, stride=1, padding=0, dilation=1, groups=1):
    # TODO: not support float64, change to float32 now
    input_ms = cast_to_ms_tensor(input)
    # can not cast 'weight' to 'weight_ms', because it will convert Parameter to Tensor, and will lost gradient.
    # ms.ops.conv do not use tensor function of ms.ops.con2d, so without cast_to_ms_tensor(weight), no effect
    # weight_ms = cast_to_ms_tensor(weight)
    weight_ms = weight
    is_float64 = False
    if input_ms.dtype in (ms.float64, ms.double):
        input_ms = input_ms.astype(ms.float32)
        weight_ms = weight_ms.astype(ms.float32)
        is_float64 = True

    _pad_mode, _stride, _padding, _dilation = _get_conv2d_const(stride, padding, dilation)
    output = ms.ops.conv2d(input_ms, weight_ms, None, _stride, _pad_mode, _padding, _dilation, groups)
    if bias is not None:
        # TODO: ms.ops.biasadd also not support float64
        if bias.dtype != output.dtype:
            bias = bias.astype(output.dtype)
        output = ms.ops.bias_add(output, bias)

    if is_float64:
        output = output.astype(ms.float64)

    return cast_to_adapter_tensor(output)

@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_maxpool2d_const_1(kernel_size, stride, padding):
    _kernel_size = kernel_size if isinstance(kernel_size, tuple) else (kernel_size, kernel_size)
    if stride is None:
        _stride = _kernel_size
    else:
        _stride = stride if isinstance(stride, tuple) else (stride, stride)

    _padding = padding if isinstance(padding, tuple) else (padding, padding)
    return _kernel_size, _stride, _padding


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_maxpool2d_const_2(kernel_size, stride, padding, dilation):
    _kernel_size = kernel_size + (1,) if isinstance(kernel_size, tuple) else (kernel_size, kernel_size, 1)
    if stride is None:
        _stride = _kernel_size
    else:
        _stride = stride + (1,) if isinstance(stride, tuple) else (stride, stride, 1)
    _padding = padding + (0,) if isinstance(padding, tuple) else (padding, padding, 0)
    _dilation = dilation + (1,) if isinstance(dilation, tuple) else (dilation, dilation, 1)
    return _kernel_size, _stride, _padding, _dilation


def max_pool2d(input, kernel_size, stride=None, padding=0, dilation=1,
               ceil_mode=False, return_indices=False):
    input = cast_to_ms_tensor(input)
    if input.dtype in all_int_type:
        raise TypeError("'max_pool2d' not implemented for int.")

    if return_indices is True or dilation != 1 or ceil_mode is True:
        _kernel_size, _stride, _padding, _dilation = _get_maxpool2d_const_2(kernel_size, stride, padding, dilation)
        input = cast_to_ms_tensor(input)
        ndim = input.ndim
        if ndim == 3:
            input = input.expand_dims(0)
            input = input.expand_dims(-1)
            out, indices = ms.ops.max_pool3d(input, _kernel_size, _stride, _padding, _dilation, ceil_mode, True)
            out = out.squeeze(0)
            indices = indices.squeeze(0)
        else:
            input = input.expand_dims(-1)
            out, indices = ms.ops.max_pool3d(input, _kernel_size, _stride, _padding, _dilation, ceil_mode, True)

        out = out.squeeze(-1)
        indices = indices.squeeze(-1)
        if return_indices:
            return cast_to_adapter_tensor((out, indices))
        return cast_to_adapter_tensor(out)
    else:
        _kernel_size, _stride, _pad = _get_maxpool2d_const_1(kernel_size, stride, padding)
        #TODO: this method do not support GRAPH_MODE
        #
        # _extra_pad_h = 0
        # _extra_pad_w = 0

        # if ceil_mode:
        #     _input_shape = ms.ops.shape(input)
        #     _valid_in_h = (_input_shape[2] + _padding[0] * 2 - _dilation[0] * (_kernel_size[0] - 1) - 1)
        #     _valid_out_h =  _valid_in_h // _stride[0]
        #     tmp = _valid_out_h * _stride[0]
        #     if  tmp < _valid_in_h:
        #         _extra_pad_h = tmp + _stride[0] - _valid_in_h

        #     _valid_in_w = (_input_shape[3] + _padding[1] * 2 - _dilation[1] * (_kernel_size[1] - 1) - 1)
        #     _valid_out_w = _valid_in_w // _stride[1]
        #     tmp = _valid_out_w * _stride[1]
        #     if  tmp < _valid_in_w:
        #         _extra_pad_w = tmp + _stride[1] - _valid_in_w

        # _pad = (((0, 0), (0, 0),
        #          (_padding[0], _padding[0] + _extra_pad_h), (_padding[1], _padding[1] + _extra_pad_w)))

        #_pad = (_padding[1], _padding[1] + _extra_pad_w, _padding[0], _padding[0] + _extra_pad_h)
        #neg_inf = -float('inf')
        _max_pool = ms.ops.MaxPool(kernel_size=_kernel_size, strides=_stride, pad_mode='valid')
        ndim = input.ndim
        if ndim == 3:
            input = input.expand_dims(0)
            input = _do_pad(input, _pad, value=-float('inf'))
            out = _max_pool(input)
            out = out.squeeze(0)
        else:
            input = _do_pad(input, _pad, value=-float('inf'))
            out = _max_pool(input)
        return cast_to_adapter_tensor(out)

def max_unpool1d(input, indices, kernel_size, stride, padding, output_size = None):
    input = cast_to_ms_tensor(input)
    indices = cast_to_ms_tensor(indices)
    if output_size is not None:
        output_size = tuple(output_size)
    out = ms.ops.max_unpool1d(input, indices, kernel_size, stride, padding, output_size)
    return out

def max_unpool2d(input, indices, kernel_size, stride, padding, output_size = None):
    input = cast_to_ms_tensor(input)
    indices = cast_to_ms_tensor(indices)
    if output_size is not None:
        output_size = tuple(output_size)
    out = ms.ops.max_unpool2d(input, indices, kernel_size, stride, padding, output_size)
    return out

def max_unpool3d(input, indices, kernel_size, stride, padding, output_size = None):
    input = cast_to_ms_tensor(input)
    indices = cast_to_ms_tensor(indices)
    if output_size is not None:
        output_size = tuple(output_size)
    out = ms.ops.max_unpool3d(input, indices, kernel_size, stride, padding, output_size)
    return cast_to_adapter_tensor(out)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_linear_output_shape(input_shape, weight_shape, input_rank, weight_rank):
    shape_out= ()
    if input_rank > 1:
        shape_out = shape_out + input_shape[:-1]
    if weight_rank == 2:
        shape_out = shape_out + (weight_shape[0],)
    return shape_out

@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _check_linear_shape(weight_rank, input_shape, weight_shape):
    if weight_rank not in (1, 2):
        raise ValueError("For nn.functional.linear, weight only support 2D or 1D input"
                            f"but got {weight_rank}D input")

    if input_shape[-1] != weight_shape[-1]:
        raise ValueError("For nn.functional.linear, size mismatch,"
                            f"got input with shape {input_shape}, and weight with shape {weight_shape}.")

def linear(input, weight, bias=None):
    input = cast_to_ms_tensor(input)

    dtype_op = _get_cache_prim(ms.ops.DType)()
    rank_op = _get_cache_prim(ms.ops.Rank)()
    shape_op = _get_cache_prim(ms.ops.Shape)()
    reshape_op = _get_cache_prim(ms.ops.Reshape)()
    bias_add_op = _get_cache_prim(ms.ops.BiasAdd)()

    dtype1 = dtype_op(input)
    dtype2 = dtype_op(weight)
    if not _check_same_type(dtype1, dtype2):
        input = input.astype(ms.float32)
        weight = weight.astype(ms.float32)

    input_rank, weight_rank = rank_op(input), rank_op(weight)
    input_shape, weight_shape = shape_op(input), shape_op(weight)
    _check_linear_shape(weight_rank, input_shape, weight_shape)

    # infers the shape of the output
    shape_out = _get_linear_output_shape(input_shape, weight_shape, input_rank, weight_rank)

    _matmul = _get_cache_prim(ms.ops.MatMul)(False, True)

    input = _expand(input, 2)
    weight = _expand(weight, 2)

    if rank_op(input) > 2:
        input = reshape_op(input, (-1, input_shape[-1]))
    output = _matmul(input, weight)
    if bias is not None:
        bias = _expand(bias, 1)
        # if output's rank bigger than 5, using output = ms.ops.add(output, bias)
        output = bias_add_op(output, bias)
    output = reshape_op(output, shape_out)
    output = cast_to_adapter_tensor(output)
    return output

def bilinear(input1, input2, weight, bias=None):
    input1 = cast_to_ms_tensor(input1)
    input2 = cast_to_ms_tensor(input2)
    weight = cast_to_ms_tensor(weight)
    x = ms.ops.matmul(input1.reshape(-1, input1.shape[-1]),
                      weight.permute(1, 0, 2).reshape(weight.shape[1], -1))
    x = ms.ops.mul(x, ms.ops.tile(input2.reshape(-1, input2.shape[-1]), (1, weight.shape[0])))
    x = x.reshape(x.shape[0], weight.shape[0], -1)
    x = ms.ops.reduce_sum(x, -1)
    if bias is not None:
        bias = cast_to_ms_tensor(bias)
        x = ms.ops.bias_add(x, bias)
    output = x.reshape(*input1.shape[:-1], -1)
    return cast_to_adapter_tensor(output)

def lp_pool1d(input, norm_type, kernel_size, stride = None, ceil_mode = False):
    input = cast_to_ms_tensor(input)
    output = ms.ops.lp_pool1d(input, norm_type, kernel_size, stride, ceil_mode)
    return cast_to_adapter_tensor(output)


def lp_pool2d(input, norm_type, kernel_size, stride = None, ceil_mode = False):
    input = cast_to_ms_tensor(input)
    output = ms.ops.lp_pool2d(input, norm_type, kernel_size, stride, ceil_mode)
    return cast_to_adapter_tensor(output)

def fractional_max_pool2d(input_x, kernel_size, output_size=None, output_ratio=None, return_indices=False,
                          _random_samples=None):
    input_ms = cast_to_ms_tensor(input_x)
    out = ms.ops.fractional_max_pool2d(input_ms, kernel_size, output_size, output_ratio, return_indices,
                                       _random_samples)
    return cast_to_adapter_tensor(out)

def fractional_max_pool3d(input_x, kernel_size, output_size=None, output_ratio=None, return_indices=False,
                          _random_samples=None):
    input_ms = cast_to_ms_tensor(input_x)
    out = ms.ops.fractional_max_pool3d(input_ms, kernel_size, output_size, output_ratio, return_indices,
                                       _random_samples)
    return cast_to_adapter_tensor(out)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_avg_pool1d_const(kernel_size, stride, padding):
    if isinstance(kernel_size, int):
        kernel_size = (kernel_size, 1)
    else:
        kernel_size = kernel_size + (1,)
    if stride is None:
        stride = (kernel_size, 1)
    elif isinstance(stride, int):
        stride = (stride, 1)
    else:
        stride = stride + (1,)
    pad = (padding, 0)
    return pad, kernel_size, stride

def avg_pool1d(input, kernel_size, stride=None, padding=0, ceil_mode=False, count_include_pad=True):
    unsupported_attr(ceil_mode)
    unsupported_attr(count_include_pad)

    _pad, _kernel_size, _stride = _get_avg_pool1d_const(kernel_size, stride, padding)

    avg_pool_ops = ms.ops.AvgPool(kernel_size=_kernel_size, strides=_stride, pad_mode='valid')

    input = cast_to_ms_tensor(input)
    ndim = input.ndim
    if ndim == 2:
        input = input.expand_dims(0)
        input = input.expand_dims(-1)
        input = _do_pad(input, _pad)
        out = avg_pool_ops(input)
        out = out.squeeze(-1)
        out = out.squeeze(0)
    else:
        input = input.expand_dims(-1)
        input = _do_pad(input, _pad)
        out = avg_pool_ops(input)
        out = out.squeeze(-1)
    return cast_to_adapter_tensor(out)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_avg_pool3d_const(kernel_size, stride, padding, divisor_override):
    if stride is None:
        _stride = kernel_size
    else:
        _stride = stride
    if divisor_override is None:
        _divisor_override = 0
    else:
        _divisor_override = divisor_override

    if isinstance(padding, tuple):
        if len(padding) == 3:
            _padding = (padding[0], padding[0], padding[1], padding[1], padding[2], padding[2])
        else:
            raise ValueError(f"For avg_pool3d, len tuple padding should be 3, but got {padding}.")
    else:
        _padding = padding

    return _stride, _padding, _divisor_override

def avg_pool3d(input, kernel_size, stride=None, padding=0,
               ceil_mode=False, count_include_pad=True, divisor_override=None):
    input_ms = cast_to_ms_tensor(input)
    _stride, _padding, _divisor_override = _get_avg_pool3d_const(kernel_size, stride, padding, divisor_override)
    if input_ms.ndim == 4:
        _input_ms = input_ms[None,...]
        out = ms.ops.avg_pool3d(_input_ms, kernel_size, _stride, _padding, ceil_mode, count_include_pad,
                                _divisor_override)
        out = out.squeeze(0)
    else:
        out = ms.ops.avg_pool3d(input_ms, kernel_size, _stride, _padding, ceil_mode, count_include_pad,
                                _divisor_override)
    return cast_to_adapter_tensor(out)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_maxpool1d_const_1(kernel_size, stride, padding, dilation):
    if isinstance(kernel_size, int):
        _kernel_size = (kernel_size, 1, 1)
    elif isinstance(kernel_size, tuple):
        _kernel_size = kernel_size + (1, 1)
    else:
        _kernel_size = kernel_size

    if stride is None:
        _stride = (kernel_size, 1, 1)
    elif isinstance(stride, int):
        _stride = (stride, 1, 1)
    elif isinstance(stride, tuple):
        _stride = stride + (1, 1)
    else:
        _stride = stride

    _padding = (padding, 0, 0)
    _dilation = (dilation, 1, 1)
    return _kernel_size, _stride, _padding, _dilation


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_maxpool1d_const_2(kernel_size, stride, padding):
    _kernel_size = (1, kernel_size)
    if stride is None:
        _stride = _kernel_size
    else:
        _stride = (1, stride)
    _padding = (0, padding)
    # _dilation = (1, dilation)
    return _padding, _kernel_size, _stride

def max_pool1d(input, kernel_size, stride=None, padding=0, dilation=1, ceil_mode=False, return_indices=False):
    input = cast_to_ms_tensor(input)
    if input.dtype in all_int_type:
        raise TypeError("'max_pool1d' not implemented for int.")
    if return_indices is True or dilation != 1 or ceil_mode is True:
        if input.ndim == 2:
            _input_ms = input[None,...,None,None]
        elif input.ndim == 3:
            _input_ms = input[..., None, None]
        else:
            _input_ms = input

        _kernel_size, _stride, _padding, _dilation = _get_maxpool1d_const_1(kernel_size, stride, padding, dilation)

        out = ms.ops.max_pool3d(_input_ms, _kernel_size, _stride, _padding, _dilation, ceil_mode, return_indices)

        if isinstance(out, tuple):
            out = list(out)
            for id, value in enumerate(out):
                out[id] = value.squeeze(-1).squeeze(-1)
                if input.ndim == 2:
                    out[id] = out[id].squeeze(0)
            out = tuple(out)
        else:
            out = out.squeeze(-1).squeeze(-1)
            if input.ndim == 2:
                out = out.squeeze(0)

        return cast_to_adapter_tensor(out)
    else:
        _pad, _kernel_size, _stride = _get_maxpool1d_const_2(kernel_size, stride, padding)
        # _pad = (_padding[1], _padding[1] + _extra_pad_w, _padding[0], _padding[0])
        # neg_inf = -float('inf')
        _max_pool = ms.ops.MaxPool(kernel_size=_kernel_size, strides=_stride, pad_mode='valid')
        ndim = input.ndim
        if ndim == 2:
            input = input.expand_dims(0)
            input = input.expand_dims(2)
            input = _do_pad(input, _pad, value=-float('inf'))
            out = _max_pool(input)
            out = out.squeeze(2)
            out = out.squeeze(0)
        else:
            input = input.expand_dims(2)
            input = _do_pad(input, _pad, value=-float('inf'))
            out = _max_pool(input)
            out = out.squeeze(2)
        return cast_to_adapter_tensor(out)


def max_pool3d(input, kernel_size, stride=None, padding=0, dilation=1, ceil_mode=False, return_indices=False):
    input_ms = cast_to_ms_tensor(input)
    if input_ms.ndim == 4:
        _input_ms = input_ms[None, ...]
    else:
        _input_ms = input_ms

    out = ms.ops.max_pool3d(_input_ms, kernel_size, stride, padding, dilation, ceil_mode, return_indices)

    if input_ms.ndim == 4:
        if isinstance(out, tuple):
            out = list(out)
            for id, value in enumerate(out):
                out[id] = value.squeeze(0)
            out = tuple(out)
        else:
            out = out.squeeze(0)

    return cast_to_adapter_tensor(out)


def conv_transpose1d(inputs, weight, bias=None, stride=1, padding=0, output_padding=0, groups=1, dilation=1):
    inputs = cast_to_ms_tensor(inputs)
    weight = cast_to_ms_tensor(weight)
    has_bias = bias is not None
    bias = cast_to_ms_tensor(bias) if bias is not None else 'zeros'
    if len(inputs.shape) != 3:
        raise ValueError("the rank of inputs tensor should be 3.")
    if len(weight.shape) != 3:
        raise ValueError("the rank of weight tensor should be 3")
    in_channel = inputs.shape[1]
    out_channel = weight.shape[1] * groups
    kernel_size = weight.shape[2]
    if stride != 1 and padding == (kernel_size - 1) // 2 and output_padding == stride - 1:
        pad_mode = 'same'
        padding = 0
        raise Warning("pad_mode = same is some thing wrong, please switch to others")
    elif stride != 1 and padding == 0 and output_padding == 0:
        pad_mode = 'valid'
        padding = 0
    else:
        pad_mode = 'pad'
    _conv_1d_transpose = nn.Conv1dTranspose(
        in_channels=in_channel, out_channels=out_channel, kernel_size=kernel_size, stride=stride,
        pad_mode=pad_mode, padding=padding, dilation=dilation, group=groups, has_bias=has_bias,
        weight_init=weight, bias_init=bias)
    out = _conv_1d_transpose(inputs)
    return cast_to_adapter_tensor(out)


def conv_transpose2d(inputs, weight, bias=None, stride=1, padding=0, output_padding=0, groups=1, dilation=1):
    inputs = cast_to_ms_tensor(inputs)
    weight = cast_to_ms_tensor(weight)
    has_bias = bias is not None
    bias = cast_to_ms_tensor(bias) if bias is not None else 'zeros'
    if len(inputs.shape) != 4:
        raise ValueError("the rank of inputs tensor should be 4.")
    if len(weight.shape) != 4:
        raise ValueError("the rank of weight tensor should be 4")
    in_channel = inputs.shape[1]
    out_channel = weight.shape[1] * groups
    kernel_size = weight.shape[2:]
    if isinstance(padding, tuple):
        padding = list(np.repeat(padding, 2))
        # convert default data type 'int64' to 'int'
        padding = tuple(map(int, padding))
    if stride != 1 and padding == 0 and output_padding == 0:
        pad_mode = 'valid'
        padding = 0
    else:
        pad_mode = 'pad'
    _conv_2d_transpose = nn.Conv2dTranspose(
        in_channels=in_channel, out_channels=out_channel, kernel_size=kernel_size, stride=stride,
        pad_mode=pad_mode, padding=padding, dilation=dilation, group=groups, has_bias=has_bias,
        weight_init=weight, bias_init=bias)
    out = _conv_2d_transpose(inputs)
    return cast_to_adapter_tensor(out)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_conv_transpose3d_const(input_shape, weight_shape, groups, padding):
    if len(input_shape) != 5:
        raise ValueError("the rank of inputs tensor should be 5.")
    if len(weight_shape) != 5:
        raise ValueError("the rank of weight tensor should be 5")

    in_channel = input_shape[1]
    out_channel = weight_shape[1] * groups
    kernel_size = weight_shape[2:]
    pad_mode = 'pad'
    if isinstance(padding, int):
        ms_padding = padding
    else:
        ms_padding = _repeat_tuple(padding, 2)
    return in_channel, out_channel, kernel_size, pad_mode, ms_padding

def conv_transpose3d(input, weight, bias=None, stride=1, padding=0, output_padding=0, groups=1, dilation=1):
    input = cast_to_ms_tensor(input)
    # do not cast weight and bias to ms_tensor, because will cause lost gradient
    # weight = cast_to_ms_tensor(weight)
    # bias = cast_to_ms_tensor(bias) if bias is not None else bias
    in_channel, out_channel, kernel_size, pad_mode, ms_padding = _get_conv_transpose3d_const(input.shape,
                                                                                             weight.shape,
                                                                                             groups,
                                                                                             padding)

    _conv_3d_transpose = _get_cache_prim(ms.ops.Conv3DTranspose)(in_channel= in_channel,
                                                                 out_channel=out_channel,
                                                                 kernel_size=kernel_size,
                                                                 mode=1,
                                                                 pad_mode=pad_mode,
                                                                 pad=ms_padding,
                                                                 stride=stride,
                                                                 dilation=dilation,
                                                                 group=groups,
                                                                 output_padding=output_padding,
                                                                 data_format='NCDHW')

    # ms.ops.Conv3DTranspose not supported bias yet
    out = _conv_3d_transpose(input, weight)
    if bias is not None:
        out = _get_cache_prim(ms.ops.BiasAdd)(data_format='NCDHW')(out, bias)
    return cast_to_adapter_tensor(out)


def affine_grid(theta, size, align_corners=None):
    theta = cast_to_ms_tensor(theta)
    if align_corners is None:
        align_corners = False

    # TODO：the input argument[theta] must be a type of {Tensor[Float16], Tensor[Float32]}
    if theta.dtype == ms.float64:
        theta = theta.astype(ms.float32)
    output = ms.ops.affine_grid(theta, size, align_corners)
    return cast_to_adapter_tensor(output)


def batch_norm(inputs, running_mean, running_var, weight=None, bias=None, training=False, momentum=0.1,
               eps=1e-05):
    inputs = cast_to_ms_tensor(inputs)
    running_mean = cast_to_ms_tensor(running_mean)
    running_var = cast_to_ms_tensor(running_var)
    weight = cast_to_ms_tensor(weight) if weight is not None else weight
    bias = cast_to_ms_tensor(bias) if bias is not None else bias
    reduced_dim = tuple(i for i in range(inputs.dim()) if i != 1)
    normalized_shape = [1] * len(inputs.shape)
    normalized_shape[1] = inputs.shape[1]
    if training:
        mean = inputs.mean(axis=reduced_dim, keep_dims=True)
        var = inputs.var(reduced_dim, keepdims=True, ddof=False)
        mean_update = mean.squeeze()
        var_update = inputs.var(axis=reduced_dim, ddof=True)
        out = (inputs - mean) / ms.ops.sqrt(var + eps)
        # parameters updating reserved for future use
        running_mean = (1 - momentum) * running_mean + momentum * mean_update
        running_var = (1 - momentum) * running_var + momentum * var_update
    else:
        out = (inputs - running_mean.view(*normalized_shape)) / ms.ops.sqrt(running_var.view(*normalized_shape) + eps)
    if weight is not None:
        out = out * weight.view(*normalized_shape)
    if bias is not None:
        out = out + bias.view(*normalized_shape)
    return cast_to_adapter_tensor(out)


def group_norm(inputs, num_groups, weight=None, bias=None, eps=1e-05):
    inputs = cast_to_ms_tensor(inputs)
    weight = cast_to_ms_tensor(weight) if weight is not None else weight
    bias = cast_to_ms_tensor(bias) if bias is not None else bias
    inputs_shape = list(inputs.shape)
    shape = [inputs_shape[0]] + [num_groups, inputs_shape[1] // num_groups] + inputs_shape[2:]
    normalized_shape = [1] * len(inputs.shape)
    normalized_shape[1] = inputs_shape[1]
    reduced_dim = tuple(i for i in range(len(shape) - 1, 1, -1))
    inputs = inputs.reshape(*shape)
    mean = inputs.mean(axis=reduced_dim, keep_dims=True)
    var = inputs.var(axis=reduced_dim, keepdims=True, ddof=False)
    out = (inputs - mean) / ms.ops.sqrt(var + eps)
    out = out.reshape(*inputs_shape)
    if weight is not None:
        out = out * weight.view(*normalized_shape)
    if bias is not None:
        out = out + bias.view(*normalized_shape)
    return cast_to_adapter_tensor(out)


def instance_norm(inputs, running_mean=None, running_var=None, weight=None, bias=None, use_input_stats=True,
                  momentum=0.1, eps=1e-05):
    inputs = cast_to_ms_tensor(inputs)
    running_mean = cast_to_ms_tensor(running_mean)
    running_var = cast_to_ms_tensor(running_var)
    weight = cast_to_ms_tensor(weight) if weight is not None else weight
    bias = cast_to_ms_tensor(bias) if bias is not None else bias
    reduced_dim = tuple(i for i in range(inputs.dim()) if i not in [0, 1])
    normalized_shape = [1] * len(inputs.shape)
    normalized_shape[1] = inputs.shape[1]

    shape = [1] * len(inputs.shape)
    shape[:2] = inputs.shape[:2]

    if use_input_stats:
        mean = inputs.mean(axis=reduced_dim)
        var = inputs.var(axis=reduced_dim, ddof=False)
        mean_update = mean.mean(0)
        var_update = inputs.var(axis=reduced_dim, ddof=True).mean(0)
        out = (inputs - mean.view(*shape)) / ms.ops.sqrt(var.view(*shape) + eps)
        running_mean = (1 - momentum) * running_mean + momentum * mean_update
        running_var = (1 - momentum) * running_var + momentum * var_update
    else:
        out = (inputs - running_mean.view(*normalized_shape)) \
                     / ms.ops.sqrt(running_var.view(*normalized_shape) + eps)
    if weight is not None:
        out = out * weight.view(*normalized_shape)
    if bias is not None:
        out = out + bias.view(*normalized_shape)
    return cast_to_adapter_tensor(out)


def layer_norm(inputs, normalized_shape, weight=None, bias=None, eps=1e-05):
    inputs = cast_to_ms_tensor(inputs)
    if weight is not None:
        weight = cast_to_ms_tensor(weight)
    else:
        weight = ms.Tensor(np.ones(normalized_shape), inputs.dtype)
    if bias is not None:
        bias = cast_to_ms_tensor(bias)
    else:
        bias = ms.Tensor(np.zeros(normalized_shape), inputs.dtype)

    if inputs.shape[-len(normalized_shape):] != normalized_shape:
        raise ValueError("For layer_norm, normalized_shape should fit inputs' shape"
                         f"but got input_shape: {inputs.shape}, normalized_shape: {normalized_shape}")
    _layer_norm = ms.ops.LayerNorm(epsilon=eps)
    out = _layer_norm(inputs, weight, bias)
    return cast_to_adapter_tensor(out[0])


def prelu(input, weight):
    #TODO:ms.ops.prelu only suports float16 and float32, not float64.
    input = cast_to_ms_tensor(input)
    # weight will be Parameter and can not be cast to tensor, will lost weights.
    # ms.ops.prelu do not use tensor function of weight, so without cast_to_ms_tensor(weight), not effect.
    # weight = cast_to_ms_tensor(weight)
    if is_under_ascend_context() and input.ndim < 2:
        shape = input.shape
        input = _expand(input, 2)
        output = ms.ops.prelu(input, weight)
        output = output.reshape(shape)
    else:
        output = ms.ops.prelu(input, weight)
    return cast_to_adapter_tensor(output)


def poisson_nll_loss(input, target, log_input=True, full=False, size_average=None, eps=1e-08, reduce=None,
                     reduction='mean'):
    input_ms = cast_to_ms_tensor(input)
    target = cast_to_ms_tensor(target)
    pi = 3.141592653589793
    if reduce is not None or size_average is not None:
        reduction = _get_reduce_string(size_average, reduce)
    if reduction not in ('none', 'mean', 'sum'):
        raise ValueError(reduction + " is not valid")

    if log_input:
        ret = ms.ops.exp(input) - target * input
    else:
        ret = input_ms - target * ms.ops.log(input_ms + eps)
    if full:
        cond = ms.ops.gt(target, 1)
        out = target * ms.ops.log(target) - target + 0.5 * ms.ops.log(2 * pi * target)
        out = ms.ops.select(cond, out, ms.ops.zeros_like(input_ms))
        ret = ret + out
    if reduction == "mean":
        ret = ms.ops.mean(ret)
    elif reduction == "sum":
        ret = ms.ops.sum(ret)
    return cast_to_adapter_tensor(ret)


def triplet_margin_with_distance_loss(anchor, positive, negative, *, distance_function=None, margin=1.0,
                                      swap=False, reduction='mean'):
    distance_function = distance_function if distance_function is not None else pairwise_distance

    anchor = cast_to_ms_tensor(anchor)
    positive = cast_to_ms_tensor(positive)
    negative = cast_to_ms_tensor(negative)
    positive_dist = distance_function(anchor, positive)
    negative_dist = distance_function(anchor, negative)

    if swap:
        swap_dist = distance_function(positive, negative)
        negative_dist = ms.ops.minimum(negative_dist, swap_dist)

    output = ms.ops.clamp(positive_dist - negative_dist + margin, min=0.0)

    if reduction == "mean":
        ret = output.mean()
    elif reduction == "sum":
        ret = output.sum()
    else:
        ret = output
    return cast_to_adapter_tensor(ret)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _get_conv3d_const(stride, padding, dilation):
    if isinstance(stride, int):
        stride = (stride, stride, stride)
    elif len(stride)==1:
        stride = (stride[0], stride[0], stride[0])
    pad_mode = "pad"
    if isinstance(padding, int):
        padding = (padding, padding, padding)
    elif isinstance(padding, tuple):
        if len(padding)==1:
            padding = (padding[0], padding[0], padding[0])

    else:
        pad_mode = padding
        padding = 0
    if isinstance(dilation, int):
        dilation = (dilation, dilation, dilation)
    elif len(dilation) == 1:
        dilation = (dilation[0], dilation[0], dilation[0])
    return pad_mode, padding, stride, dilation


def conv3d(input, weight, bias=None, stride=1, padding=0, dilation=1, groups=1):
    # Todo: not support float64, change to float32 now
    input_ms = cast_to_ms_tensor(input)
    weight_ms = cast_to_ms_tensor(weight)
    is_float64 = False
    if input_ms.dtype in (ms.float64, ms.double):
        input_ms = input_ms.astype(ms.float32)
        weight_ms = weight_ms.astype(ms.float32)
        is_float64 = True

    _pad_mode, _padding, _stride, _dilation = _get_conv3d_const(stride, padding, dilation)
    output = ms.ops.conv3d(input_ms, weight_ms, None, _stride, _pad_mode, _padding, _dilation, groups)
    if bias is not None:
        # TODO: ms.ops.biasadd also not support float64
        if bias.dtype != output.dtype:
            bias = bias.astype(output.dtype)
        output = ms.ops.bias_add(output, bias)

    if is_float64:
        output = output.astype(ms.float64)

    return cast_to_adapter_tensor(output)


def unfold(input, kernel_size, dilation=1, padding=0, stride=1):
    # TODO: do not support on GPU
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.unfold(input_ms, kernel_size, dilation, padding, stride)
    output = output.reshape(output.shape[0], output.shape[1] * output.shape[2], -1)
    return cast_to_adapter_tensor(output)


def fold(input, output_size, kernel_size, dilation=1, padding=0, stride=1):
    # TODO: do not support on Ascend
    input_ms = cast_to_ms_tensor(input)
    ndim = input_ms.ndim
    if ndim == 2:
        input_ms = input_ms.expand_dims(0)
    shape = input_ms.shape
    if isinstance(kernel_size, int):
        shape_tmp = kernel_size * kernel_size
    else:
        shape_tmp = kernel_size[0] * kernel_size[1]
    input_ms = input_ms.reshape(shape[0], -1, shape_tmp, shape[2])
    output = ms.ops.fold(input_ms, ms.Tensor(output_size), kernel_size, dilation, padding, stride)
    if ndim == 2:
        output = output.squeeze(0)
    return cast_to_adapter_tensor(output)

def multi_head_attention_forward(query, key, value, embed_dim_to_check, num_heads, in_proj_weight,
                                 in_proj_bias, bias_k, bias_v, add_zero_attn, dropout_p, out_proj_weight,
                                 out_proj_bias, training=True, key_padding_mask=None, attn_mask=None,
                                 use_separate_proj_weight=False, q_proj_weight=None, k_proj_weight=None,
                                 v_proj_weight=None, static_k=None, static_v=None, average_attn_weights=True,
                                 k_is_v=False, q_is_k=False):
    query = cast_to_ms_tensor(query)
    key = cast_to_ms_tensor(key)
    value = cast_to_ms_tensor(value)
    key_padding_mask = cast_to_ms_tensor(key_padding_mask)
    attn_mask = cast_to_ms_tensor(attn_mask)
    static_k = cast_to_ms_tensor(static_k)
    static_v = cast_to_ms_tensor(static_v)
    in_proj_weight = ms.ops.Identity()(in_proj_weight) if in_proj_weight is not None else None
    in_proj_bias = ms.ops.Identity()(in_proj_bias) if in_proj_bias is not None else None
    bias_k = ms.ops.Identity()(bias_k) if bias_k is not None else None
    bias_v = ms.ops.Identity()(bias_v) if bias_v is not None else None
    out_proj_weight = ms.ops.Identity()(out_proj_weight) if out_proj_weight is not None else None
    out_proj_bias = ms.ops.Identity()(out_proj_bias) if out_proj_bias is not None else None
    q_proj_weight = ms.ops.Identity()(q_proj_weight) if q_proj_weight is not None else None
    k_proj_weight = ms.ops.Identity()(k_proj_weight) if k_proj_weight is not None else None
    v_proj_weight = ms.ops.Identity()(v_proj_weight) if v_proj_weight is not None else None
    # TODO: older ver of torch doesn't have is_causal arg
    attn_output, attn_output_weights = ms.ops.function.nn_func.multi_head_attention_forward(
        query, key, value, embed_dim_to_check, num_heads,
        in_proj_weight, in_proj_bias, bias_k, bias_v, add_zero_attn, dropout_p,
        out_proj_weight, out_proj_bias, training=training,
        key_padding_mask=key_padding_mask, attn_mask=attn_mask,
        use_separate_proj_weight=use_separate_proj_weight,
        q_proj_weight=q_proj_weight, k_proj_weight=k_proj_weight,
        v_proj_weight=v_proj_weight, static_k=static_k, static_v=static_v,
        average_attn_weights=average_attn_weights, k_is_v=k_is_v, q_is_k=q_is_k)
    return cast_to_adapter_tensor(attn_output), cast_to_adapter_tensor(attn_output_weights)
