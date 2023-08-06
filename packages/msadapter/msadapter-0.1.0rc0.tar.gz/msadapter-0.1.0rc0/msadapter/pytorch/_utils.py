import sys
import traceback


# class KeyErrorMessage(str):
#     r"""str subclass that returns itself in repr"""
#     def __repr__(self):
#         return self


class ExceptionWrapper:
    r"""Wraps an exception plus traceback to communicate across threads"""
    def __init__(self, exc_info=None, where="in background"):
        if exc_info is None:
            exc_info = sys.exc_info()
        self.exc_type = exc_info[0]
        self.exc_msg = "".join(traceback.format_exception(*exc_info))
        self.where = where

    def reraise(self):
        r"""Reraises the wrapped exception in the current thread"""
        msg = "Caught {} {}.\nOriginal {}".format(
            self.exc_type.__name__, self.where, self.exc_msg)
        if self.exc_type == KeyError:
            # msg = KeyErrorMessage(msg)
            msg = str(msg)
        elif getattr(self.exc_type, "message", None):
            raise self.exc_type(message=msg)
        try:
            exception = self.exc_type(msg)
        except TypeError:
            raise RuntimeError(msg) from None
        raise exception
