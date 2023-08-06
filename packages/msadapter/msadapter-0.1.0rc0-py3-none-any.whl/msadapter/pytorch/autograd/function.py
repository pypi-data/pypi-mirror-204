#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings
from msadapter.utils import unsupported_attr
from msadapter.pytorch.nn import Module


class Function(Module):
    """Base class to create custom `autograd.Function`

    Examples::

        >>> class Exp(Function):
        >>>     def __init__(self):
        >>>         super(Exp, self).__init__()
        >>>
        >>>     def forward(self, i):
        >>>         result = i.exp()
        >>>         return result
        >>>
        >>>     def bprop(self, i, out, grad_output):
        >>>         return grad_output * out
        >>>
        >>> # Use non-static forward method:
        >>> output = Exp()(input)
    """
    def __init__(self, *args, **kwargs):
        unsupported_attr(args)
        unsupported_attr(kwargs)
        super(Function, self).__init__()
        warnings.warn("'autograd.Function' is the same as 'nn.Module', and do not support other Function methods")


    def apply(self, *args, **kwargs):
        """
        # Don not use it by calling the apply method.
        """
        unsupported_attr(args)
        unsupported_attr(kwargs)
        raise RuntimeError("To create a custom autograd.Function, use 'def forward(self, ...)' and "
            "'def bprop(self, ..., out, dout)' instead of 'forward()' and 'backward()' static methods. "
            "Then, use it as normal module class, do not call the class method 'apply'."
            " Please refer to the following example: "
            " https://openi.pcl.ac.cn/OpenI/MSAdapter/src/branch/master/"
                           "testing/ut/pytorch/autograd/test_autograd_function.py")
    