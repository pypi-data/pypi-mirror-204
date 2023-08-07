import time
import h5py
import numpy
import pytest
from ..data.hdf5.dataset_writer import DatasetWriter


@pytest.mark.parametrize("npoints", (1, 3, 1000))
@pytest.mark.parametrize("flush_period", (None, 0.1))
def test_dataset_writer_variable_points(tmpdir, npoints, flush_period):
    expected = list()
    filename = str(tmpdir / "test.h5")
    if flush_period is None:
        sleep_time = None
    else:
        sleep_time = flush_period + 0.1
    isleep = npoints // 3

    with h5py.File(filename, mode="w") as f:
        with DatasetWriter(f, "data", flush_period=flush_period) as writer:
            for i in range(npoints):
                data = numpy.random.random((10, 20))
                writer.add_point(data)
                expected.append(data)
                if sleep_time and i == isleep:
                    time.sleep(sleep_time)
    with h5py.File(filename, mode="r") as f:
        data = f["data"][()]
    numpy.testing.assert_allclose(data, expected)


@pytest.mark.parametrize("npoints", (1, 3, 1000))
@pytest.mark.parametrize("flush_period", (None, 0.1))
def test_dataset_writer_fixed_points(tmpdir, npoints, flush_period):
    expected = list()
    filename = str(tmpdir / "test.h5")
    if flush_period is None:
        sleep_time = None
    else:
        sleep_time = flush_period + 0.1
    isleep = npoints // 3

    with h5py.File(filename, mode="w") as f:
        with DatasetWriter(
            f, "data", flush_period=flush_period, npoints=npoints
        ) as writer:
            for i in range(npoints):
                data = numpy.random.random((10, 20))
                writer.add_point(data)
                expected.append(data)
                if sleep_time and i == isleep:
                    time.sleep(sleep_time)
    with h5py.File(filename, mode="r") as f:
        data = f["data"][()]
    numpy.testing.assert_allclose(data, expected)
