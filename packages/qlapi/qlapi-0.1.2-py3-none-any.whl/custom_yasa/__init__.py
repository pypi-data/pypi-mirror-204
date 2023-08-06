from yasa import *
import numpy as np
import matplotlib.pyplot as plt
from lspopt import spectrogram_lspopt
from matplotlib.colors import Normalize, ListedColormap
import os.path
from tkinter import filedialog
import tkinter as tk
import datetime as dt
import pytz


def time_freq_analysis(
        data,
        sf,
        hypno=None,
        win_sec=30,
        fmin=0.5,
        fmax=25,
        trimperc=2.5,
        cmap="RdBu_r",
        vmin=None,
        vmax=None,
        **kwargs
):
    """
    Plot a full-night multi-taper spectrogram, optionally with the hypnogram on top.

    For more details, please refer to the `Jupyter notebook
    <https://github.com/raphaelvallat/yasa/blob/master/notebooks/10_spectrogram.ipynb>`_

    .. versionadded:: 0.1.8

    Parameters
    ----------
    data : :py:class:`numpy.ndarray`
        Single-channel EEG data. Must be a 1D NumPy array.
    sf : float
        The sampling frequency of data AND the hypnogram.
    hypno : array_like
        Sleep stage (hypnogram), optional.

        The hypnogram must have the exact same number of samples as ``data``.
        To upsample your hypnogram, please refer to :py:func:`yasa.hypno_upsample_to_data`.

        .. note::
            The default hypnogram format in YASA is a 1D integer
            vector where:

            - -2 = Unscored
            - -1 = Artefact / Movement
            - 0 = Wake
            - 1 = N1 sleep
            - 2 = N2 sleep
            - 3 = N3 sleep
            - 4 = REM sleep
    win_sec : int or float
        The length of the sliding window, in seconds, used for multitaper PSD
        calculation. Default is 30 seconds. Note that ``data`` must be at least
        twice longer than ``win_sec`` (e.g. 60 seconds).
    fmin, fmax : int or float
        The lower and upper frequency of the spectrogram. Default 0.5 to 25 Hz.
    trimperc : int or float
        The amount of data to trim on both ends of the distribution when
        normalizing the colormap. This parameter directly impacts the
        contrast of the spectrogram plot (higher values = higher contrast).
        Default is 2.5, meaning that the min and max of the colormap
        are defined as the 2.5 and 97.5 percentiles of the spectrogram.
    cmap : str
        Colormap. Default to 'RdBu_r'.
    vmin : int or float
        The lower range of color scale. Overwrites ``trimperc``
    vmax : int or float
        The upper range of color scale. Overwrites ``trimperc``
    **kwargs : dict
        Other arguments that are passed to :py:func:`yasa.plot_hypnogram`.

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        Matplotlib Figure

    """
    # Increase font size while preserving original
    old_fontsize = plt.rcParams["font.size"]
    plt.rcParams.update({"font.size": 18})

    # Safety checks
    assert isinstance(data, np.ndarray), "Data must be a 1D NumPy array."
    assert isinstance(sf, (int, float)), "sf must be int or float."
    assert data.ndim == 1, "Data must be a 1D (single-channel) NumPy array."
    assert isinstance(win_sec, (int, float)), "win_sec must be int or float."
    assert isinstance(fmin, (int, float)), "fmin must be int or float."
    assert isinstance(fmax, (int, float)), "fmax must be int or float."
    assert fmin < fmax, "fmin must be strictly inferior to fmax."
    assert fmax < sf / 2, "fmax must be less than Nyquist (sf / 2)."
    assert isinstance(vmin, (int, float, type(None))), "vmin must be int, float, or None."
    assert isinstance(vmax, (int, float, type(None))), "vmax must be int, float, or None."
    if vmin is not None:
        assert isinstance(vmax, (int, float)), "vmax must be int or float if vmin is provided"
    if vmax is not None:
        assert isinstance(vmin, (int, float)), "vmin must be int or float if vmax is provided"
    if hypno is not None:
        # Validate and handle hypnogram-related inputs
        assert hypno.size == data.size, "Hypno must have the same sf as data."

    # Calculate multi-taper spectrogram
    nperseg = int(win_sec * sf)
    assert data.size > 2 * nperseg, "Data length must be at least 2 * win_sec."
    f, t, Sxx = spectrogram_lspopt(data, sf, nperseg=nperseg, noverlap=nperseg / 2)
    Sxx = 10 * np.log10(Sxx)  # Convert uV^2 / Hz --> dB / Hz

    # Select only relevant frequencies (up to 30 Hz)
    good_freqs = np.logical_and(f >= fmin, f <= fmax)
    Sxx = Sxx[good_freqs, :]
    f = f[good_freqs]
    t /= 3600  # Convert t to hours
    return Sxx, t, f


