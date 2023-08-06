#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numbers
import warnings
import math

import mindspore as ms
from mindspore.nn.layer.rnns import _DynamicRNNRelu, _DynamicRNNTanh, _DynamicLSTMCPUGPU, _DynamicLSTMAscend, \
                                    _DynamicGRUAscend, _DynamicGRUCPUGPU
from mindspore.nn.layer.rnn_cells import _rnn_tanh_cell, _rnn_relu_cell, _lstm_cell, _gru_cell

from msadapter.pytorch.nn.modules.module import Module
from msadapter.pytorch.tensor import cast_to_ms_tensor, cast_to_adapter_tensor
from msadapter.pytorch.nn.parameter import Parameter
from msadapter.pytorch.functional import empty, zeros
from msadapter.pytorch.nn import init
from msadapter.utils import unsupported_attr, is_under_ascend_context


class RNNBase(Module):
    def __init__(self, mode, input_size, hidden_size,
                 num_layers=1, bias=True, batch_first=False,
                 dropout=0., bidirectional=False, proj_size=0,
                 device=None, dtype=None):
        unsupported_attr(device)
        super(RNNBase, self).__init__()
        self.mode = mode
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.bias = bias
        self.batch_first = batch_first
        self.dropout = float(dropout)
        self.bidirectional = bidirectional
        self.proj_size = proj_size
        self.num_directions = 2 if bidirectional else 1

        if not isinstance(dropout, numbers.Number) or not 0 <= dropout <= 1 or \
                isinstance(dropout, bool):
            raise ValueError("dropout should be a number in range [0, 1] "
                             "representing the probability of an element being "
                             "zeroed")
        if dropout > 0 and num_layers == 1:
            warnings.warn("dropout option adds dropout after all but last "
                          "recurrent layer, so non-zero dropout expects "
                          "num_layers greater than 1, but got dropout={} and "
                          "num_layers={}".format(dropout, num_layers))
        if proj_size < 0:
            raise ValueError("proj_size should be a positive integer or zero to disable projections")
        if proj_size >= hidden_size:
            raise ValueError("proj_size has to be smaller than hidden_size")

        if mode == 'LSTM':
            gate_size = 4 * hidden_size
        elif mode == 'GRU':
            if is_under_ascend_context() and hidden_size % 16 != 0:
                raise ValueError(f"GRU on ascend do not support hidden size that is not divisible by 16, "
                                 f"but get hidden size {hidden_size}, please reset the argument.")
            gate_size = 3 * hidden_size
        elif mode == 'RNN_TANH':
            gate_size = hidden_size
        elif mode == 'RNN_RELU':
            gate_size = hidden_size
        else:
            raise ValueError("Unrecognized RNN mode: " + mode)

        self._flat_weights_names = []
        self._all_weights = []
        for layer in range(num_layers):
            for direction in range(self.num_directions):
                real_hidden_size = proj_size if proj_size > 0 else hidden_size
                layer_input_size = input_size if layer == 0 else real_hidden_size * self.num_directions

                w_ih = Parameter(empty((gate_size, layer_input_size), dtype=dtype))
                w_hh = Parameter(empty((gate_size, real_hidden_size), dtype=dtype))
                b_ih = Parameter(empty(gate_size, dtype=dtype))
                b_hh = Parameter(empty(gate_size, dtype=dtype))
                layer_params = ()
                if self.proj_size == 0:
                    if bias:
                        layer_params = (w_ih, w_hh, b_ih, b_hh)
                    else:
                        layer_params = (w_ih, w_hh)
                else:
                    w_hr = Parameter(empty((proj_size, hidden_size), dtype=dtype))
                    if bias:
                        layer_params = (w_ih, w_hh, b_ih, b_hh, w_hr)
                    else:
                        layer_params = (w_ih, w_hh, w_hr)

                suffix = '_reverse' if direction == 1 else ''
                param_names = ['weight_ih_l{}{}', 'weight_hh_l{}{}']
                if bias:
                    param_names += ['bias_ih_l{}{}', 'bias_hh_l{}{}']
                if self.proj_size > 0:
                    param_names += ['weight_hr_l{}{}']
                param_names = [x.format(layer, suffix) for x in param_names]

                for name, param in zip(param_names, layer_params):
                    setattr(self, name, param)
                self._flat_weights_names.extend(param_names)
                self._all_weights.append(param_names)

        self._flat_weights = \
            [(lambda wn: getattr(self, wn) if hasattr(self, wn) else None)(wn) for wn in self._flat_weights_names]
        self.reset_parameters()

    def __setattr__(self, attr, value):
        if hasattr(self, "_flat_weights_names") and attr in self._flat_weights_names:
            # keep self._flat_weights up to date if you do self.weight = ...
            idx = self._flat_weights_names.index(attr)
            self._flat_weights[idx] = value
        super(RNNBase, self).__setattr__(attr, value)

    def reset_parameters(self) -> None:
        stdv = 1.0 / math.sqrt(self.hidden_size) if self.hidden_size > 0 else 0
        for weight in self.parameters():
            init.uniform_(weight, -stdv, stdv)

    def extra_repr(self):
        s = '{input_size}, {hidden_size}'
        if self.proj_size != 0:
            s += ', proj_size={proj_size}'
        if self.num_layers != 1:
            s += ', num_layers={num_layers}'
        if self.bias is not True:
            s += ', bias={bias}'
        if self.batch_first is not False:
            s += ', batch_first={batch_first}'
        if self.dropout != 0:
            s += ', dropout={dropout}'
        if self.bidirectional is not False:
            s += ', bidirectional={bidirectional}'
        return s.format(**self.__dict__)

    @property
    def all_weights(self):
        return [[getattr(self, weight) for weight in weights] for weights in self._all_weights]

    def __setstate__(self, d):
        super(RNNBase, self).__setstate__(d)
        if 'all_weights' in d:
            self._all_weights = d['all_weights']
        # In PyTorch 1.8 we added a proj_size member variable to LSTM.
        # LSTMs that were serialized via torch.save(module) before PyTorch 1.8
        # don't have it, so to preserve compatibility we set proj_size here.
        if 'proj_size' not in d:
            self.proj_size = 0

        if isinstance(self._all_weights[0][0], str):
            return
        num_layers = self.num_layers
        num_directions = 2 if self.bidirectional else 1
        self._flat_weights_names = []
        self._all_weights = []
        for layer in range(num_layers):
            for direction in range(num_directions):
                suffix = '_reverse' if direction == 1 else ''
                weights = ['weight_ih_l{}{}', 'weight_hh_l{}{}', 'bias_ih_l{}{}',
                           'bias_hh_l{}{}', 'weight_hr_l{}{}']
                weights = [x.format(layer, suffix) for x in weights]
                if self.bias:
                    if self.proj_size > 0:
                        self._all_weights += [weights]
                        self._flat_weights_names.extend(weights)
                    else:
                        self._all_weights += [weights[:4]]
                        self._flat_weights_names.extend(weights[:4])
                else:
                    if self.proj_size > 0:
                        self._all_weights += [weights[:2]] + [weights[-1:]]
                        self._flat_weights_names.extend(weights[:2] + [weights[-1:]])
                    else:
                        self._all_weights += [weights[:2]]
                        self._flat_weights_names.extend(weights[:2])
        self._flat_weights = \
            [(lambda wn: getattr(self, wn) if hasattr(self, wn) else None)(wn) for wn in self._flat_weights_names]

    def _get_weight_and_bias(self, num_directions, layer, bias):
        _param_nums_per_directions = 4 if bias else 2
        _param_nums_per_layer = num_directions * _param_nums_per_directions
        offset = _param_nums_per_layer * layer

        param = ()

        for _ in range(num_directions):
            if bias:
                param += tuple(self._flat_weights[offset:offset + _param_nums_per_directions])
            else:
                param += tuple(self._flat_weights[offset:offset + _param_nums_per_directions])
                param += (None, None)
            offset = offset + _param_nums_per_directions

        return param

    def forward(self, input, hx=None):
        if len(input.shape) not in (2, 3):
            raise RuntimeError(f"For RNN, input should be 2D or 3D, but got {len(input.shape)}D.")

        is_batched = len(input.shape) == 3

        input = cast_to_ms_tensor(input)

        if not is_batched:
            input = ms.ops.unsqueeze(input, 1)
        else:
            if self.batch_first:
                input = ms.ops.transpose(input, (1, 0, 2))

        x_dtype = input.dtype
        max_batch_size = input.shape[1]
        num_directions = 2 if self.bidirectional else 1
        if hx is None:
            hx = zeros(self.num_layers * num_directions,
                       max_batch_size, self.hidden_size,
                       dtype=x_dtype)
            hx = cast_to_ms_tensor(hx)
        else:
            hx = cast_to_ms_tensor(hx)
            if len(hx.shape) not in (2, 3):
                raise RuntimeError(f"For RNN, hx should be 2D or 3D, but got {len(hx.shape)}D.")
            if not is_batched:
                if len(hx.shape) != 2:
                    raise RuntimeError("For RNN, hx ndim should be equal to input")
                hx = ms.ops.unsqueeze(hx, 1)

        pre_layer = input
        h_n = ()
        # For jit
        output = None

        if num_directions == 1:
            for i in range(self.num_layers):
                w_ih, w_hh, b_ih, b_hh = self._get_weight_and_bias(num_directions, i, self.bias)
                output, h_t = self.rnn_cell(pre_layer, hx[i], None, w_ih, w_hh, b_ih, b_hh)
                h_n += (h_t,)

                pre_layer = ms.ops.dropout(output, 1 - self.dropout) \
                    if (self.dropout != 0 and i < self.num_layers - 1) else output
        else:
            for i in range(self.num_layers):
                w_ih, w_hh, b_ih, b_hh, w_ih_b, w_hh_b, b_ih_b, b_hh_b = \
                    self._get_weight_and_bias(num_directions, i, self.bias)

                x_b = ms.ops.reverse(pre_layer, [0])
                output, h_t = self.rnn_cell(pre_layer, hx[2 * i], None, w_ih, w_hh, b_ih, b_hh)
                output_b, h_t_b = self.rnn_cell(x_b, hx[2 * i + 1], None, w_ih_b, w_hh_b, b_ih_b, b_hh_b)

                output_b = ms.ops.reverse(output_b, [0])
                output = ms.ops.concat((output, output_b), 2)
                h_n += (h_t,)
                h_n += (h_t_b,)

                pre_layer = ms.ops.dropout(output, 1 - self.dropout) \
                    if (self.dropout != 0 and i < self.num_layers - 1) else output

        h_n = ms.ops.concat(h_n, 0)
        h_n = h_n.view(hx.shape)

        if not is_batched:
            output = ms.ops.squeeze(output, 1)
            h_n = ms.ops.squeeze(h_n, 1)
        else:
            if self.batch_first:
                output = ms.ops.transpose(output, (1, 0, 2))
        return cast_to_adapter_tensor(output.astype(x_dtype)), cast_to_adapter_tensor(h_n.astype(x_dtype))

