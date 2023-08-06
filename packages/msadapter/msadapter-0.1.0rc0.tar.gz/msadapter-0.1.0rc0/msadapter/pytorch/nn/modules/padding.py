#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mindspore import nn
from msadapter.pytorch.tensor import cast_to_ms_tensor, cast_to_adapter_tensor
from .module import Module

__all__ = ['ConstantPad1d', 'ConstantPad2d', 'ConstantPad3d', 'ReflectionPad1d', 'ReflectionPad2d', 'ReflectionPad3d',
           'ZeroPad2d', 'ReplicationPad1d', 'ReplicationPad2d', 'ReplicationPad3d']


class _ConstantPadNd(Module):
    def __init__(self, padding, value):
        super(_ConstantPadNd, self).__init__()
        self.padding = padding
        self.value = value
        self.pad_fun = None

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        output = self.pad_fun(input)
        return cast_to_adapter_tensor(output)

    def extra_repr(self) -> str:
        return 'padding={}, value={}'.format(self.padding, self.value)


class ConstantPad1d(_ConstantPadNd):
    r"""Pads the input tensor boundaries with a constant value.

    For `N`-dimensional padding, use :func:`torch.nn.functional.pad()`.

    Args:
        padding (int, tuple): the size of the padding. If is `int`, uses the same
            padding in both boundaries. If a 2-`tuple`, uses
            (:math:`\text{padding\_left}`, :math:`\text{padding\_right}`)

    Shape:
        - Input: :math:`(C, W_{in})` or :math:`(N, C, W_{in})`.
        - Output: :math:`(C, W_{out})` or :math:`(N, C, W_{out})`, where

          :math:`W_{out} = W_{in} + \text{padding\_left} + \text{padding\_right}`

    Examples::
        >>> m = nn.ConstantPad1d(2, 3.5)
        >>> input = msadapter.pytorch.ones(1, 2, 4)
        >>> m(input)
    """

    def __init__(self, padding, value: float):
        super(ConstantPad1d, self).__init__(padding, value)
        self.pad_fun = nn.ConstantPad1d(self.padding, self.value)


class ConstantPad2d(_ConstantPadNd):
    r"""Pads the input tensor boundaries with a constant value.

    For `N`-dimensional padding, use :func:`torch.nn.functional.pad()`.

    Args:
        padding (int, tuple): the size of the padding. If is `int`, uses the same
            padding in all boundaries. If a 4-`tuple`, uses (:math:`\text{padding\_left}`,
            :math:`\text{padding\_right}`, :math:`\text{padding\_top}`, :math:`\text{padding\_bottom}`)

    Shape:
        - Input: :math:`(N, C, H_{in}, W_{in})` or :math:`(C, H_{in}, W_{in})`.
        - Output: :math:`(N, C, H_{out}, W_{out})` or :math:`(C, H_{out}, W_{out})`, where

          :math:`H_{out} = H_{in} + \text{padding\_top} + \text{padding\_bottom}`

          :math:`W_{out} = W_{in} + \text{padding\_left} + \text{padding\_right}`

    Examples::

        >>> m = nn.ConstantPad2d(2, 3.5)
        >>> input = msadapter.pytorch.ones(1, 2, 2)
        >>> m(input)

    """
    def __init__(self, padding, value):
        super(ConstantPad2d, self).__init__(padding, value)
        self.pad_fun = nn.ConstantPad2d(self.padding, self.value)


