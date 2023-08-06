#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parameter interface"""
import sys
import numbers
from copy import copy

import mindspore as ms
import mindspore.common.dtype as mstype
from mindspore.common.initializer import initializer
import mindspore._checkparam as Validator
from mindspore._c_expression import Tensor as Tensor_
from mindspore.parallel._tensor import _get_slice_index
from mindspore.parallel._auto_parallel_context import auto_parallel_context
from mindspore.parallel._ps_context import _is_role_worker, _is_role_sched, _clone_hash_table
from mindspore.parallel._ps_context import _insert_accumu_init_info
from mindspore.ops import functional as F
from msadapter.pytorch.tensor import Tensor, cast_to_adapter_tensor

__all__ = ['Parameter', 'ParameterTuple']

PARAMETER_NAME_DEFAULT = "Parameter"
PARAMETER_NAME_PREFIX_MAX_LEN = 1024

# Global variable for parameter unique key.
_GLOBAL_PARAMETER_KEY = -1


def _is_in_parallel_mode():
    """Get parallel mode."""
    return auto_parallel_context().get_parallel_mode() in ["semi_auto_parallel", "auto_parallel"]


def init_to_value(init):
    """
    Get value of initializer.

    Returns:
        Value of the initializer.

    Raises:
        ValueError: The value of the argument 'init' is not correct.
    """
    if isinstance(init, str):
        if init == 'zeros':
            return 0.0
        if init == 'ones':
            return 1.0
        raise ValueError("The argument 'init' should be one of values in ['zeros', 'ones'].")
    if isinstance(init, numbers.Number):
        return float(init)
    raise ValueError("The argument 'init' should be number or string, but got {}.".format(type(init)))

def _get_unique_parameter_key():
    """
    Get parameter unique key.
    Used to identify the same Parameter for Worker and Server in the embedding cache scenario.

    Returns:
        Integer. The unique parameter key.
    """
    global _GLOBAL_PARAMETER_KEY
    _GLOBAL_PARAMETER_KEY += 1
    return _GLOBAL_PARAMETER_KEY

