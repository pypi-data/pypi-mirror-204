import logging
from numbers import Number
from contextlib import contextmanager, ExitStack
from typing import Union, Tuple

import numpy
import h5py
from ewoksdata.data.hdf5.dataset_writer import DatasetWriter

from .worker import persistent_worker
from .worker import set_maximum_persistent_workers
from .utils import data_utils, xrpd_utils, pyfai_utils, integrate_utils
from .data_access import TaskWithDataAccess


__all__ = ["Integrate1D", "IntegrateBlissScan", "IntegrateBlissScanWithoutSaving"]


logger = logging.getLogger(__name__)


class _BaseIntegrate(
    TaskWithDataAccess,
    input_names=["detector", "geometry", "energy"],
    optional_input_names=[
        "detector_config",
        "mask",
        "integration_options",
        "fixed_integration_options",
        "maximum_persistent_workers",
    ],
    register=False,
):
    @contextmanager
    def _worker(self):
        nworkers = self.get_input_value("maximum_persistent_workers", None)
        if nworkers is not None:
            set_maximum_persistent_workers(nworkers)
        options = self._get_pyfai_options()
        with persistent_worker(options) as worker:
            yield worker, options

    def _get_pyfai_options(self) -> dict:
        geometry = data_utils.data_from_storage(self.inputs.geometry)
        xrpd_utils.validate_geometry(geometry)
        integration_options = data_utils.data_from_storage(
            self.inputs.integration_options, remove_numpy=True
        )
        fixed_integration_options = data_utils.data_from_storage(
            self.get_input_value("fixed_integration_options", None), remove_numpy=True
        )
        config = dict()
        if integration_options:
            config.update(integration_options)
        if fixed_integration_options:
            config.update(fixed_integration_options)
        if geometry:
            config.update(geometry)

        config.setdefault("unit", "2th_deg")
        config["detector"] = data_utils.data_from_storage(self.inputs.detector)
        config["detector_config"] = data_utils.data_from_storage(
            self.get_input_value("detector_config", None)
        )
        config["wavelength"] = xrpd_utils.energy_wavelength(self.inputs.energy)
        if not self.missing_inputs.mask and self.inputs.mask is not None:
            config["mask"] = self.get_image(
                data_utils.data_from_storage(self.inputs.mask)
            )
        return config

    def _pyfai_normalization_factor(
        self,
        monitor: Union[numpy.ndarray, Number, str, list, None],
        reference: Union[numpy.ndarray, Number, str, list, None],
    ) -> Tuple[float, float, float]:
        r"""Returns the pyfai normalization factor based on a monitor and a reference value.

        The pyfai normalization factor is defined as

        .. code::

            Inorm = I / normalization_factor

        Monitor normalization is done like this

        .. code::

            Inorm = I / monitor * reference

        which means that the normalization factor is

        .. code::

            normalization_factor = monitor / reference
        """
        if data_utils.is_data(reference):
            reference = self.get_data(reference)
        else:
            reference = 1
        if data_utils.is_data(monitor):
            monitor = self.get_data(monitor)
        else:
            monitor = 1
        normalization_factor = monitor / reference
        return normalization_factor, monitor, reference


class Integrate1D(
    _BaseIntegrate,
    input_names=["image"],
    optional_input_names=["monitor", "reference"],
    output_names=["x", "y", "yerror", "xunits", "info"],
):
    """1D integration of a single diffraction pattern."""

    def run(self):
        raw_data = self.get_image(self.inputs.image)
        normalization_factor, monitor, reference = self._pyfai_normalization_factor(
            self.inputs.monitor, self.inputs.reference
        )

        with self._worker() as (worker, config):
            result = worker.process(raw_data, normalization_factor=normalization_factor)

            self.outputs.x = result.radial
            self.outputs.y = result.intensity
            yerror = integrate_utils.get_yerror(result)
            self.outputs.yerror = numpy.abs(yerror)
            self.outputs.xunits = result.unit.name

            info = pyfai_utils.compile_integration_info(
                config, monitor=monitor, reference=reference
            )
            self.outputs.info = info


