#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
# from functools import lru_cache

from mindspore.ops import operations as P
from mindspore.ops.primitive import _primexpr

from msadapter.pytorch.nn.parameter import Parameter
from msadapter.pytorch.nn import init
from msadapter.pytorch.functional import empty
from msadapter.utils import unsupported_attr
from msadapter.pytorch.tensor import cast_to_ms_tensor, cast_to_adapter_tensor
from msadapter.pytorch.nn.functional import conv2d, conv_transpose3d, conv1d
# from .utils import _triple, _pair, _single, _reverse_repeat_tuple, _GLOBAL_LRU_CACHE_SIZE_NN
from .utils import _triple, _pair, _single, _reverse_repeat_tuple
from .module import Module

__all__ = ['Conv1d', 'Conv2d', 'Conv3d',
           'ConvTranspose1d', 'ConvTranspose2d', 'ConvTranspose3d',
           'LazyConv1d', 'LazyConv2d', 'LazyConv3d',
           'LazyConvTranspose1d', 'LazyConvTranspose2d', 'LazyConvTranspose3d']


class _ConvNd(Module):
    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 stride,
                 padding,
                 dilation,
                 output_padding,
                 groups,
                 bias,
                 padding_mode,
                 device=None,
                 dtype=None,
                 transposed=False
                 ):
        """Initialize _Conv."""
        unsupported_attr(device)
        unsupported_attr(dtype)

        super(_ConvNd, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.transposed = transposed
        self.output_padding = output_padding
        self.groups = groups
        self.padding_mode = padding_mode
        # MS add
        self.pad_mode = 'same'
        self.data_format = 'NCHW'
        self.has_bias = bias
        if in_channels % groups != 0:
            raise ValueError('in_channels must be divisible by groups')
        if out_channels % groups != 0:
            raise ValueError('out_channels must be divisible by groups')
        valid_padding_strings = {'same', 'valid'}
        if isinstance(padding, str):
            if padding not in valid_padding_strings:
                raise ValueError(
                    "Invalid padding string {!r}, should be one of {}".format(
                        padding, valid_padding_strings))

            if padding == 'same' and any(s != 1 for s in stride):
                raise ValueError("padding='same' is not supported for strided convolutions")

        if isinstance(self.padding, str):
            self._reversed_padding_repeated_twice = [0, 0] * len(kernel_size)
            if padding == 'same':
                for d, k, i in zip(dilation, kernel_size,
                                   range(len(kernel_size) - 1, -1, -1)):
                    total_padding = d * (k - 1)
                    left_pad = total_padding // 2
                    self._reversed_padding_repeated_twice[2 * i] = left_pad
                    self._reversed_padding_repeated_twice[2 * i + 1] = (
                        total_padding - left_pad)
        else:
            self._reversed_padding_repeated_twice = _reverse_repeat_tuple(self.padding, 2)

        if transposed:
            self.weight = Parameter(empty((in_channels, out_channels // groups, *kernel_size)))
        else:
            self.weight = Parameter(empty((out_channels, in_channels // groups, *kernel_size)))
        if bias:
            self.bias = Parameter(empty(out_channels))
        else:
            self.bias = None
        self.reset_parameters()

    def reset_parameters(self):
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight)
            if fan_in != 0:
                bound = 1 / math.sqrt(fan_in)
                init.uniform_(self.bias, -bound, bound)

    def extra_repr(self):
        s = 'input_channels={}, output_channels={}, kernel_size={}, ' \
            'stride={}, pad_mode={}, padding={}, dilation={}, ' \
            'group={}, has_bias={}'.format(self.in_channels,
                                           self.out_channels,
                                           self.kernel_size,
                                           self.stride,
                                           self.pad_mode,
                                           self.padding,
                                           self.dilation,
                                           self.groups,
                                           self.has_bias)
        return s


class Conv1d(_ConvNd):
    r"""
        1D convolution layer.

        Calculates the 1D convolution on the input tensor which is typically of shape :math:`(N, C_{in}, L_{in})`,
        where :math:`N` is batch size, :math:`C_{in}` is a number of channels and :math:`L_{in}` is a length of
        sequence. For the tensor of each batch, its shape is :math:`(C_{in}, L_{in})`, the formula is defined as:

        Supported Platforms:
            ``Ascend`` ``GPU`` ``CPU``

        Examples:
            >>> net = nn.Conv1d(120, 240, 4, has_bias=False, weight_init='normal')
            >>> x = Tensor(np.ones([1, 120, 640]), mindspore.float32)
            >>> output = net(x).shape
            >>> print(output)
            (1, 240, 640)
        """

    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride=1,
        padding=0,
        dilation=1,
        groups=1,
        bias=True,
        padding_mode='zeros',
        device=None,
        dtype=None
    ):
        factory_kwargs = {'device': device, 'dtype': dtype, 'transposed': False}
        kernel_size_ = _single(kernel_size)
        stride_ = _single(stride)
        padding_ = padding if isinstance(padding, str) else _single(padding)
        dilation_ = _single(dilation)
        super(Conv1d, self).__init__(in_channels, out_channels, kernel_size_, stride_, padding_, dilation_,
            _pair(0), groups, bias, padding_mode, **factory_kwargs)

        #TODO pad_mode in ['zeros', 'reflect', 'replicate', 'circular']
        if padding_mode in {'reflect', 'replicate', 'circular'}:
            raise ValueError("Pad mode '{}' is not currently supported.".format(padding_mode))

    def forward(self, input):
        return conv1d(input, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups)


class Conv2d(_ConvNd):
    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 stride=1,
                 padding=0,
                 dilation=1,
                 groups=1,
                 bias=True,
                 padding_mode='zeros',
                 device=None,
                 dtype=None):
        """Initialize Conv2d."""
        factory_kwargs = {'device': device, 'dtype': dtype, 'transposed': False}
        kernel_size_ = _pair(kernel_size)
        stride_ = _pair(stride)
        padding_ = padding if isinstance(padding, str) else _pair(padding)
        dilation_ = _pair(dilation)
        super(Conv2d, self).__init__(in_channels, out_channels, kernel_size_, stride_, padding_, dilation_,
            _pair(0), groups, bias, padding_mode, **factory_kwargs)

        #TODO pad_mode in ['zeros', 'reflect', 'replicate', 'circular']
        if padding_mode in {'reflect', 'replicate', 'circular'}:
            raise ValueError("Pad mode '{}' is not currently supported.".format(padding_mode))

    def forward(self, x):
        x = cast_to_ms_tensor(x)
        ndim = x.ndim
        if ndim == 3:
            x = x.expand_dims(0)
            # Under pynative-mode, self.stride, etc can be changed at any time.
            # However, under graph-mode, the graph will be generated at first time running and can not
            # be altered anymore. After that, self.stride, etc are not supported to be changed dynamically.
            output = conv2d(x, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups)
            output = output.squeeze(0)
        else:
            output = conv2d(x, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups)
        return cast_to_adapter_tensor(output)


class Conv3d(_ConvNd):
    r"""
    3D convolution layer.

    Calculates the 3D convolution on the input tensor which is typically of shape

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.ones([16, 3, 10, 32, 32]), mindspore.float32)
        >>> conv3d = nn.Conv3d(in_channels=3, out_channels=32, kernel_size=(4, 3, 3))
        >>> output = conv3d(x)
        >>> print(output.shape)
        (16, 32, 10, 32, 32)
    """
    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride=1,
        padding=0,
        dilation=1,
        groups=1,
        bias=True,
        padding_mode='zeros',
        device=None,
        dtype=None
    ):
        factory_kwargs = {'device': device, 'dtype': dtype, 'transposed': False}

        kernel_size_ = _triple(kernel_size)
        stride_ = _triple(stride)
        padding_ = padding if isinstance(padding, str) else _triple(padding)
        dilation_ = _triple(dilation)

        super(Conv3d, self).__init__(in_channels, out_channels, kernel_size_, stride_, padding_, dilation_,
            _pair(0), groups, bias, padding_mode, **factory_kwargs)

        #TODO pad_mode in ['zeros', 'reflect', 'replicate', 'circular']
        if padding_mode in {'reflect', 'replicate', 'circular'}:
            raise ValueError("Pad mode '{}' is not currently supported.".format(padding_mode))

        if padding == 0:
            self.pad_mode = 'valid'
            self.padding =(self.padding[0], self.padding[0], self.padding[1],
                           self.padding[1], self.padding[2], self.padding[2])
        elif isinstance(self.padding, str):
            self.pad_mode = self.padding
            self.padding = 0
        elif padding_mode == 'zeros':
            self.pad_mode = "pad"
            self.padding =(self.padding[0], self.padding[0], self.padding[1],
                           self.padding[1], self.padding[2], self.padding[2])

        self.conv3d = P.Conv3D(out_channel=self.out_channels,
                               kernel_size=self.kernel_size,
                               mode=1,
                               pad_mode=self.pad_mode,
                               pad=self.padding,
                               stride=self.stride,
                               dilation=self.dilation,
                               group=groups,
                               data_format='NCDHW')
        self.bias_add = P.BiasAdd(data_format='NCDHW')
        self.shape = P.Shape()

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        ndim = input.ndim
        if ndim == 4:
            input = input.expand_dims(0)
            output = self.conv3d(input, self.weight)
            if self.has_bias:
                output = self.bias_add(output, self.bias)
            output = output.squeeze(0)
        else:
            output = self.conv3d(input, self.weight)
            if self.has_bias:
                output = self.bias_add(output, self.bias)
        return cast_to_adapter_tensor(output)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE_NN)
def _output_padding(output_padding, input_ndim, input_shape, output_size,
                    stride, padding, kernel_size,
                    num_spatial_dims, dilation=None):
    if output_size is None:
        ret = _single(output_padding)
    else:
        has_batch_dim = input_ndim == num_spatial_dims + 2
        num_non_spatial_dims = 2 if has_batch_dim else 1
        if len(output_size) == num_non_spatial_dims + num_spatial_dims:
            output_size = output_size[num_non_spatial_dims:]
        if len(output_size) != num_spatial_dims:
            raise ValueError(
                f"ConvTranspose{num_spatial_dims}D: for {input.dim()}D input, "
                f"output_size must have {num_spatial_dims} "
                f"or {num_non_spatial_dims + num_spatial_dims} elements (got {len(output_size)})")

        min_sizes = []
        max_sizes = []
        for d in range(num_spatial_dims):
            dim_size = ((input_shape[d + num_non_spatial_dims] - 1) * stride[d] -
                        2 * padding[d] +
                        (dilation[d] if dilation is not None else 1) * (kernel_size[d] - 1) + 1)
            min_sizes.append(dim_size)
            max_sizes.append(min_sizes[d] + stride[d] - 1)

        for i in range(len(output_size)):
            size = output_size[i]
            min_size = min_sizes[i]
            max_size = max_sizes[i]
            if size < min_size or size > max_size:
                raise ValueError((
                    "requested an output size of {}, but valid sizes range "
                    "from {} to {} (for an input of {})").format(
                        output_size, min_sizes, max_sizes, input_shape[2:]))

        res = []
        for d in range(num_spatial_dims):
            res.append(output_size[d] - min_sizes[d])

        ret = tuple(res)
    return ret


class ConvTranspose1d(_ConvNd):
    r"""
    1D transposed convolution layer.

    Calculates a 1D transposed convolution, which can be regarded as Conv1d for the gradient of the input.
    It also called deconvolution (although it is not an actual deconvolution).
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> net = nn.ConvTranspose1d(3, 64, 4, has_bias=False)
        >>> x = Tensor(np.ones([1, 3, 50]), mindspore.float32)
        >>> output = net(x).shape
        >>> print(output)
        (1, 64, 53)
    """
    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride=1,
        padding=0,
        output_padding=0,
        groups=1,
        bias=True,
        dilation=1,
        padding_mode='zeros',
        device=None,
        dtype=None,
    ):
        factory_kwargs = {'device': device, 'dtype': dtype, 'transposed': True}

        _padding = _single(padding)
        _kernel_size = (1, kernel_size) if isinstance(kernel_size, int) else (1, kernel_size[0])
        _stride = (1, stride) if isinstance(stride, int) else (1, stride[0])
        _dilation = (1, dilation) if isinstance(dilation, int) else (1, dilation[0])

        super(ConvTranspose1d, self).__init__(in_channels, out_channels, _kernel_size, _stride,
                                              _padding, _dilation, output_padding, groups, bias,
                                              padding_mode, **factory_kwargs)

        self.shape = P.Shape()
        if padding_mode in {'reflect', 'replicate', 'circular'}:
            raise ValueError("Pad mode '{}' is not currently supported.".format(padding_mode))
        if output_padding > 0:
            raise ValueError("output_padding '{}' is not currently supported.".format(output_padding))

        if (isinstance(padding, int) and padding == 0) or (isinstance(padding, tuple) and padding[0] == 0):
            self.pad_mode = 'valid'
            self.padding = (0, 0, 0, 0)
        elif padding_mode == 'zeros':
            self.pad_mode = "pad"
            if isinstance(padding, int):
                self.padding = (0, 0, padding, padding)
            else:
                self.padding = (0, 0, padding[0], padding[0])

        self.is_valid = self.pad_mode == 'valid'
        self.is_same = self.pad_mode == 'same'
        self.is_pad = self.pad_mode == 'pad'

        # cause Conv2DBackpropInput's out_channel refers to Conv2D's out_channel.
        self.conv2d_transpose = P.Conv2DBackpropInput(out_channel=self.in_channels,
                                                      kernel_size=self.kernel_size,
                                                      mode=1,
                                                      pad_mode=self.pad_mode,
                                                      pad=self.padding,
                                                      stride=self.stride,
                                                      dilation=self.dilation,
                                                      group=groups)
        self.bias_add = P.BiasAdd()
        self.expand_dims = P.ExpandDims()
        self.squeeze = P.Squeeze(2)

    def forward(self, input, output_size=None):
        if output_size is not None:
            raise ValueError("output_size '{}' is not currently supported.".format(output_size))

        x = cast_to_ms_tensor(input)
        ndim = x.ndim
        if ndim == 2:
            x = x.expand_dims(0)
            x = self.expand_dims(x, 2)

            n, _, h, w = self.shape(x)

            h_out = _deconv_output_length(self.is_valid, self.is_same, self.is_pad, h, self.kernel_size[0],
                                          self.stride[0], self.dilation[0], self.padding[0] + self.padding[1])
            w_out = _deconv_output_length(self.is_valid, self.is_same, self.is_pad, w, self.kernel_size[1],
                                          self.stride[1], self.dilation[1], self.padding[2] + self.padding[3])
            output = self.conv2d_transpose(x, self.weight, (n, self.out_channels, h_out, w_out))

            if self.has_bias:
                output = self.bias_add(output, self.bias)

            output = self.squeeze(output)
            output = output.squeeze(0)
        else:
            x = self.expand_dims(x, 2)

            n, _, h, w = self.shape(x)

            h_out = _deconv_output_length(self.is_valid, self.is_same, self.is_pad, h, self.kernel_size[0],
                                          self.stride[0], self.dilation[0], self.padding[0] + self.padding[1])
            w_out = _deconv_output_length(self.is_valid, self.is_same, self.is_pad, w, self.kernel_size[1],
                                          self.stride[1], self.dilation[1], self.padding[2] + self.padding[3])
            output = self.conv2d_transpose(x, self.weight, (n, self.out_channels, h_out, w_out))

            if self.has_bias:
                output = self.bias_add(output, self.bias)

            output = self.squeeze(output)
        return cast_to_adapter_tensor(output)



class ConvTranspose2d(_ConvNd):
    r"""
    2D transposed convolution layer.

    Calculates a 2D transposed convolution, which can be regarded as Conv2d for the gradient of the input.
    It also called deconvolution (although it is not an actual deconvolution).

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> net = nn.ConvTranspose2d(3, 64, 4, has_bias=False)
        >>> x = Tensor(np.ones([1, 3, 16, 50]), mindspore.float32)
        >>> output = net(x).shape
        >>> print(output)
        (1, 64, 19, 53)
        """

    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride=1,
        padding=0,
        output_padding=0,
        groups=1,
        bias=True,
        dilation=1,
        padding_mode='zeros',
        device=None,
        dtype=None
    ):
        factory_kwargs = {'device': device, 'dtype': dtype, 'transposed': True}

        _kernel_size = _pair(kernel_size)
        _stride = _pair(stride)
        _padding = _pair(padding)
        _dilation = _pair(dilation)
        output_padding = _pair(output_padding)

        super(ConvTranspose2d, self).__init__(in_channels, out_channels, _kernel_size, _stride, _padding, _dilation,
                                              output_padding, groups, bias, padding_mode, **factory_kwargs)

        self.shape = P.Shape()

        if padding == 0:
            self.pad_mode = 'valid'
            self.padding =(self.padding[0], self.padding[0], self.padding[1], self.padding[1])
        elif isinstance(self.padding, str):
            self.pad_mode = self.padding
            self.padding = 0
        elif padding_mode == 'zeros':
            self.pad_mode = "pad"
            self.padding =(self.padding[0], self.padding[0], self.padding[1], self.padding[1])

        if self.padding_mode != 'zeros':
            raise ValueError('Only `zeros` padding mode is supported for ConvTranspose2d')

        self.is_valid = self.pad_mode == 'valid'
        self.is_same = self.pad_mode == 'same'
        self.is_pad = self.pad_mode == 'pad'

        # cause Conv2DTranspose's out_channel refers to Conv2D's out_channel.
        self.conv2d_transpose = P.Conv2DTranspose(out_channel=self.in_channels,
                                                  kernel_size=self.kernel_size,
                                                  mode=1,
                                                  pad_mode=self.pad_mode,
                                                  pad=self.padding,
                                                  stride=self.stride,
                                                  dilation=self.dilation,
                                                  group=groups)
        self.bias_add = P.BiasAdd()
        if isinstance(self.padding, int):
            self.padding_top, self.padding_bottom, self.padding_left, self.padding_right = (self.padding,) * 4
        else:
            self.padding_top, self.padding_bottom, self.padding_left, self.padding_right = self.padding

    def forward(self, input, output_size = None):
        if output_size is not None:
            raise ValueError("output_size '{}' is not currently supported.".format(output_size))
        x = cast_to_ms_tensor(input)
        ndim = x.ndim
        if ndim == 3:
            x = x.expand_dims(0)
            n, _, h, w = self.shape(x)
            h_out = _deconv_output_length(self.is_valid, self.is_same, self.is_pad, h, self.kernel_size[0],
                                          self.stride[0], self.dilation[0], self.padding_top + self.padding_bottom)
            w_out = _deconv_output_length(self.is_valid, self.is_same, self.is_pad, w, self.kernel_size[1],
                                          self.stride[1], self.dilation[1], self.padding_left + self.padding_right)
            output = self.conv2d_transpose(x, self.weight, (n, self.out_channels, h_out, w_out))
            if self.has_bias:
                output = self.bias_add(output, self.bias)
            output = output.squeeze(0)
        else:
            n, _, h, w = self.shape(x)
            h_out = _deconv_output_length(self.is_valid, self.is_same, self.is_pad, h, self.kernel_size[0],
                                          self.stride[0], self.dilation[0], self.padding_top + self.padding_bottom)
            w_out = _deconv_output_length(self.is_valid, self.is_same, self.is_pad, w, self.kernel_size[1],
                                          self.stride[1], self.dilation[1], self.padding_left + self.padding_right)
            output = self.conv2d_transpose(x, self.weight, (n, self.out_channels, h_out, w_out))
            if self.has_bias:
                output = self.bias_add(output, self.bias)
        return cast_to_adapter_tensor(output)



