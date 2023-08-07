import numpy
import h5py
import pytest
from ewoksorange.tests.utils import execute_task

from orangecontrib.ewoksxrpd.batchintegrate import OWIntegrateBlissScan


@pytest.mark.parametrize("ndims", [1, 2])
def test_batch_integrate_task(ndims, bliss_task_inputs, tmpdir):
    assert_batch_integrate(ndims, bliss_task_inputs, tmpdir)


@pytest.mark.parametrize("ndims", [1, 2])
def test_batch_integrate_widget(ndims, bliss_task_inputs, tmpdir, qtapp):
    assert_batch_integrate(ndims, bliss_task_inputs, tmpdir, qtapp=qtapp)


def assert_batch_integrate(ndims, bliss_task_inputs, tmpdir, qtapp=None):
    output_filename = str(tmpdir / "result.h5")
    inputs = {**bliss_task_inputs, "output_filename": output_filename}

    if ndims == 2:
        inputs["integration_options"] = {
            "method": "no_csr_cython",
            "integrator_name": "integrate2d_ng",
            "nbpt_azim": 100,
            "error_model": "poisson",
        }
    else:
        inputs["integration_options"] = {
            "error_model": "azimuthal",
            "method": "no_csr_cython",
            "integrator_name": "sigma_clip_ng",
            "extra_options": {"max_iter": 3, "thres": 0},
        }

    execute_task(
        OWIntegrateBlissScan.ewokstaskclass if qtapp is None else OWIntegrateBlissScan,
        inputs=inputs,
    )

    with h5py.File(output_filename) as root:
        data = root["2.1/measurement/p3_integrated"][()]
        if ndims == 2:
            axes = ["points", "azimuth", "2th"]
        else:
            axes = ["points", "2th"]
        assert root["2.1/p3_integrate/integrated"].attrs["axes"].tolist() == axes
        spectrum0 = data[0]
        for spectrum in data:
            numpy.testing.assert_allclose(spectrum, spectrum0, atol=1)

        # Check links to raw data
        root["2.1/measurement/monitor"][()]
        list(root["2.1/instrument"].keys())
