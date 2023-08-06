#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mindspore as ms
from mindspore.communication.management import init, get_group_size

from msadapter.utils import get_backend
from msadapter.pytorch.tensor import FloatTensor, LongTensor

def is_available():
    backend = get_backend()
    if backend == 'GPU':
        return True
    return False

def current_device():
    return 0

def device_count():
    # TODO Use this method when supported
    # init()
    # return get_group_size()
    return 1

def set_device(device):
    if isinstance(device, int):
        ms.context.set_context(device_id=device)
    elif device in ("gpu", 'GPU'):
        ms.context.set_context(device_target="GPU")
    elif device in ("cpu", "CPU"):
        ms.context.set_context(device_target="CPU")
    elif device in ("ascend", "Ascend"):
        ms.context.set_context(device_target="Ascend")
    else:
        raise ValueError("device must be cpu, gpu, ascend or CPU, GPU, Ascend.")
