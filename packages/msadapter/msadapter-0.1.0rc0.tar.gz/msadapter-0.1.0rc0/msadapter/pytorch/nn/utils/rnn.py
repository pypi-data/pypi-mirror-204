from typing import Iterable
import numpy as np
import mindspore as ms
from msadapter.pytorch.tensor import cast_to_ms_tensor, cast_to_adapter_tensor


def pad_sequence(sequences, batch_first=False, padding_value=0.0):
    if not isinstance(sequences, Iterable):
        msg = ('pad_sequence: Expected iterable for input sequences, but got arg of type: '
               f'{type(sequences)}')
        raise RuntimeError(msg)
    if len(sequences) == 0:
        raise RuntimeError("pad_sequence: received an empty list of sequences")

    sequences = cast_to_ms_tensor(sequences)
    num_samples = len(sequences)
    lengths = []
    sample_shape = ()
    flag = True

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.
    for x in sequences:
        lengths.append(len(x))
        if flag and len(x):
            sample_shape = np.asarray(x).shape[1:]
            flag = False

    maxlen = max(lengths)

    x_shape = (num_samples, maxlen) + sample_shape if batch_first else (maxlen, num_samples) + sample_shape
    x = ms.ops.full(x_shape, padding_value, dtype=sequences[0].dtype)
    for idx, s in enumerate(sequences):
        if batch_first:
            trunc = s[:maxlen]
            x[idx, : len(trunc)] = trunc
        else:
            trunc = s[:maxlen]
            x[ : len(trunc), idx] = trunc
    return cast_to_adapter_tensor(x)