class RNN(RNNBase):
    def __init__(self, *args, **kwargs):
        if 'proj_size' in kwargs:
            raise ValueError("proj_size argument is only supported for LSTM, not RNN or GRU")
        self.nonlinearity = kwargs.pop('nonlinearity', 'tanh')
        if self.nonlinearity == 'tanh':
            mode = 'RNN_TANH'
        elif self.nonlinearity == 'relu':
            mode = 'RNN_RELU'
        else:
            raise ValueError("Unknown nonlinearity '{}'".format(self.nonlinearity))
        super(RNN, self).__init__(mode, *args, **kwargs)

        if mode == 'RNN_TANH':
            self.rnn_cell = _DynamicRNNRelu()
        elif mode == 'RNN_RELU':
            self.rnn_cell = _DynamicRNNTanh()

class GRU(RNNBase):
    def __init__(self, *args, **kwargs):
        if 'proj_size' in kwargs:
            raise ValueError("proj_size argument is only supported for LSTM, not RNN or GRU")

        super(GRU, self).__init__('GRU', *args, **kwargs)

        if is_under_ascend_context():
            self.rnn_cell = _DynamicGRUAscend()
        else:
            self.rnn_cell = _DynamicGRUCPUGPU()

class LSTM(RNNBase):
    def __init__(self, *args, **kwargs):
        super(LSTM, self).__init__('LSTM', *args, **kwargs)
        if self.proj_size > 0:
            raise NotImplementedError("For LSTM, proj_size > 0 is not supported yet.")
        if is_under_ascend_context():
            self.lstm_cell = _DynamicLSTMAscend()
        else:
            self.lstm_cell = _DynamicLSTMCPUGPU()

    def forward(self, input, hx=None):
        if len(input.shape) not in (2, 3):
            raise RuntimeError(f"For LSTM, input should be 2D or 3D, but got {len(input.shape)}D.")

        is_batched = len(input.shape) == 3

        input = cast_to_ms_tensor(input)

        if not is_batched:
            input = ms.ops.unsqueeze(input, 1)
        else:
            if self.batch_first:
                input = ms.ops.transpose(input, (1, 0, 2))

        x_dtype = input.dtype
        max_batch_size = input.shape[1]
        num_directions = 2 if self.bidirectional else 1
        real_hidden_size = self.proj_size if self.proj_size > 0 else self.hidden_size
        if hx is None:
            h_zeros = zeros(self.num_layers * num_directions,
                            max_batch_size, real_hidden_size,
                            dtype=x_dtype)
            c_zeros = zeros(self.num_layers * num_directions,
                            max_batch_size, self.hidden_size,
                            dtype=x_dtype)
            hx = (h_zeros, c_zeros)
            hx = cast_to_ms_tensor(hx)
        else:
            hx = cast_to_ms_tensor(hx)
            if is_batched:
                if (len(hx[0].shape) != 3 or len(hx[1].shape) != 3):
                    msg = ("For batched 3-D input, hx and cx should "
                           f"also be 3-D but got ({len(hx[0].shape)}-D, {len(hx[1].shape)}-D) tensors")
                    raise RuntimeError(msg)
            else:
                if len(hx[0].shape) != 2 or len(hx[1].shape) != 2:
                    msg = ("For unbatched 2-D input, hx and cx should "
                           f"also be 2-D but got ({len(hx[0].shape)}-D, {len(hx[1].shape)}-D) tensors")
                    raise RuntimeError(msg)
                hx = (ms.ops.unsqueeze(hx[0], 1), ms.ops.unsqueeze(hx[1], 1))

        pre_layer = input
        h_n = ()
        c_n = ()
        # For jit
        output = None

        if num_directions == 1:
            for i in range(self.num_layers):
                w_ih, w_hh, b_ih, b_hh = self._get_weight_and_bias(num_directions, i, self.bias)

                h_i = (hx[0][i], hx[1][i])
                output, hc_t = self.lstm_cell(pre_layer, h_i, None, w_ih, w_hh, b_ih, b_hh)
                h_t, c_t = hc_t
                h_n += (h_t,)
                c_n += (c_t,)

                pre_layer = ms.ops.dropout(output, 1 - self.dropout) \
                    if (self.dropout != 0 and i < self.num_layers - 1) else output
        else:
            for i in range(self.num_layers):
                w_ih, w_hh, b_ih, b_hh, w_ih_b, w_hh_b, b_ih_b, b_hh_b = \
                    self._get_weight_and_bias(num_directions, i, self.bias)

                x_b = ms.ops.reverse(pre_layer, [0])
                h_i = (hx[0][2 * i], hx[1][2 * i])
                h_b_i = (hx[0][2 * i + 1], hx[1][2 * i + 1])
                output, hc_t = self.lstm_cell(pre_layer, h_i, None, w_ih, w_hh, b_ih, b_hh)
                output_b, hc_t_b = self.lstm_cell(x_b, h_b_i, None, w_ih_b, w_hh_b, b_ih_b, b_hh_b)

                output_b = ms.ops.reverse(output_b, [0])
                output = ms.ops.concat((output, output_b), 2)
                h_t, c_t = hc_t
                h_t_b, c_t_b = hc_t_b
                h_n += (h_t,)
                h_n += (h_t_b,)
                c_n += (c_t,)
                c_n += (c_t_b,)

                pre_layer = ms.ops.dropout(output, 1 - self.dropout) \
                    if (self.dropout != 0 and i < self.num_layers - 1) else output

        h_n = ms.ops.concat(h_n, 0)
        h_n = h_n.view(hx[0].shape)
        c_n = ms.ops.concat(c_n, 0)
        c_n = c_n.view(hx[1].shape)
        if not is_batched:
            output = ms.ops.squeeze(output, 1)
            h_n = ms.ops.squeeze(h_n, 1)
            c_n = ms.ops.squeeze(c_n, 1)
        else:
            if self.batch_first:
                output = ms.ops.transpose(output, (1, 0, 2))
        return cast_to_adapter_tensor(output.astype(x_dtype)), \
                cast_to_adapter_tensor((h_n.astype(x_dtype), c_n.astype(x_dtype)))


