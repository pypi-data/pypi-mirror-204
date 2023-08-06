#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple

import mindspore as ms
from mindspore.ops.primitive import _primexpr
from msadapter.pytorch.tensor import cast_to_ms_tensor, cast_to_adapter_tensor
from msadapter.utils import unsupported_attr, pynative_mode_condition
from .container import Sequential, ModuleList
from .linear import Linear
from .module import Module
from ..functional import log_softmax

@_primexpr
def _ASMoutput():
    return namedtuple('_ASMoutput', ['output', 'loss'])

class AdaptiveLogSoftmaxWithLoss(Module):
    def __init__(self, in_features, n_classes, cutoffs, div_value=4., head_bias=False, device=None, dtype=None):
        super(AdaptiveLogSoftmaxWithLoss, self).__init__()
        unsupported_attr(device)
        cutoffs = list(cutoffs)
        # #TODO: pylint
        # if (cutoffs != sorted(cutoffs)) \
        #         or (min(cutoffs) <= 0) \
        #         or (max(cutoffs) > (n_classes - 1)) \
        #         or (len(set(cutoffs)) != len(cutoffs)) \
        #         or any([int(c) != c for c in cutoffs]):
        #
        #     raise ValueError("cutoffs should be a sequence of unique, positive "
        #                      "integers sorted in an increasing order, where "
        #                      "each value is between 1 and n_classes-1")

        self.in_features = in_features
        self.n_classes = n_classes
        self.cutoffs = cutoffs + [n_classes]
        self.div_value = div_value
        self.head_bias = head_bias
        self.dtype = dtype

        self.shortlist_size = self.cutoffs[0]
        self.n_clusters = len(self.cutoffs) - 1
        self.head_size = self.shortlist_size + self.n_clusters

        self.head = Linear(self.in_features, self.head_size, bias=self.head_bias, dtype=self.dtype)
        self.tail = ModuleList()

        for i in range(self.n_clusters):

            hsz = int(self.in_features // (self.div_value ** (i + 1)))
            osz = self.cutoffs[i + 1] - self.cutoffs[i]

            projection = Sequential(
                Linear(self.in_features, hsz, bias=False, dtype=self.dtype),
                Linear(hsz, osz, bias=False, dtype=self.dtype),
            )

            self.tail.append(projection)

    def reset_parameters(self):
        self.head.reset_parameters()
        for i2h, h2o in self.tail:
            i2h.reset_parameters()
            h2o.reset_parameters()

    def forward(self, input_, target_):
        input_ = cast_to_ms_tensor(input_)
        #target_ = cast_to_ms_tensor(target_)
        targ_dim = target_.dim()

        if targ_dim == 1:
            if input_.shape[0] != target_.shape[0]:
                raise RuntimeError('Input and target should have the same size '
                                   'in the batch dimension.')
            if input_.dim() != 2:
                raise RuntimeError('1D target tensor expects 2D input tensors, '
                                   'but found inputs with size', input_.shape())
        elif targ_dim == 0:
            if input_.dim() != 1:
                raise RuntimeError('0D target tensor expects 1D input tensors, '
                                   'but found inputs with size', input_.shape())
        else:
            raise RuntimeError('0D or 1D target tensor expected, '
                               'multi-target not supported')

        is_batched = targ_dim > 0
        input = input_ if is_batched else input_.unsqueeze(0)
        target = target_ if is_batched else target_.unsqueeze(0)

        used_rows = 0
        batch_size = target.shape[0]

        output = input.new_zeros(batch_size)
        #gather_inds = ms.numpy.empty(batch_size, target.dtype)
        gather_inds = target.new_empty(batch_size)

        cutoff_values = [0] + self.cutoffs
        for i in range(len(cutoff_values) - 1):

            low_idx = cutoff_values[i]
            high_idx = cutoff_values[i + 1]

            target_mask = (target >= low_idx) & (target < high_idx)
            row_indices = target_mask.nonzero().squeeze()

            if row_indices.numel() == 0:
                continue

            if i == 0:
                #gather_inds.index_copy_(0, row_indices, target[target_mask])
                gather_inds = index_copy_0dim(gather_inds, row_indices, target[target_mask])

            else:
                relative_target = target[target_mask] - low_idx
                #input_subset = input.index_select(0, row_indices)
                input_subset = ms.ops.gather(input, row_indices, 0)

                cluster_output = self.tail[i - 1](input_subset)
                cluster_index = self.shortlist_size + i - 1

                gather_inds.index_fill_(0, row_indices, cluster_index)
                cluster_logprob = log_softmax(cluster_output, dim=1)
                local_logprob = cluster_logprob.gather(1, relative_target.unsqueeze(1))
                #output.index_copy_(0, row_indices, local_logprob.squeeze(1))
                output = index_copy_0dim(output, row_indices, local_logprob.squeeze(1))

            used_rows += row_indices.numel()

        if used_rows != batch_size:
            raise RuntimeError("Target values should be in [0, {}], "
                               "but values in range [{}, {}] "
                               "were found. ".format(self.n_classes - 1,
                                                     target.min().item(),
                                                     target.max().item()))

        head_output = self.head(input)
        head_logprob = log_softmax(head_output, dim=1)
        output += head_logprob.gather(1, gather_inds.unsqueeze(1)).squeeze()
        loss = (-output).mean()
        if not is_batched:
            output = output.squeeze(0)

        output = cast_to_adapter_tensor(output)
        loss = cast_to_adapter_tensor(loss)
        if pynative_mode_condition():
            return _ASMoutput()(output, loss)
        return output, loss

    def _get_full_log_prob(self, input, head_output):
        input = cast_to_ms_tensor(input)
        head_output = cast_to_ms_tensor(head_output)
        out = input.new_empty((head_output.shape[0], self.n_classes))
        head_logprob = log_softmax(head_output, dim=1)

        out[:, :self.shortlist_size] = head_logprob[:, :self.shortlist_size]

        for i, (start_idx, stop_idx) in enumerate(zip(self.cutoffs, self.cutoffs[1:])):
            cluster_output = self.tail[i](input)
            cluster_logprob = log_softmax(cluster_output, dim=1)
            output_logprob = cluster_logprob + head_logprob[:, self.shortlist_size + i].unsqueeze(1)

            out[:, start_idx:stop_idx] = output_logprob

        return cast_to_adapter_tensor(out)

    def log_prob(self, input):
        input = cast_to_ms_tensor(input)
        head_output = self.head(input)
        out = self._get_full_log_prob(input, head_output)
        return cast_to_adapter_tensor(out)


    def predict(self, input):
        input = cast_to_ms_tensor(input)
        head_output = self.head(input)
        cast_to_adapter_tensor()
        output = ms.ops.argmax(head_output, axis=1)
        not_in_shortlist = (output >= self.shortlist_size)
        any_in_shortlist = (output < self.shortlist_size)

        if not not_in_shortlist:
            return cast_to_adapter_tensor(output)

        elif not any_in_shortlist:
            log_prob = self._get_full_log_prob(input, head_output)
            return cast_to_adapter_tensor(ms.ops.argmax(log_prob, axis=1))

        else:
            log_prob = self._get_full_log_prob(input[not_in_shortlist],
                                               head_output[not_in_shortlist])
            output[not_in_shortlist] = ms.ops.argmax(log_prob, axis=1)
            return cast_to_adapter_tensor(output)


def index_copy_0dim(input, index, tensor):
    for i in range(len(index)):
        input[index[i]] = tensor[i]
    return input