class ConstantPad3d(_ConstantPadNd):
    r"""Pads the input tensor boundaries with a constant value.

    For `N`-dimensional padding, use :func:`torch.nn.functional.pad()`.

    Args:
        padding (int, tuple): the size of the padding. If is `int`, uses the same
            padding in all boundaries. If a 6-`tuple`, uses
            (:math:`\text{padding\_left}`, :math:`\text{padding\_right}`,
            :math:`\text{padding\_top}`, :math:`\text{padding\_bottom}`,
            :math:`\text{padding\_front}`, :math:`\text{padding\_back}`)

    Shape:
        - Input: :math:`(N, C, D_{in}, H_{in}, W_{in})` or :math:`(C, D_{in}, H_{in}, W_{in})`.
        - Output: :math:`(N, C, D_{out}, H_{out}, W_{out})` or
          :math:`(C, D_{out}, H_{out}, W_{out})`, where

          :math:`D_{out} = D_{in} + \text{padding\_front} + \text{padding\_back}`

          :math:`H_{out} = H_{in} + \text{padding\_top} + \text{padding\_bottom}`

          :math:`W_{out} = W_{in} + \text{padding\_left} + \text{padding\_right}`

    Examples::

        >>> m = nn.ConstantPad3d(3, 3.5)
        >>> input = msadapter.pytorch.ones(16, 3, 10, 20, 30)
        >>> output = m(input)

    """
    def __init__(self, padding, value):
        super(ConstantPad3d, self).__init__(padding, value)
        self.pad_fun = nn.ConstantPad3d(self.padding, self.value)


class _ReflectionPadNd(Module):
    def __init__(self, padding):
        super(_ReflectionPadNd, self).__init__()
        self.padding = padding
        self.pad_fun = None

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        output = self.pad_fun(input)
        return cast_to_adapter_tensor(output)

    def extra_repr(self) -> str:
        return '{}'.format(self.padding)


class ReflectionPad1d(_ReflectionPadNd):
    r"""Pads the input tensor using the reflection of the input boundary.

    For `N`-dimensional padding, use :func:`torch.nn.functional.pad()`.

    Args:
        padding (int, tuple): the size of the padding. If is `int`, uses the same
            padding in all boundaries. If a 2-`tuple`, uses
            (:math:`\text{padding\_left}`, :math:`\text{padding\_right}`)

    Shape:
        - Input: :math:`(C, W_{in})` or :math:`(N, C, W_{in})`.
        - Output: :math:`(C, W_{out})` or :math:`(N, C, W_{out})`, where

          :math:`W_{out} = W_{in} + \text{padding\_left} + \text{padding\_right}`

    Examples::

        >>> m = nn.ReflectionPad1d(2)
        >>> input = msadapter.pytorch.ones(1, 2, 4)
        >>> m(input)

    """

    def __init__(self, padding):
        super(ReflectionPad1d, self).__init__(padding)
        self.pad_fun = nn.ReflectionPad1d(self.padding)


class ReflectionPad2d(_ReflectionPadNd):
    r"""Pads the input tensor using the reflection of the input boundary.

    For `N`-dimensional padding, use :func:`torch.nn.functional.pad()`.

    Args:
        padding (int, tuple): the size of the padding. If is `int`, uses the same
            padding in all boundaries. If a 4-`tuple`, uses (:math:`\text{padding\_left}`,
            :math:`\text{padding\_right}`, :math:`\text{padding\_top}`, :math:`\text{padding\_bottom}`)

    Shape:
        - Input: :math:`(N, C, H_{in}, W_{in})` or :math:`(C, H_{in}, W_{in})`.
        - Output: :math:`(N, C, H_{out}, W_{out})` or :math:`(C, H_{out}, W_{out})` where

          :math:`H_{out} = H_{in} + \text{padding\_top} + \text{padding\_bottom}`

          :math:`W_{out} = W_{in} + \text{padding\_left} + \text{padding\_right}`

    Examples::

        >>> m = nn.ReflectionPad2d(2)
        >>> input = msadapter.pytorch.ones(1, 1, 3, 3)
        >>> m(input)

    """

    def __init__(self, padding):
        super(ReflectionPad2d, self).__init__(padding)
        self.pad_fun = nn.ReflectionPad2d(self.padding)

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        output = self.pad_fun(input)
        return cast_to_adapter_tensor(output)

