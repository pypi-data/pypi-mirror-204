import importlib.metadata

__version__ = importlib.metadata.version("napari-cilia-beating-frequency")

import collections
import csv
import enum
import pathlib
from typing import TYPE_CHECKING, List, Optional

import magicgui
import numpy
import scipy.ndimage
import scipy.signal
import skimage.measure

if TYPE_CHECKING:
    import napari.viewer
    import napari.layers
    import napari.types


class DownsampleFunc(enum.Enum):
    mean = numpy.mean
    max = numpy.max


class PsdFunc(enum.Enum):
    sqrt = numpy.sqrt
    cbrt = numpy.cbrt
    log = numpy.log1p


@magicgui.magic_factory(
    layer=dict(label="Source Image:"),
    downsample=dict(label="Downsample N Times:", min=0),
    downsample_func=dict(label="Downsample Function:"),
    beating_min=dict(label="Minimum Beating Frequency [Hz]:", min=0.0),
    beating_max=dict(label="Maximum Beating Frequency [Hz]:", min=0.0),
    sampling_freq=dict(label="Sampling Frequency [Hz]:", min=0.0),
    threshold_factor=dict(label="Threshold for Highest-powered Pixels", min=1.0),
    psd_func=dict(label="Spectrum Preprocessing Function:"),
    output_csv_path=dict(label="Frequencies Output CSV Path:"),
)
def widget(
    layer: "napari.layers.Image",
    *,
    downsample: int = 0,
    downsample_func: Optional[DownsampleFunc] = None,
    beating_min: float = 2.0,
    beating_max: float = 20.0,
    sampling_freq: float = 249.0,
    threshold_factor: float = 1.5,
    psd_func: Optional[PsdFunc] = None,
    output_csv_path: pathlib.Path = pathlib.Path("frequencies.csv"),
) -> List["napari.types.LayerDataTuple"]:
    if layer is None:
        return None

    name = layer.name
    data = layer.data

    if downsample and downsample_func:
        data = skimage.measure.block_reduce(
            data, block_size=downsample, func=downsample_func.value
        )

    # Get power spectral density for each pixel.
    sample_freqs, psd = scipy.signal.periodogram(data, fs=sampling_freq, axis=0)
    if psd_func:
        psd = psd_func.value(psd)

    # Pixel has valid frequency if it's frequency carrying the most power lies
    # in an acceptable frequency range.
    max_pow_freqs = sample_freqs[numpy.argmax(psd, axis=0)]
    valid_freq_mask = (beating_min <= max_pow_freqs) & (max_pow_freqs <= beating_max)

    # Pixel has a high signal if it's max(P) >= median(P) + N * mad(P).
    # MAD: Median Absolute Deviation.
    psd_max = numpy.max(psd, axis=0)
    psd_median = numpy.median(psd, axis=0)
    psd_mad = numpy.median(numpy.abs(psd - psd_median), axis=0)
    high_signal_mask = psd_max >= (psd_median + threshold_factor * psd_mad)

    active_mask = valid_freq_mask & high_signal_mask
    active_freqs = numpy.round(max_pow_freqs[active_mask], decimals=6)
    freq_counts = collections.Counter(active_freqs)

    with open(output_csv_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(("frequency", "count"))
        csv_writer.writerows(freq_counts.most_common())

    return [
        (psd_max, dict(name=f"{name} / PSD / Maximum")),
        (psd_median, dict(name=f"{name} / PSD / Median")),
        (max_pow_freqs, dict(name=f"{name} / PSD / Dominant Frequency Map")),
        (active_mask, dict(name=f"{name} / PSD / Mask"), "labels"),
    ]
