#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mindspore.nn.optim import SGD
from mindspore.nn.optim import Adam
from mindspore.nn.optim import Momentum
from mindspore.nn.optim import LARS
from mindspore.nn.optim import AdamWeightDecay
from mindspore.nn.optim import LazyAdam
from mindspore.nn.optim import AdamOffload
from mindspore.nn.optim import Lamb
from mindspore.nn.optim import ASGD
from mindspore.nn.optim import RMSProp
from mindspore.nn.optim import Rprop
from mindspore.nn.optim import FTRL
from mindspore.nn.optim import ProximalAdagrad
from mindspore.nn.optim import Adagrad
from mindspore.nn.optim import thor
from mindspore.nn.optim import AdaFactor
from mindspore.nn.optim import AdaSumByDeltaWeightWrapCell
from mindspore.nn.optim import AdaSumByGradWrapCell
from mindspore.nn.optim import AdaMax
from mindspore.nn.optim import Adadelta

__all__ = ['Momentum', 'LARS', 'Adam', 'AdamWeightDecay', 'LazyAdam', 'AdamOffload',
           'Lamb', 'SGD', 'ASGD', 'Rprop', 'FTRL', 'RMSProp', 'ProximalAdagrad', 'Adagrad', 'thor', 'AdaFactor',
           'AdaSumByDeltaWeightWrapCell', 'AdaSumByGradWrapCell', 'AdaMax', 'Adadelta']
