import os
from typing import Mapping, Union
from typing_extensions import TypeGuard
from numbers import Number

import numpy
import h5py
from silx.io import h5py_utils
from silx.io.url import DataUrl


def is_data(data) -> TypeGuard[Union[numpy.ndarray, Number, str, list]]:
    if isinstance(data, (numpy.ndarray, Number)):
        return True
    if isinstance(data, (str, list)) and data:
        return True
    return False


def data_from_storage(data, remove_numpy=True):
    if isinstance(data, numpy.ndarray):
        if not remove_numpy:
            return data
        elif data.ndim == 0:
            return data.item()
        else:
            return data.tolist()
    elif isinstance(data, Mapping):
        return {
            k: data_from_storage(v, remove_numpy=remove_numpy)
            for k, v in data.items()
            if not k.startswith("@")
        }
    else:
        return data


@h5py_utils.retry()
def link_bliss_scan(outentry: h5py.Group, bliss_scan_url: Union[str, DataUrl]):
    if isinstance(bliss_scan_url, str):
        bliss_scan_url = DataUrl(bliss_scan_url)
    file_path = bliss_scan_url.file_path()
    data_path = bliss_scan_url.data_path()
    out_filename = outentry.file.filename
    ext_filename = os.path.relpath(out_filename, os.path.dirname(file_path))
    if ".." in ext_filename:
        ext_filename = file_path
    with h5py_utils.File(file_path, mode="r") as root:
        inentry = root[data_path]
        # Link to the entire group
        for groupname in ("instrument", "sample"):
            if groupname in outentry or groupname not in inentry:
                continue
            outentry[groupname] = h5py.ExternalLink(
                ext_filename, inentry[groupname].name
            )
        # Link to all sub groups
        for groupname in ("measurement",):
            if groupname not in inentry:
                continue
            igroup = inentry[groupname]
            if groupname in outentry:
                ogroup = outentry[groupname]
            else:
                ogroup = outentry.create_group(groupname)
                ogroup.attrs["NX_class"] = igroup.attrs["NX_class"]
            for name in igroup.keys():
                if name in ogroup:
                    continue
                if name not in ogroup:
                    ogroup[name] = h5py.ExternalLink(ext_filename, igroup[name].name)


def convert_to_3d(data: Union[numpy.ndarray, Number, str, list]):
    data_arr = numpy.array(data)

    if data_arr.ndim >= 3:
        return data_arr

    if data_arr.ndim == 2:
        return data_arr.reshape(1, *data_arr.shape)

    if data_arr.ndim == 1:
        return data_arr.reshape(1, 1, *data_arr.shape)

    return data_arr.reshape(1, 1, 1)
