from collections import OrderedDict
from mindspore import save_checkpoint, load_checkpoint
from msadapter.utils import unsupported_attr

def save(obj, f, pickle_module=None, pickle_protocol=None, _use_new_zipfile_serialization=None):
    """
    Saves an object to a disk file. Note: save supports saving ckpt files only
    Args:
        obj: saved object
        f: a file-like object (has to implement write and flush) or a string or
           os.PathLike object containing a file name

    """
    unsupported_attr(pickle_module)
    unsupported_attr(pickle_protocol)
    unsupported_attr(_use_new_zipfile_serialization)

    if isinstance(obj, OrderedDict):
        ms_params  = []
        for name, value in obj.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    param_dict = {}
                    param_dict['name'] = k
                    param_dict['data'] = v
                    ms_params.append(param_dict)
            else:
                param_dict = {}
                param_dict['name'] = name
                param_dict['data'] = value
                ms_params.append(param_dict)
        save_checkpoint(ms_params, f)
    else:
        #TODO Saving network structure needs to be implemented
        save_checkpoint(obj, f)

def load(f, map_location=None, pickle_module=None, **pickle_load_args):
    """load(f, map_location=None, pickle_module=pickle, **pickle_load_args)
    Loads an object saved with :func:`torch.save` from a file.

    Args:
        f: a file-like object (has to implement :meth:`read`, :meth:`readline`, :meth:`tell`, and :meth:`seek`),
            or a string or os.PathLike object containing a file name
    """
    unsupported_attr(map_location)
    unsupported_attr(pickle_module)
    unsupported_attr(pickle_load_args)

    if f[-5:] == ".ckpt":
        parameter_dict = load_checkpoint(f, net=None)
        return parameter_dict
    else:
        raise ValueError("For 'load', only ckpt files can be loaded.")
