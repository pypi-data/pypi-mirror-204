import numpy as np
import msadapter.pytorch.common.dtype as _dtype
from msadapter.utils import unsupported_attr

_default_dtype = np.float32
# TODO: to supported more methods
class _TypedStorage():
    def __new__(cls, *args, wrap_storage=None, dtype=None, device=None):
        if cls == _TypedStorage:
            return super().__new__(cls)
        if dtype is not None:
            raise RuntimeError("For TypedStorage, Keyword argument 'dtype' cannot be specified")
        _dtype = _cls_dtype_map.get(cls)
        return _TypedStorage(*args, wrap_storage=wrap_storage, dtype=_dtype, device=device)

    def __init__(self, *args, wrap_storage=None, dtype=None, device=None):
        unsupported_attr(device)
        if wrap_storage is not None:
            raise NotImplementedError("For TypeStorage, `wrap_storage` is not supported yet.")

        if len(args) != 1 or isinstance(args[0], int):
            raise NotImplementedError("For TypeStorage, `args` now only support sequence data.")

        if not dtype:
            dtype = _default_dtype
        self.data = np.frombuffer(args[0], dtype)
        self.dtype = dtype

    @classmethod
    def from_buffer(cls, bytestream):
        _dtype = _cls_dtype_map.get(cls)
        return _TypedStorage(bytestream, dtype=_dtype)

class ByteStorage(_TypedStorage):
    @property
    def dtype(self):
        return _dtype.uint8

# TODO: To supported other type storage.

_cls_dtype_map = {ByteStorage: np.uint8}
