#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mindspore.nn as nn
from msadapter.pytorch.tensor import cast_to_ms_tensor, cast_to_adapter_tensor
from .module import Module

__all__ = ['ChannelShuffle']


class ChannelShuffle(Module):
    def __init__(self, groups):
        super(ChannelShuffle, self).__init__()
        self.groups = groups
        self.channel_shuffle = nn.ChannelShuffle(self.groups)

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        out = self.channel_shuffle(input)
        return cast_to_adapter_tensor(out)

    def extra_repr(self):
        return 'groups={}'.format(self.groups)
