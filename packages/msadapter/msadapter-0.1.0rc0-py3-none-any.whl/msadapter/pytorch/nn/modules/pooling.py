#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Iterable

import mindspore as ms
from mindspore.ops import operations as P
from mindspore.ops import functional as F
from mindspore.ops._primitive_cache import _get_cache_prim

import msadapter.pytorch.nn.functional as Adapter_F
from msadapter.utils import unsupported_attr, is_under_ascend_context
from msadapter.pytorch.tensor import cast_to_ms_tensor, cast_to_adapter_tensor
from .module import Module

__all__ = ['MaxPool1d', 'MaxPool2d', 'MaxPool3d',
           'AvgPool1d', 'AvgPool2d', 'AvgPool3d',
           'AdaptiveAvgPool1d', 'AdaptiveAvgPool2d', 'AdaptiveAvgPool3d',
           'AdaptiveMaxPool1d', 'AdaptiveMaxPool2d', 'AdaptiveMaxPool3d',
           'LPPool1d', 'LPPool2d', 'FractionalMaxPool2d', 'FractionalMaxPool3d']

class _MaxPoolNd(Module):
    def __init__(self, kernel_size, stride=None, padding=0, dilation=1, return_indices=False, ceil_mode=False):
        super(_MaxPoolNd, self).__init__()
        self.kernel_size = kernel_size
        self.stride = stride if (stride is not None) else kernel_size
        self.padding = padding
        self.dilation = dilation
        self.return_indices = return_indices
        self.ceil_mode = ceil_mode

    def extra_repr(self):
        return 'kernel_size={kernel_size}, stride={stride}, padding={padding}' \
            ', dilation={dilation}, ceil_mode={ceil_mode}'.format(**self.__dict__)


class MaxPool1d(_MaxPoolNd):
    def forward(self, input):
        input = cast_to_ms_tensor(input)
        output = Adapter_F.max_pool1d(input, self.kernel_size, self.stride, self.padding, self.dilation,
                                    self.ceil_mode, self.return_indices)
        return cast_to_adapter_tensor(output)


class MaxPool2d(_MaxPoolNd):
    def __init__(self, kernel_size=1, stride=None, padding=0, dilation=1, return_indices=False, ceil_mode=False):
        super(MaxPool2d, self).__init__(kernel_size, stride, padding, dilation, return_indices, ceil_mode)

    def forward(self, input):
        return Adapter_F.max_pool2d(input, self.kernel_size, self.stride, self.padding, self.dilation,
                                    self.ceil_mode, self.return_indices)


class MaxPool3d(_MaxPoolNd):
    def __init__(self, kernel_size=1, stride=None, padding=0, dilation=1, return_indices=False, ceil_mode=False):
        super(MaxPool3d, self).__init__(kernel_size, stride, padding, dilation, return_indices, ceil_mode)

    def forward(self, input):
        return Adapter_F.max_pool3d(input, self.kernel_size, self.stride, self.padding, self.dilation,
                                    self.ceil_mode, self.return_indices)


class _AvgPoolNd(Module):
    def __init__(self, kernel_size, stride=None, padding=0, ceil_mode=False, count_include_pad=True,
                 divisor_override = None):
        super(_AvgPoolNd, self).__init__()
        self.kernel_size = kernel_size
        self.stride = stride if (stride is not None) else kernel_size
        self.padding = padding
        self.ceil_mode = ceil_mode
        self.count_include_pad = count_include_pad
        self.divisor_override = divisor_override

        unsupported_attr(ceil_mode)
        unsupported_attr(count_include_pad)
        unsupported_attr(divisor_override)
        if ceil_mode is True or count_include_pad is False or divisor_override is not None:
            raise NotImplementedError("These parameters cannot be set now.")

    def extra_repr(self):
        return 'kernel_size={}, stride={}, padding={}'.format(
            self.kernel_size, self.stride, self.padding
        )


class AvgPool1d(_AvgPoolNd):
    def __init__(self, kernel_size, stride=None, padding=0, ceil_mode=False, count_include_pad=True):
        super(AvgPool1d, self).__init__(kernel_size, stride, padding, ceil_mode, count_include_pad)
        self.padding = padding
        self.kernel_size = kernel_size

    def forward(self, input):
        return Adapter_F.avg_pool1d(input, kernel_size=self.kernel_size, stride=self.stride, padding=self.padding)


class AvgPool2d(_AvgPoolNd):
    def __init__(self, kernel_size, stride=None, padding=0, ceil_mode=False, count_include_pad=True,
                 divisor_override=None):
        super(AvgPool2d, self).__init__(kernel_size, stride, padding, ceil_mode, count_include_pad, divisor_override)
        self.padding = padding
        self.kernel_size = kernel_size

    def forward(self, input):
        return Adapter_F.avg_pool2d(input, kernel_size=self.kernel_size, stride=self.stride, padding=self.padding)