"""
    # Normalization
    if vmin is None:
        vmin, vmax = np.nanpercentile(Sxx, [0 + trimperc, 100 - trimperc])
    norm = Normalize(vmin=vmin, vmax=vmax)

    # Open figure
    if hypno is None:
        fig, ax1 = plt.subplots(nrows=1, figsize=(12, 4))
    else:
        fig, (ax0, ax1) = plt.subplots(
            nrows=2,
            figsize=(12, 6),
            gridspec_kw={"height_ratios": [1, 2], "hspace": 0.1},
        )

    # Draw Spectrogram
    im = ax1.pcolormesh(t, f, Sxx, norm=norm, cmap=cmap, antialiased=True, shading="auto")
    ax1.set_xlim(0, t.max())
    ax1.set_ylabel("Frequency [Hz]")
    ax1.set_xlabel("Time [hrs]")

    if hypno is not None:
        hypnoplot_kwargs = dict(lw=1.5, fill_color=None)
        hypnoplot_kwargs.update(kwargs)
        # Draw hypnogram
        ax0 = plot_hypnogram(hypno, sf_hypno=sf, ax=ax0, **hypnoplot_kwargs)
        ax0.xaxis.set_visible(False)
    else:
        # Add colorbar
        cbar = fig.colorbar(im, ax=ax1, shrink=0.95, fraction=0.1, aspect=25)
        cbar.ax.set_ylabel("Log Power (dB / Hz)", rotation=270, labelpad=20)

    # Revert font-size
    plt.rcParams.update({"font.size": old_fontsize})
    return Sxx, t, f
"""


def get_data_within(start_time, end_time, channel=None, sf=None, resampling=False, reref=True, path=None):
    if not path:
        root = tk.Tk()
        root.withdraw()
        path = tk.filedialog.askdirectory()

    file_list = glob.glob(os.path.join(path, "*.edf"))

    def is_first_file(file_name):
        file_name = os.path.split(file_name)[-1]
        file_name = os.path.splitext(file_name)[0]
        return file_name.split('_')[-1] == '1'

    idx_start = 0
    idx_end = 0
    for idx_file, file in enumerate(file_list):
        file_name = os.path.split(file)[-1]
        file_name_time = file_name.split('_')[0]

        file_dt = dt.datetime.strptime(file_name_time, "%Y%m%d%H%M%S").replace(tzinfo=pytz.UTC)
        if (file_dt <= start_time) & is_first_file(file):
            idx_start = idx_file
        if file_dt <= end_time:
            idx_end = idx_file

    file_list = file_list[idx_start:idx_end + 1]

    if not file_list:
        raise Exception('No data in selected duration! ')

    raw_list = []
    for file in file_list:
        raw = mne.io.read_raw_edf(file, preload=False, verbose=False)
        start_time_file = raw.annotations.orig_time
        end_time_file = start_time_file + dt.timedelta(seconds=raw.times[-1])
        if end_time_file < start_time:
            continue
        elif start_time_file > end_time:
            break
        else:
            raw.is_first_file = is_first_file(file)
            raw_list.append(raw)

    if not raw_list:
        raise Exception('No data in selected duration! ')

    if sf is None:
        sf = min(raw.info['sfreq'] for raw in raw_list)

    if resampling:
        for idx_raw, raw in enumerate(raw_list):
            if not raw.info['sfreq'] == sf:
                is_first_file = raw.is_first_file
                raw_list[idx_raw] = raw.copy().resample(sf)
                raw_list[idx_raw].is_first_file = is_first_file
    else:
        raw_list = [raw for raw in raw_list if raw.info['sfreq'] == sf]

    if not channel:
        print(channel)
        channel = range(min(len(raw.ch_names) for raw in raw_list) - 1)

    data = np.empty((len(channel), int(sf * (end_time - start_time).total_seconds()) + 1))
    data[:] = np.nan
    for raw in raw_list:

        if all(isinstance(item, str) for item in channel):
            idx_chan = [raw.ch_names.index(item) for item in channel]
        elif all(isinstance(item, int) for item in channel):
            idx_chan = list(channel)
            ch_names = [raw.ch_names[i] for i in idx_chan]

        if raw.is_first_file or ('idx_whole_start' not in locals()):
            start_time_file = raw.annotations.orig_time
            idx_whole_start = int((start_time_file - start_time).total_seconds() * sf)
        else:
            idx_whole_start += data_len

        data_len = raw.n_times
        if idx_whole_start + data_len < 0:
            continue
        flag_overlap = (0 <= np.arange(idx_whole_start, idx_whole_start + data_len, 1)) \
                       & (np.arange(idx_whole_start, idx_whole_start + data_len, 1) < data.shape[1])

        data[:, max(0, idx_whole_start):min(idx_whole_start + data_len, data.shape[1])] = \
            mne.io.read_raw_edf(raw.filenames[0], verbose=False).get_data()[idx_chan][:, flag_overlap]

    info = mne.create_info(ch_names=ch_names, sfreq=sf, ch_types='eeg', verbose=False)
    raw = mne.io.RawArray(data, info, verbose=False)
    if reref:
        raw.set_eeg_reference(ref_channels='average')
    return raw, path