class Parameter(ms.Parameter):
    # Parameter is an subclass of ms.Parameter and adapter.Tensor, only 'Parameter' in methods need be overload.
    _base_type = {}
    def __new__(cls, data, *args, **kwargs):
        init_data_flag = bool(isinstance(data, ms.Tensor) and data.has_init)
        rc = sys.getrefcount(data)
        _, *class_init_args = Parameter._get_parameter_new_args(data, rc)
        new_type = Parameter._get_base_class(Tensor)
        obj = Tensor.__new__(new_type)
        Tensor.__init__(obj, *class_init_args, inner=True)
        # it's better to make the Initializer a kind of tensor.
        obj.init_mode = None
        obj.is_default_input_init = init_data_flag
        if obj.has_init:
            obj.init_mode = data
        return obj

    def __reduce_ex__(self, _):
        data = self
        if self.init_mode is not None:
            data = self.init_mode
        else:
            # cast to break deep infinite loop while deepcopy
            data = Tensor(self)
        return (
            Parameter, (data, self.requires_grad, self.name, self.layerwise_parallel))

    def __init__(self, data, requires_grad=True, name=None, layerwise_parallel=False, parallel_optimizer=True):
        super().__init__(default_input=data, name=name, requires_grad=requires_grad,
                         layerwise_parallel=layerwise_parallel, parallel_optimizer=parallel_optimizer)

    def __deepcopy__(self, memodict):
        new_obj = Parameter(self)
        new_obj.name = self.name
        new_obj._inited_param = self._inited_param
        return new_obj

    def __str__(self):
        return f'Parameter containing: {Tensor_.__repr__(self.data)}, requires_grad={self.requires_grad})'

    def __parameter__(self):
        """For parse check."""

    @staticmethod
    def _get_base_class(input_class):
        input_class_name = Parameter.__name__
        if input_class_name in Parameter._base_type:
            new_type = Parameter._base_type.get(input_class_name)
        else:
            new_type = type(input_class_name, (Parameter, input_class), {})
            Parameter._base_type[input_class_name] = new_type
        return new_type

    def copy(self):
        """
        Copy the parameter.

        Returns:
            Parameter, a new parameter.
        """
        return self.clone(init='same')

    def clone(self, init='same'):
        """
        Clone the parameter.

        Args:
            init (Union[Tensor, str, numbers.Number]): Initialize the shape and dtype of the parameter.
                If `init` is a `Tensor` or `numbers.Number`, clone a new parameter with the same shape
                and dtype, and the data of the new parameter will be set according to `init`. If `init`
                is a `str`, the `init` should be the alias of the class inheriting from `Initializer`.
                For example, if `init` is 'same', clone a new parameter with the same data, shape, and
                dtype. Default: 'same'.

        Returns:
            Parameter, a new parameter.
        """
        x = copy(self)
        param_info_clone = self.param_info.clone()
        info = self.param_info
        if hasattr(info, "cloned_obj"):
            info.cloned_obj.append(x)
        else:
            info.cloned_obj = [x]
        self.param_info = info
        param_info_clone.obj = x
        x.param_info = param_info_clone
        x.is_init = False
        x.init = self.init
        x.is_param_ps = self.is_param_ps
        x.init_in_server = self.init_in_server
        x.cache_enable = self.cache_enable
        if x.cache_enable:
            x.key = _get_unique_parameter_key()
        x.requires_aggr = self.requires_aggr
        if self.cache_shape:
            x.cache_shape = self.cache_shape
        if init != 'same':
            shape = self.shape
            dtype = self.dtype
            init_data = initializer(init, shape=shape, dtype=dtype)
            x.set_data(cast_to_adapter_tensor(init_data))
        return x

    @property
    def data(self):
        """Return the parameter object."""
        return self

    @data.setter
    def data(self, data):
        self.set_data(data)

    def _update_tensor_data(self, data):
        """Update the parameter by a Tensor."""
        if isinstance(self, Tensor):
            self.init_flag = False
            self.init = None
            return self.assign_value(data)
        new_param = Parameter(data, self.name, self.requires_grad)
        new_param.param_info = self.param_info
        return new_param

    @staticmethod
    def _from_tensor(tensor, *args, **kwargs):
        """Create a `Parameter` that data is shared from a `Tensor`."""
        if not isinstance(tensor, Tensor_):
            raise TypeError(f"The type of input must be Tensor, but got {type(tensor)}.")
        param = Tensor_.__new__(Parameter)
        Tensor_.__init__(param, tensor)
        param.init = None
        param.init_mode = None
        param.is_default_input_init = False
        Parameter.__init__(param, tensor, *args, **kwargs)
        return param

    def set_data(self, data, slice_shape=False):
        """
        Set Parameter's data.

        Args:
            data (Union[Tensor, int, float]): New data.
            slice_shape (bool): If slice the parameter is set to true, the shape is not checked for consistency.
                                Default: False.

        Returns:
            Parameter, the parameter after set data.
        """
        if not isinstance(data, (ms.Tensor, int, float)):
            raise TypeError(f"Parameter data must be [`Tensor`, `int`, `float`] or a kind of `Tensor` "
                            f"(like `Tensor`). But with type {type(data)}.")
        if isinstance(data, (int, float)):
            if self.dtype in mstype.int_type and isinstance(data, float):
                self._raise_type_error(mstype.float_)
            data = Tensor(data, self.dtype)
        # both not init.
        incoming_tensor_is_init = isinstance(data, ms.Tensor) and not data.has_init
        current_tensor_is_init = isinstance(self, Tensor) and not self.has_init
        Parameter._set_data_check_input_valid(self.shape, data.shape, current_tensor_is_init, incoming_tensor_is_init,
                                              slice_shape)
        if self.dtype != data.dtype:
            if mstype.implicit_conversion_seq[self.dtype] < mstype.implicit_conversion_seq[data.dtype]:
                self._raise_type_error(data.dtype)
            else:
                if isinstance(data, ms.Tensor) and data.init is not None:
                    data.init_data()
                data = F.cast(data, self.dtype)
        if isinstance(data, ms.Tensor) and data.has_init:
            # The parameter has been initialized, directly update by the data
            if current_tensor_is_init:
                self._update_tensor_data(data.init_data())
            else:
                # also update the related inited parameter data
                if self.inited_param is not None:
                    self.inited_param.set_data(data)
                self.init_mode = data
        elif incoming_tensor_is_init or current_tensor_is_init:
            self._update_tensor_data(data)
        self.sliced = slice_shape
        return self

    @staticmethod
    def _get_init_data_args(layout=None):
        """Get the data layout args."""
        init_data_args = ()
        if layout:
            if not isinstance(layout, tuple):
                raise TypeError("The argument 'layout' should be tuple, but got {}.".format(type(layout)))
            if len(layout) < 6:
                raise ValueError("The length of 'layout' must be larger than 5, but got {}.".format(len(layout)))
            slice_index = int(_get_slice_index(layout[0], layout[1]))
            init_data_args += (slice_index, layout[2], layout[5])
        return init_data_args

    def init_data(self, layout=None, set_sliced=False):
        """
        Initialize the parameter's data.

        Args:
            layout (Union[None, tuple]): The parameter's layout info.
                layout [dev_mat, tensor_map, slice_shape, filed_size, uniform_split, opt_shard_group]. Default: None.
                It's not None only in 'SEMI_AUTO_PARALLEL' or 'AUTO_PARALLEL' mode.

                - dev_mat (list(int)): The parameter's device matrix.
                - tensor_map (list(int)): The parameter's tensor map.
                - slice_shape (list(int)): The parameter's slice shape.
                - filed_size (int): The parameter's filed size.
                - uniform_split (bool): Whether the parameter is split evenly.
                - opt_shard_group (str): The group of the parameter while running optimizer parallel.

            set_sliced (bool): True if the parameter is set sliced after initializing the data.
                Default: False.

        Raises:
            RuntimeError: If it is from Initializer, and parallel mode has changed after the Initializer created.
            ValueError: If the length of the layout is less than 6.
            TypeError: If `layout` is not tuple.

        Returns:
            Parameter, the `Parameter` after initializing data. If current `Parameter` was already initialized before,
            returns the same initialized `Parameter`.
        """
        if self.is_default_input_init and self.is_in_parallel != _is_in_parallel_mode():
            raise RuntimeError("Must set or change parallel mode before any Tensor created.")
        if self.init_mode is None:
            return self
        if self.inited_param is not None:
            return self.inited_param

        init_data_args = self._get_init_data_args(layout)

        if self.init_in_server and self.is_param_ps and isinstance(self.init_mode, Tensor) and \
                self.init_mode.init is not None and (_is_role_worker() or _is_role_sched()):
            if self.cache_enable:
                data = self.init_mode.init_data(*init_data_args)
            else:
                data = self.init_mode.init_data(0, [1])
        else:
            data = self.init_mode.init_data(*init_data_args)

        obj = self._update_tensor_data(data)
        if id(obj) != id(self):
            self._inited_param = obj
        obj.init_mode = None
        obj.sliced = set_sliced
        return obj

    def requires_grad_(self, requires_grad=True):
        self.requires_grad = requires_grad

    def detach(self):
        return cast_to_adapter_tensor(ms.Parameter.value(self))