class ReflectionPad3d(_ReflectionPadNd):
    r"""Pads the input tensor using the reflection of the input boundary.

    For `N`-dimensional padding, use :func:`torch.nn.functional.pad()`.

    Args:
        padding (int, tuple): the size of the padding. If is `int`, uses the same
            padding in all boundaries. If a 6-`tuple`, uses
            (:math:`\text{padding\_left}`, :math:`\text{padding\_right}`,
            :math:`\text{padding\_top}`, :math:`\text{padding\_bottom}`,
            :math:`\text{padding\_front}`, :math:`\text{padding\_back}`)

    Shape:
        - Input: :math:`(N, C, D_{in}, H_{in}, W_{in})` or :math:`(C, D_{in}, H_{in}, W_{in})`.
        - Output: :math:`(N, C, D_{out}, H_{out}, W_{out})` or :math:`(C, D_{out}, H_{out}, W_{out})`,
          where

          :math:`D_{out} = D_{in} + \text{padding\_front} + \text{padding\_back}`

          :math:`H_{out} = H_{in} + \text{padding\_top} + \text{padding\_bottom}`

          :math:`W_{out} = W_{in} + \text{padding\_left} + \text{padding\_right}`

    Examples::

        >>> m = nn.ReflectionPad3d(1)
        >>> input = msadapter.pytorch.ones(1, 1, 2, 2, 2)
        >>> m(input)

    """

    def __init__(self, padding):
        super(ReflectionPad3d, self).__init__(padding)
        self.pad_fun = nn.ReflectionPad3d(self.padding)

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        if input.ndim == 5:
            input_shape = input.shape
            input = input.reshape((-1,) + input_shape[2:])
            output = self.pad_fun(input)
            output = output.reshape(input_shape[0:2] + output.shape[1:])
        else:
            output = self.pad_fun(input)
        return cast_to_adapter_tensor(output)


class ZeroPad2d(ConstantPad2d):
    r"""Pads the input tensor boundaries with zero.

    For `N`-dimensional padding, use :func:`torch.nn.functional.pad()`.

    Args:
        padding (int, tuple): the size of the padding. If is `int`, uses the same
            padding in all boundaries. If a 4-`tuple`, uses (:math:`\text{padding\_left}`,
            :math:`\text{padding\_right}`, :math:`\text{padding\_top}`, :math:`\text{padding\_bottom}`)

    Shape:
        - Input: :math:`(N, C, H_{in}, W_{in})` or :math:`(C, H_{in}, W_{in})`.
        - Output: :math:`(N, C, H_{out}, W_{out})` or :math:`(C, H_{out}, W_{out})`, where

          :math:`H_{out} = H_{in} + \text{padding\_top} + \text{padding\_bottom}`

          :math:`W_{out} = W_{in} + \text{padding\_left} + \text{padding\_right}`

    Examples::

        >>> m = nn.ZeroPad2d(2)
        >>> input = msadapter.pytorch.ones(1, 1, 3, 3)
        >>> m(input)

    """

    def __init__(self, padding) -> None:
        super(ZeroPad2d, self).__init__(padding, 0.)

class _ReplicationPadNd(Module):
    def __init__(self, padding):
        super(_ReplicationPadNd, self).__init__()
        self.padding = padding
        self.pad_fun = None

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        output = self.pad_fun(input)
        return cast_to_adapter_tensor(output)

    def extra_repr(self) -> str:
        return '{}'.format(self.padding)

class ReplicationPad1d(_ReplicationPadNd):
    def __init__(self, padding):
        super(ReplicationPad1d, self).__init__(padding)
        self.pad_fun = nn.ReplicationPad1d(padding)

class ReplicationPad2d(_ReplicationPadNd):
    def __init__(self, padding):
        super(ReplicationPad2d, self).__init__(padding)
        self.pad_fun = nn.ReplicationPad2d(padding)

class ReplicationPad3d(_ReplicationPadNd):
    def __init__(self, padding):
        super(ReplicationPad3d, self).__init__(padding)
        self.pad_fun = nn.ReplicationPad3d(padding)