class RNNCellBase(Module):
    def __init__(self, input_size, hidden_size, bias, num_chunks, device=None, dtype=None):
        unsupported_attr(device)
        super(RNNCellBase, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.bias = bias
        self.weight_ih = Parameter(empty((num_chunks * hidden_size, input_size), dtype=dtype))
        self.weight_hh = Parameter(empty((num_chunks * hidden_size, hidden_size), dtype=dtype))
        if bias:
            self.bias_ih = Parameter(empty(num_chunks * hidden_size, dtype=dtype))
            self.bias_hh = Parameter(empty(num_chunks * hidden_size, dtype=dtype))
        else:
            self.register_parameter('bias_ih', None)
            self.register_parameter('bias_hh', None)

        self._rnn_cell = None
        self.reset_parameters()

    def extra_repr(self) -> str:
        s = '{input_size}, {hidden_size}'
        if 'bias' in self.__dict__ and self.bias is not True:
            s += ', bias={bias}'
        if 'nonlinearity' in self.__dict__ and self.nonlinearity != "tanh":
            s += ', nonlinearity={nonlinearity}'
        return s.format(**self.__dict__)

    def reset_parameters(self) -> None:
        stdv = 1.0 / math.sqrt(self.hidden_size) if self.hidden_size > 0 else 0
        for weight in self.parameters():
            init.uniform_(weight, -stdv, stdv)

    def forward(self, input, hx=None):
        input = cast_to_ms_tensor(input)

        if len(input.shape) not in (1, 2):
            raise RuntimeError(f"RNNCell: Expected input to be 1-D or 2-D but received {len(input.shape)}-D tensor")
        is_batched = len(input.shape) == 2
        if not is_batched:
            input = ms.ops.unsqueeze(input, 0)

        if hx is None:
            hx = zeros(input.shape[0], self.hidden_size, dtype=input.dtype)
            hx = cast_to_ms_tensor(hx)
        else:
            hx = cast_to_ms_tensor(hx)
            hx = ms.ops.unsqueeze(hx, 0) if not is_batched else hx

        ret = self._rnn_cell(input, hx, self.weight_ih, self.weight_hh, self.bias_ih, self.bias_hh)
        if not is_batched:
            ret = ms.ops.squeeze(ret, 0)
        return cast_to_adapter_tensor(ret)

class RNNCell(RNNCellBase):
    def __init__(self, input_size, hidden_size, bias=True, nonlinearity="tanh",
                 device=None, dtype=None):
        super(RNNCell, self).__init__(input_size, hidden_size, bias, num_chunks=1, device=device, dtype=dtype)
        self.nonlinearity = nonlinearity
        if self.nonlinearity == "tanh":
            self._rnn_cell = _rnn_tanh_cell
        elif self.nonlinearity == "relu":
            self._rnn_cell = _rnn_relu_cell
        else:
            raise RuntimeError(
                "Unknown nonlinearity: {}".format(self.nonlinearity))

class LSTMCell(RNNCellBase):
    def __init__(self, input_size, hidden_size, bias=True, device=None, dtype=None):
        super(LSTMCell, self).__init__(input_size, hidden_size, bias, num_chunks=4, device=device, dtype=dtype)

    def forward(self, input, hx=None):
        input = cast_to_ms_tensor(input)
        if len(input.shape) not in (1, 2):
            raise RuntimeError(f"LSTMCell: Expected input to be 1-D or 2-D but received {len(input.shape)}-D tensor")
        is_batched = len(input.shape) == 2
        if not is_batched:
            input = ms.ops.unsqueeze(input, 0)

        if hx is None:
            _zeros = zeros(input.shape[0], self.hidden_size, dtype=input.dtype)
            hx = (_zeros, _zeros)
            hx = cast_to_ms_tensor(hx)
        else:
            hx = cast_to_ms_tensor(hx)
            hx = (ms.ops.unsqueeze(hx[0], 0), ms.ops.unsqueeze(hx[1], 0)) if not is_batched else hx

        hx = cast_to_ms_tensor(hx)

        ret = _lstm_cell(input, hx, self.weight_ih, self.weight_hh, self.bias_ih, self.bias_hh)

        if not is_batched:
            ret = (ms.ops.squeeze(ret[0], 0), ms.ops.squeeze(ret[1], 0))
        return cast_to_adapter_tensor(ret)


class GRUCell(RNNCellBase):
    def __init__(self, input_size, hidden_size, bias=True, device=None, dtype=None):
        super(GRUCell, self).__init__(input_size, hidden_size, bias, num_chunks=3, device=device, dtype=dtype)
        self._rnn_cell = _gru_cell
