from contextlib import contextmanager

import h5py
from silx.io.dictdump import dicttonx

from .utils import data_utils, pyfai_utils
from .data_access import TaskWithDataAccess

__all__ = ["SaveNexusPattern1D", "SaveNexusIntegrated"]


class _BaseSaveNexusIntegrated(
    TaskWithDataAccess,
    input_names=["url"],
    optional_input_names=[
        "bliss_scan_url",
        "metadata",
        "nxprocess_name",
        "nxmeasurement_name",
        "nxprocess_as_default",
    ],
    output_names=["saved"],
    register=False,
):
    @property
    def _process_info(self):
        raise NotImplementedError

    @property
    def _nxprocess_name(self):
        if self.inputs.nxprocess_name:
            return self.inputs.nxprocess_name
        return "integrate"

    @property
    def _nxmeasurement_name(self):
        if self.inputs.nxmeasurement_name:
            return self.inputs.nxmeasurement_name
        return "integrated"

    @contextmanager
    def _save_context(self):
        with self.open_h5item(self.inputs.url, mode="a", create=True) as parent:
            assert isinstance(parent, h5py.Group)
            nxprocess = pyfai_utils.create_nxprocess(
                parent, self._nxprocess_name, self._process_info
            )

            yield nxprocess

            url = data_utils.data_from_storage(
                self.inputs.bliss_scan_url, remove_numpy=True
            )
            if url:
                self.link_bliss_scan(parent, url)
            mark_as_default = self.get_input_value("nxprocess_as_default", True)
            pyfai_utils.create_nxprocess_links(
                nxprocess, self._nxmeasurement_name, mark_as_default=mark_as_default
            )
            if self.inputs.metadata:
                dicttonx(
                    self.inputs.metadata,
                    parent,
                    update_mode="add",
                    add_nx_class=True,
                )
        self.outputs.saved = True


class SaveNexusPattern1D(
    _BaseSaveNexusIntegrated,
    input_names=["x", "y", "xunits"],
    optional_input_names=["header", "yerror"],
):
    def run(self):
        with self._save_context() as nxprocess:
            nxdata = pyfai_utils.create_nxdata(
                nxprocess, self.inputs.y.ndim, self.inputs.x, self.inputs.xunits, None
            )
            nxdata["intensity"] = self.inputs.y
            if not self.missing_inputs.yerror:
                nxdata["intensity_errors"] = self.inputs.yerror

    @property
    def _process_info(self):
        return self.inputs.header


class SaveNexusIntegrated(
    _BaseSaveNexusIntegrated,
    input_names=["radial", "intensity", "radial_units"],
    optional_input_names=["info", "azimuthal", "intensity_error"],
):
    def run(self):
        with self._save_context() as nxprocess:
            nxdata = pyfai_utils.create_nxdata(
                nxprocess,
                self.inputs.intensity.ndim,
                self.inputs.radial,
                self.inputs.radial_units,
                self.inputs.azimuthal,
            )
            nxdata["intensity"] = self.inputs.intensity
            if not self.missing_inputs.intensity_error:
                nxdata["intensity_errors"] = self.inputs.intensity_error

    @property
    def _process_info(self):
        return self.inputs.info
