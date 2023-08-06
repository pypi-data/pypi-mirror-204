import numpy as np
import mindspore as ms
import mindspore.nn as nn

_error_msg = "[numpy backward issue.] For '{}', it can not backward, please use other function instead."

#TODO: NumpyLstsq constructs the same output that torch.lstsq generates
#Later, torch.lstsq will be deprecated and used linalg.lstsq instead, the NumpyLstsq will be deprecated as well
class NumpyLstsq(nn.Cell):
    def __init__(self, op_name=None):
        super().__init__()
        self.op_name = op_name
    def construct(self, input, A):
        type_np = A.dtype
        shape_np = A.shape
        input_np = input.asnumpy()
        A_np = A.asnumpy()
        output = ms.Tensor(np.linalg.lstsq(A_np, input_np)[0])
        #TODO: linalg.lstsq not support qr as return, thus the qr will be set to zeros
        qr = ms.ops.zeros(shape_np, type_np)
        return output, qr
    def bprop(self, input, A, out, dout):
        raise RuntimeError(_error_msg.format(self.op_name))

#TODO: NumpyLstsq constructs the same output that torch.linalg.lstsq generates
class NumpyFullLstsq(nn.Cell):
    def __init__(self, op_name=None, rcond=None):
        super().__init__()
        self.op_name = op_name
        self.rcond = rcond
    def construct(self, a, b):
        a = a.asnumpy()
        b = b.asnumpy()
        output = np.linalg.lstsq(a, b, rcond=self.rcond)
        x = ms.Tensor(output[0])
        residuals = ms.Tensor(output[1])
        rank = ms.Tensor(output[2])
        s = ms.Tensor(output[3])
        return x, residuals, rank, s
    def bprop(self, a, b, out, dout):
        raise RuntimeError(_error_msg.format(self.op_name))