class AvgPool3d(_AvgPoolNd):
    def forward(self, input):
        return Adapter_F.avg_pool3d(input, kernel_size=self.kernel_size, stride=self.stride, padding=self.padding,
                                    ceil_mode=self.ceil_mode)


class _AdaptiveAvgPoolNd(Module):
    def __init__(self, output_size):
        super(_AdaptiveAvgPoolNd, self).__init__()
        self.output_size = output_size

    def extra_repr(self):
        return 'output_size={}'.format(self.output_size)


class AdaptiveAvgPool1d(_AdaptiveAvgPoolNd):

    def __init__(self, output_size):
        """Initialize AdaptiveMaxPool1d."""
        super(AdaptiveAvgPool1d, self).__init__(output_size)
        self.expand = P.ExpandDims()
        self.squeeze = P.Squeeze(2)
        self.output_size = output_size
        self.shape = F.shape

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        _, _, width = self.shape(input)
        stride = width // self.output_size
        kernel_size = width - (self.output_size - 1) * stride
        stride = (1, width // self.output_size)
        kernel_size = (1, kernel_size)

        max_pool = _get_cache_prim(P.AvgPool)(kernel_size=kernel_size, strides=stride,
                                              pad_mode="valid", data_format="NCHW")
        input = self.expand(input, 2)
        x = max_pool(input)
        x = self.squeeze(x)
        return cast_to_adapter_tensor(x)


class AdaptiveAvgPool2d(_AdaptiveAvgPoolNd):
    def __init__(self, output_size):
        super(AdaptiveAvgPool2d, self).__init__(output_size)
        self.output_size = output_size
        self.shape = P.Shape()
        if not isinstance(self.output_size, Iterable):
            self.output_size = [self.output_size, ] * 2
        self.condition = [0,] * 2
        if None in self.output_size:
            self.output_size = list(self.output_size)
            if self.output_size[0] is None:
                self.condition [0] = 1
                self.output_size[0] = 0
            if self.output_size[1] is None:
                self.condition [1] = 1
                self.output_size[1] = 0

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        _, _, h, w = self.shape(input)
        out_h = self.output_size[0] + self.condition[0] * h
        out_w = self.output_size[1] + self.condition[1] * w
        stride_h = h // out_h
        kernel_h = h - (out_h - 1) * stride_h
        stride_w = w // out_w
        kernel_w = w - (out_w - 1) * stride_w
        avg_pool = _get_cache_prim(P.AvgPool)(
            kernel_size=(kernel_h, kernel_w), strides=(stride_h, stride_w), pad_mode="valid", data_format="NCHW"
        )
        outputs = avg_pool(input)
        return cast_to_adapter_tensor(outputs)


class AdaptiveAvgPool3d(_AdaptiveAvgPoolNd):
    def __init__(self, output_size):
        super(AdaptiveAvgPool3d, self).__init__(output_size)
        self.output_size = output_size
        self.shape = P.Shape()
        if not isinstance(self.output_size, Iterable):
            self.output_size = [self.output_size, ] * 3
        self.condition = [0,] * 3
        if None in self.output_size:
            self.output_size = list(self.output_size)
            if self.output_size[0] is None:
                self.condition [0] = 1
                self.output_size[0] = 0
            if self.output_size[1] is None:
                self.condition [1] = 1
                self.output_size[1] = 0
            if self.output_size[2] is None:
                self.condition[2] = 1
                self.output_size[2] = 0

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        _, _, d, h, w = self.shape(input)
        out_d = self.output_size[0] + self.condition[0] * d
        out_h = self.output_size[1] + self.condition[1] * h
        out_w = self.output_size[2] + self.condition[2] * w
        stride_d = d // out_d
        kernel_d = d - (out_d - 1) * stride_d
        stride_h = h // out_h
        kernel_h = h - (out_h - 1) * stride_h
        stride_w = w // out_w
        kernel_w = w - (out_w - 1) * stride_w
        avg_pool = _get_cache_prim(P.AvgPool3D)(kernel_size=(kernel_d, kernel_h, kernel_w),
                                                strides=(stride_d, stride_h, stride_w),
                                                pad_mode="valid", data_format="NCDHW")
        outputs = avg_pool(input)
        return cast_to_adapter_tensor(outputs)


class _AdaptiveMaxPoolNd(Module):
    def __init__(self, output_size, return_indices = False):
        super(_AdaptiveMaxPoolNd, self).__init__()
        self.output_size = output_size
        self.return_indices = return_indices

    def extra_repr(self) -> str:
        return 'output_size={}'.format(self.output_size)


class AdaptiveMaxPool1d(_AdaptiveMaxPoolNd):
    def __init__(self, output_size, return_indices=False):
        """Initialize AdaptiveMaxPool1d."""
        super(AdaptiveMaxPool1d, self).__init__(output_size, return_indices)
        self.output_size = output_size
        self.return_indices = return_indices

    def forward(self, input):
        return Adapter_F.adaptive_max_pool1d(input, self.output_size, self.return_indices)


class AdaptiveMaxPool2d(_AdaptiveMaxPoolNd):
    def forward(self, input):
        input = cast_to_ms_tensor(input)
        if is_under_ascend_context() and len(input.shape) == 3:
            input = ms.ops.expand_dims(input, 0)
            output = ms.ops.adaptive_max_pool2d(input, self.output_size, self.return_indices)
            if self.return_indices:
                output[0] = ms.ops.squeeze(output[0], 0)
                output[1] = ms.ops.squeeze(output[1], 1)
            else:
                output = ms.ops.squeeze(output, 0)
        else:
            output = ms.ops.adaptive_max_pool2d(input, self.output_size, self.return_indices)
        return cast_to_adapter_tensor(output)


class AdaptiveMaxPool3d(_AdaptiveMaxPoolNd):
    def __init__(self, output_size, return_indices=False):
        # TODO: not support `return_indices` yet
        if return_indices and is_under_ascend_context():
            raise NotImplementedError('AdaptiveMaxPool3d doesn\'t  support return_indices on Ascend now.')
        super(AdaptiveMaxPool3d, self).__init__(output_size, return_indices)
        self.return_indices = return_indices

    def forward(self, input):
        outputs = Adapter_F.adaptive_max_pool3d(input, self.output_size, self.return_indices)
        return outputs


class _LPPoolNd(Module):
    def __init__(self, norm_type, kernel_size, stride = None,
                 ceil_mode = False):
        super(_LPPoolNd, self).__init__()
        self.norm_type = norm_type
        self.kernel_size = kernel_size
        self.stride = stride
        self.ceil_mode = ceil_mode

    def extra_repr(self):
        return 'norm_type={norm_type}, kernel_size={kernel_size}, stride={stride}, ' \
            'ceil_mode={ceil_mode}'.format(**self.__dict__)


class LPPool1d(_LPPoolNd):
    def forward(self, input):
        return Adapter_F.lp_pool1d(input, float(self.norm_type), self.kernel_size,
                                   self.stride, self.ceil_mode)


class LPPool2d(_LPPoolNd):
    def forward(self, input):
        return Adapter_F.lp_pool2d(input, float(self.norm_type), self.kernel_size,
                                   self.stride, self.ceil_mode)

class FractionalMaxPool2d(Module):
    def __init__(self, kernel_size, output_size=None, output_ratio=None, return_indices=False,
                 _random_samples=None):
        super(FractionalMaxPool2d, self).__init__()
        self.kernel_size = kernel_size
        self.return_indices = return_indices
        self.output_size = output_size
        self.output_ratio = output_ratio
        self._random_samples = _random_samples
        if output_size is None and output_ratio is None:
            raise ValueError("FractionalMaxPool2d requires specifying either "
                             "an output size, or a pooling ratio")
        if output_size is not None and output_ratio is not None:
            raise ValueError("only one of output_size and output_ratio may be specified")
        if self.output_ratio is not None:
            if not (0 < self.output_ratio[0] < 1 and 0 < self.output_ratio[1] < 1):
                raise ValueError("output_ratio must be between 0 and 1 (got {})"
                                 .format(output_ratio))

    def forward(self, input):
        return Adapter_F.fractional_max_pool2d(input, self.kernel_size, self.output_size, self.output_ratio,
                                               self.return_indices, self._random_samples)

class FractionalMaxPool3d(Module):
    def __init__(self, kernel_size, output_size=None, output_ratio=None, return_indices=False,
                 _random_samples=None):
        super(FractionalMaxPool3d, self).__init__()
        self.kernel_size = kernel_size
        self.return_indices = return_indices
        self.output_size = output_size
        self.output_ratio = output_ratio
        self._random_samples = _random_samples
        if output_size is None and output_ratio is None:
            raise ValueError("FractionalMaxPool3d requires specifying either "
                             "an output size, or a pooling ratio")
        if output_size is not None and output_ratio is not None:
            raise ValueError("only one of output_size and output_ratio may be specified")
        if self.output_ratio is not None:
            if not (0 < self.output_ratio[0] < 1 and 0 < self.output_ratio[1] < 1):
                raise ValueError("output_ratio must be between 0 and 1 (got {})"
                                 .format(output_ratio))

    def forward(self, input):
        return Adapter_F.fractional_max_pool3d(input, self.kernel_size, self.output_size, self.output_ratio,
                                                   self.return_indices, self._random_samples)