class ConvTranspose3d(_ConvNd):
    r"""
       3D transposed convolution layer.

       Calculates a 3D transposed convolution, which can be regarded as Conv3d for the gradient of the input.
       It also called deconvolution (although it is not an actual deconvolution).

       Examples:
           >>> x = Tensor(np.ones([32, 16, 10, 32, 32]), mindspore.float32)
           >>> conv3d_transpose = nn.ConvTranspose3d(in_channels=16, out_channels=3, kernel_size=(4, 6, 2),
           ...                                       pad_mode='pad')
           >>> output = conv3d_transpose(x)
           >>> print(output.shape)
           (32, 3, 13, 37, 33)
       """

    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride = 1,
        padding = 0,
        output_padding = 0,
        groups = 1,
        bias = True,
        dilation = 1,
        padding_mode = 'zeros',
        device=None,
        dtype=None
    ):
        factory_kwargs = {'device': device, 'dtype': dtype, 'transposed': True}

        _kernel_size = _triple(kernel_size)
        _stride = _triple(stride)
        _padding = _triple(padding)
        _dilation = _triple(dilation)
        output_padding = _triple(output_padding)

        super(ConvTranspose3d, self).__init__(in_channels, out_channels, _kernel_size, _stride, _padding, _dilation,
                                              output_padding, groups, bias, padding_mode, **factory_kwargs)

    def forward(self, input, output_size = None):
        if self.padding_mode != 'zeros':
            raise ValueError('Only `zeros` padding mode is supported for ConvTranspose3d')

        ndim = input.ndim
        input_shape = input.size()
        num_spatial_dims = 3

        if output_size is not None:
            output_size = tuple(output_size)

        _out_padding = _output_padding(self.output_padding, ndim, input_shape, output_size,
                                       self.stride, self.padding, self.kernel_size, num_spatial_dims,
                                       self.dilation)

        if ndim == 4:
            input = input.unsqueeze(0)
            output = conv_transpose3d(input, self.weight, self.bias, self.stride,
                                      self.padding, _out_padding, self.groups, self.dilation)
            output = output.squeeze(0)
        else:
            output = conv_transpose3d(input, self.weight, self.bias, self.stride,
                                      self.padding, _out_padding, self.groups, self.dilation)
        return cast_to_adapter_tensor(output)


def _deconv_output_length(is_valid, is_same, is_pad, input_length, filter_size, stride_size, dilation_size, padding):
    """Calculate the width and height of output."""
    length = 0
    filter_size = filter_size + (filter_size - 1) * (dilation_size - 1)
    if is_valid:
        if filter_size - stride_size > 0:
            length = input_length * stride_size + filter_size - stride_size
        else:
            length = input_length * stride_size
    elif is_same:
        length = input_length * stride_size
    elif is_pad:
        length = input_length * stride_size - padding + filter_size - stride_size

    return length


LazyConv1d = Conv1d
LazyConv2d = Conv2d
LazyConv3d = Conv3d

LazyConvTranspose1d = ConvTranspose1d
LazyConvTranspose2d = ConvTranspose2d
LazyConvTranspose3d = ConvTranspose3d