class IntegrateBlissScan(
    _BaseIntegrate,
    input_names=["filename", "scan", "detector_name", "output_filename"],
    optional_input_names=[
        "counter_names",
        "monitor_name",
        "reference",
        "subscan",
        "retry_timeout",
        "retry_period",
        "demo",
        "scan_memory_url",
        "nxprocess_name",
        "nxmeasurement_name",
        "nxprocess_as_default",
        "flush_period",
    ],
):
    """1D or 2D integration of a single detector in a single Bliss scan with saving."""

    def run(self):
        if self.inputs.counter_names:
            counter_names = list(self.inputs.counter_names)
        else:
            counter_names = list()

        detector_name = self.inputs.detector_name
        monitor_name = self.get_input_value("monitor_name", None)
        if monitor_name and monitor_name not in counter_names:
            counter_names.append(monitor_name)
        reference = self.get_input_value("reference", None)
        reference_name = None
        if isinstance(reference, str):
            reference_name = reference
            if reference not in counter_names:
                counter_names.append(reference)

        scan = self.inputs.scan
        subscan = self.get_input_value("subscan", 1)
        output_url = f"silx://{self.inputs.output_filename}?path=/{scan}.{subscan}"
        input_url = f"silx://{self.inputs.filename}?path=/{scan}.{subscan}"
        flush_period = self.get_input_value("flush_period", None)

        with ExitStack() as stack:
            worker = None
            parent = None
            nxprocess = None
            measurement = None

            intensity_writer = None
            error_writer = None
            ctr_writers = dict()

            if self.inputs.scan_memory_url:
                logger.info("PyFAI integrate data from %r", self.inputs.scan_memory_url)
                data_iterator = self.iter_bliss_data_from_memory(
                    self.inputs.scan_memory_url,
                    lima_names=[detector_name],
                    counter_names=counter_names,
                )
            else:
                logger.info(
                    "PyFAI integrate data from '%s::%d.%d'",
                    self.inputs.filename,
                    self.inputs.scan,
                    subscan,
                )
                data_iterator = self.iter_bliss_data(
                    self.inputs.filename,
                    self.inputs.scan,
                    lima_names=[detector_name],
                    counter_names=counter_names,
                    subscan=subscan,
                )

            for ptdata in data_iterator:
                if worker is None:
                    # Start the worker + open the output file only after
                    # the first image is read
                    worker, config = stack.enter_context(self._worker())
                    info = pyfai_utils.compile_integration_info(
                        config, reference=reference
                    )

                    parent = stack.enter_context(
                        self.open_h5item(output_url, mode="a", create=True)
                    )
                    assert isinstance(parent, h5py.Group)
                    nxprocess = pyfai_utils.create_nxprocess(
                        parent, self._nxprocess_name, info
                    )

                    if counter_names:
                        measurement = parent.create_group("measurement")
                        measurement.attrs["NX_class"] = "NXcollection"

                normalization_factor, *_ = self._pyfai_normalization_factor(
                    ptdata.get(monitor_name), ptdata.get(reference_name, reference)
                )
                image = ptdata[detector_name]
                if self.inputs.demo:
                    image = image[:-1, :-1]
                result = worker.process(
                    image, normalization_factor=normalization_factor
                )
                if intensity_writer is None:
                    nxdata = pyfai_utils.create_nxdata(
                        nxprocess,
                        result.intensity.ndim + 1,  # +1 for the scan dimension
                        result.radial,
                        result.unit,
                        result.azimuthal if result.intensity.ndim == 2 else None,
                    )
                    intensity_writer = stack.enter_context(
                        DatasetWriter(nxdata, "intensity", flush_period=flush_period)
                    )
                    if result.sigma is not None:
                        error_writer = stack.enter_context(
                            DatasetWriter(
                                nxdata, "intensity_errors", flush_period=flush_period
                            )
                        )
                    for name in counter_names:
                        ctr_writers[name] = stack.enter_context(
                            DatasetWriter(measurement, name, flush_period=flush_period)
                        )

                flush = intensity_writer.add_point(result.intensity)
                if result.sigma is not None:
                    flush |= error_writer.add_point(result.sigma)
                for name in counter_names:
                    flush |= ctr_writers[name].add_point(ptdata[name])
                if flush:
                    parent.file.flush()

            if intensity_writer is None:
                raise RuntimeError("No scan data")
            intensity_writer.flush_buffer()
            if error_writer is not None:
                error_writer.flush_buffer()

            nxdata["points"] = numpy.arange(intensity_writer.dataset.shape[0])
            axes = nxdata.attrs["axes"]
            axes[0] = "points"
            nxdata.attrs["axes"] = axes

            self.link_bliss_scan(parent, input_url)
            mark_as_default = self.get_input_value("nxprocess_as_default", True)
            pyfai_utils.create_nxprocess_links(
                nxprocess, self._nxmeasurement_name, mark_as_default=mark_as_default
            )

    @property
    def _nxprocess_name(self):
        if self.inputs.nxprocess_name:
            return self.inputs.nxprocess_name
        default = "integrate"
        if self.inputs.detector_name:
            return f"{self.inputs.detector_name}_{default}"
        return default

    @property
    def _nxmeasurement_name(self):
        if self.inputs.nxmeasurement_name:
            return self.inputs.nxmeasurement_name
        default = "integrated"
        if self.inputs.detector_name:
            return f"{self.inputs.detector_name}_{default}"
        return default