class ParameterTuple(tuple):
    """
    Inherited from tuple, ParameterTuple  is used to save multiple parameter.

    Note:
        It is used to store the parameters of the network into the parameter tuple collection.
    """
    def __new__(cls, iterable):
        """Create instance object of ParameterTuple."""
        data = tuple(iterable)
        ids = set()
        names = set()
        for x in data:
            if not isinstance(x, Parameter):
                raise TypeError(f"For ParameterTuple initialization, "
                                f"ParameterTuple input should be 'Parameter' collection, "
                                f"but got a {type(iterable)}. ")
            if id(x) not in ids:
                if x.name in names:
                    raise ValueError("The value {} , its name '{}' already exists. "
                                     "Please set a unique name for the parameter.".format(x, x.name))
                names.add(x.name)
                ids.add(id(x))
        return tuple.__new__(ParameterTuple, tuple(data))

    def clone(self, prefix, init='same'):
        """
        Clone the parameters in ParameterTuple element-wisely to generate a new ParameterTuple.

        Args:
            prefix (str): Namespace of parameter, the prefix string will be added to the names of parameters
                in parametertuple.

            init (Union[Tensor, str, numbers.Number]): Clone the shape and dtype of Parameters in ParameterTuple and
                set  data according to `init`. Default: 'same'.
                If `init` is a `Tensor` , set the new Parameter data to the input Tensor.
                If `init` is `numbers.Number` , set the new Parameter data to the input number.
                If `init` is a `str`, data will be seted according to the initialization method of the same name in
                the `Initializer`.
                If `init` is 'same', the new Parameter has the same value with the original Parameter.


        Returns:
            Tuple, the new Parameter tuple.
        """
        Validator.check_str_by_regular(prefix)
        new = []
        for x in self:
            x1 = x.clone(init)
            x1.name = prefix + "." + x1.name
            new.append(x1)

            if not x1.cache_enable:
                continue

            if _is_role_worker():
                _clone_hash_table(x.name, x.key, x1.name, x1.key)
                _insert_accumu_init_info(x1.name, init_to_value(init))
        return ParameterTuple(new)

    def __parameter_tuple__(self):
        """For parse check."""