class IntegrateBlissScanWithoutSaving(
    _BaseIntegrate,
    input_names=["filename", "scan", "detector_name"],
    optional_input_names=[
        "counter_names",
        "monitor_name",
        "reference",
        "subscan",
        "retry_timeout",
        "retry_period",
        "demo",
        "scan_memory_url",
    ],
    output_names=[
        "radial",
        "azimuthal",
        "intensity",
        "intensity_error",
        "radial_units",
        "info",
    ],
):
    """1D or 2D integration of a single detector in a single Bliss scan without saving."""

    def run(self):
        with self._worker() as (worker, config):
            if self.inputs.counter_names:
                counter_names = list(self.inputs.counter_names)
            else:
                counter_names = list()
            detector_name = self.inputs.detector_name
            monitor_name = self.get_input_value("monitor_name", None)
            if monitor_name and monitor_name not in counter_names:
                counter_names.append(monitor_name)
            reference = self.get_input_value("reference", None)
            reference_name = None
            if isinstance(reference, str):
                reference_name = reference
                if reference not in counter_names:
                    counter_names.append(reference)
            subscan = self.get_input_value("subscan", None)

            intensities = []
            sigmas = []
            radial = None
            unit = None
            azimuthal = None

            if self.inputs.scan_memory_url:
                logger.info("PyFAI integrate data from %r", self.inputs.scan_memory_url)
                data_iterator = self.iter_bliss_data_from_memory(
                    self.inputs.scan_memory_url,
                    lima_names=[detector_name],
                    counter_names=counter_names,
                )
            else:
                logger.info(
                    "PyFAI integrate data from '%s::%d.%s'",
                    self.inputs.filename,
                    self.inputs.scan,
                    subscan,
                )
                data_iterator = self.iter_bliss_data(
                    self.inputs.filename,
                    self.inputs.scan,
                    lima_names=[detector_name],
                    counter_names=counter_names,
                    subscan=subscan,
                )

            for ptdata in data_iterator:
                normalization_factor, *_ = self._pyfai_normalization_factor(
                    ptdata.get(monitor_name), ptdata.get(reference_name, reference)
                )
                image = ptdata[detector_name]
                if self.inputs.demo:
                    image = image[:-1, :-1]
                result = worker.process(
                    image, normalization_factor=normalization_factor
                )

                intensities.append(result.intensity)
                sigmas.append(integrate_utils.get_yerror(result))
                if radial is None:
                    radial = result.radial
                if unit is None:
                    unit = result.unit.name
                if worker.do_2D() and azimuthal is None:
                    azimuthal = result.azimuthal

            info = pyfai_utils.compile_integration_info(config, reference=reference)

            self.outputs.radial = radial
            self.outputs.azimuthal = azimuthal
            self.outputs.intensity = numpy.array(intensities)
            self.outputs.intensity_error = numpy.array(sigmas)
            self.outputs.radial_units = unit
            self.outputs.info = info
