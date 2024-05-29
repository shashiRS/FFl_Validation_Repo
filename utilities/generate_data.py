"""Needed methods to drive the examples."""
import datetime
import logging
import os
import random
import string
from pathlib import Path
from typing import Callable, List, Optional

import numpy as np
import scipy.signal
from tsf.core._internals.debugging_support import Bootstrap
from tsf.db.connect import DatabaseConnector, ScopedConnectionProvider
from tsf.io.bsig import BsigWriter
from tsf.io.signals import SignalReader

from utilities.signal_definitions import ExampleSignals, ExampleSignals2

_log = logging.getLogger(__name__)
np.random.seed(27)
random.seed(27)


def _make_activation_signal(N: int, min_activations=1, max_activations=10, min_peak_length=2, max_peak_length=7):
    """Generate a signal.

    :param N: signal length
    :param min_activations:
    :param max_activations:
    :param min_peak_length:
    :param max_peak_length:
    :return:
    """
    signal = np.zeros(N)
    number_of_activations = np.random.randint(min_activations, max_activations)
    positions = np.random.choice(np.arange(N), number_of_activations)
    for p in positions:
        peak_l = np.random.randint(min_peak_length, max_peak_length)
        signal[p : p + peak_l] = 1

    return signal


def _make_binary_signal(N: int, success_rate=0.98):
    """Generate a signal of an approach like activation."""
    binary_activation = np.zeros(N)
    if random.random() > (1 - success_rate):
        binary_activation[N - 1000 : N - 900] = 1

    return binary_activation


def generate_bsig(bsig: Path, bsig_other: Path = None, splits=None):
    """Generate a BSIG for the example signal definition."""
    # timestamps are in microseconds (us) sampling as unit64 data type.
    if bsig:
        bsig = Path(bsig)
    if bsig_other:
        bsig_other = Path(bsig_other)

    f = 60e3  # ms
    if splits:
        N = max([max(t) for t in splits]) + 1
    else:
        N = np.random.randint(3000, 8000)
        splits = [(0, N)]
    jitter_max = 3e3  # ms

    # unix timestamp in us
    ts_0 = int(datetime.datetime.utcnow().timestamp() * 1e6)
    ts = np.cumsum(np.ones(N) * f + np.random.randint(0, int(jitter_max), N))
    ts += ts_0
    ts = ts.astype(np.uint64)

    sig_a = _make_activation_signal(N)
    sig_b = _make_activation_signal(N)
    sig_c = _make_activation_signal(N)
    sig_d = _make_activation_signal(N)

    binary_activation_a = _make_binary_signal(N)
    binary_activation_b = _make_binary_signal(N, 0.99)
    binary_activation_c = _make_binary_signal(N, 0.50)
    binary_activation_d = _make_binary_signal(N, 0.12)

    # Construct a fake ego velocity
    ego_vx = (np.random.random(N) - 0.5) * 0.2
    ego_vx[0] = 0.01
    corners = random.sample(range(1000, N - 1000), 2)
    u = np.zeros(N)
    c0 = min(corners)
    c1 = max(corners) + 2
    # Ramp to 30 km/h
    u[0:c0] = np.arange(c0) * 30 / (3.6 * c0)
    # constant 30 km/h
    u[c0:c1] = np.ones(c1 - c0) * 30 / 3.6
    # ramp down to 0
    u[c1:N] = 30 / 3.6 - np.arange(N - c1) * 30 / (3.6 * (N - c1))
    # mix with ego vx
    ego_vx = ego_vx + u
    ego_vx = scipy.signal.medfilt(ego_vx, 15)

    for st_idx, et_idx in splits:
        if len(splits) == 1:
            bsig_path = bsig
            bsig_other_path = bsig_other
        else:
            st = ts[st_idx]
            et = ts[et_idx]
            bsig_path = bsig.parent / f"{bsig.name}_{st}-{et}{bsig.suffix}"

            if bsig_other:
                bsig_other_path = bsig_other.parent / f"{bsig_other.name}_{st}-{et}{bsig_other.suffix}"

        exp_sd = ExampleSignals()
        os.makedirs(bsig_path.parent, exist_ok=True)
        with BsigWriter(bsig_path) as wrt:
            wrt[SignalReader.MTS_TS_SIGNAL] = ts[st_idx:et_idx]
            wrt[exp_sd.signal_properties[ExampleSignals.Columns.ACTIVATION_A].signals[0]] = sig_a[st_idx:et_idx]
            wrt[exp_sd.signal_properties[ExampleSignals.Columns.ACTIVATION_B].signals[0]] = sig_b[st_idx:et_idx]
            wrt[exp_sd.signal_properties[ExampleSignals.Columns.BINARY_ACTIVATION_A].signals[0]] = binary_activation_a[
                st_idx:et_idx
            ]
            wrt[exp_sd.signal_properties[ExampleSignals.Columns.BINARY_ACTIVATION_B].signals[0]] = binary_activation_b[
                st_idx:et_idx
            ]
            wrt[exp_sd.signal_properties[ExampleSignals.Columns.EGO_VELO].signals[0]] = ego_vx[st_idx:et_idx]

        if bsig_other:
            exp_sd2 = ExampleSignals2()
            os.makedirs(bsig_other_path.parent, exist_ok=True)
            with BsigWriter(bsig_other_path) as wrt:
                wrt[SignalReader.MTS_TS_SIGNAL] = ts[st_idx:et_idx]
                wrt[exp_sd2.signal_properties[ExampleSignals2.Columns.ACTIVATION_C].signals[0]] = sig_c[st_idx:et_idx]
                wrt[exp_sd2.signal_properties[ExampleSignals2.Columns.ACTIVATION_D].signals[0]] = sig_d[st_idx:et_idx]
                wrt[
                    exp_sd2.signal_properties[ExampleSignals2.Columns.BINARY_ACTIVATION_C].signals[0]
                ] = binary_activation_c[st_idx:et_idx]
                wrt[
                    exp_sd2.signal_properties[ExampleSignals2.Columns.BINARY_ACTIVATION_D].signals[0]
                ] = binary_activation_d[st_idx:et_idx]


def generate_bsig_multiple(base_dir: Path, name: str):
    """Generate a BSIG for the example signal definition."""
    exp_sd = ExampleSignals()
    exp_sd2 = ExampleSignals2()

    f = 60e3  # ms
    N = np.random.randint(3000, 8000)
    jitter_max = 3e3  # ms

    # unix timestamp in us
    ts_0 = int(datetime.datetime.utcnow().timestamp() * 1e6)
    ts = np.cumsum(np.ones(N) * f + np.random.randint(0, int(jitter_max), N))
    ts += ts_0
    ts = ts.astype(np.uint64)

    os.makedirs(base_dir / "bin_data_1", exist_ok=True)
    with BsigWriter(base_dir / "bin_data_1" / name) as wrt:
        # timestamps are in microseconds (us) sampling as unit64 data type.
        sig_a = np.zeros(N)
        samples_a = np.random.randint(1, 10)
        positions = np.random.choice(np.arange(N), samples_a)
        for position in positions:
            sample = np.random.randint(2, 7)
            sig_a[position : position + sample] = 1

        sig_b = np.zeros(N)
        samples_b = np.random.randint(1, 10)
        positions = np.random.choice(np.arange(N), samples_b)
        for position in positions:
            sample = np.random.randint(2, 7)
            sig_b[position : position + sample] = 1

        sig_d = np.zeros(N)
        samples_d = np.random.randint(1, 10)
        positions = np.random.choice(np.arange(N), samples_d)
        for position in positions:
            sample = np.random.randint(2, 7)
            sig_d[position : position + sample] = 1

        # 90% Chance of passing
        binary_activation_a = np.zeros(N)
        if random.random() > 0.02:
            binary_activation_a[N - 1000 : N - 900] = 1

        binary_activation_b = np.zeros(N)
        if random.random() > 0.1:
            binary_activation_b[N - 1000 : N - 900] = 1

        ego_vx = (np.random.random(N) - 0.5) * 0.2
        ego_vx[0] = 0.01
        corners = random.sample(range(1000, N - 1000), 2)
        u = np.zeros(N)
        c0 = min(corners)
        c1 = max(corners) + 2
        # Ramp to 30 km/h
        u[0:c0] = np.arange(c0) * 30 / (3.6 * c0)
        # constant 30 km/h
        u[c0:c1] = np.ones(c1 - c0) * 30 / 3.6
        # ramp down to 0
        u[c1:N] = 30 / 3.6 - np.arange(N - c1) * 30 / (3.6 * (N - c1))
        # mix with ego vx
        ego_vx = ego_vx + u
        ego_vx = scipy.signal.medfilt(ego_vx, 15)

        wrt[SignalReader.MTS_TS_SIGNAL] = ts
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.ACTIVATION_A].signals[0]] = sig_a
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.ACTIVATION_B].signals[0]] = sig_b
        wrt[exp_sd2.signal_properties[ExampleSignals2.Columns.ACTIVATION_D].signals[0]] = sig_d
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.BINARY_ACTIVATION_A].signals[0]] = binary_activation_a
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.BINARY_ACTIVATION_B].signals[0]] = binary_activation_b
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.EGO_VELO].signals[0]] = ego_vx

    os.makedirs(base_dir / "bin_data_2", exist_ok=True)
    with BsigWriter(base_dir / "bin_data_2" / name) as wrt:
        # timestamps are in microseconds (us) sampling as unit64 data type.
        sig_c = np.zeros(N)
        samples_c = np.random.randint(1, 10)
        positions = np.random.choice(np.arange(N), samples_c)
        for position in positions:
            sample = np.random.randint(2, 7)
            sig_c[position : position + sample] = 1

        # 90% Chance of passing
        binary_activation_c = np.zeros(N)
        if random.random() > 0.02:
            binary_activation_c[N - 1000 : N - 900] = 1

        wrt[SignalReader.MTS_TS_SIGNAL] = ts
        wrt[exp_sd2.signal_properties[ExampleSignals2.Columns.ACTIVATION_C].signals[0]] = sig_c
        wrt[exp_sd2.signal_properties[ExampleSignals2.Columns.BINARY_ACTIVATION_C].signals[0]] = binary_activation_c


def generate_testrun_data(
    data_folder: Path,
    processing_inputs: List[str],
    cp: ScopedConnectionProvider,
    side_load_callback: Callable = None,
    prefix="",
    suffix="",
    break_after: Optional[int] = None,
    create_orphans=False,
):
    """Generate BSIGs for the given processing input sets."""
    with DatabaseConnector(cp) as dbc:
        input_entry_names = []

        for ips_url in processing_inputs:
            ips = dbc.processing_inputs.get_input_set(url=ips_url)
            input_entry_names.extend([e.stem for e in ips.entries])

    if break_after:
        k = break_after
    else:
        k = -1
    for pie in input_entry_names[:k]:
        _log.debug(f"Producing bsig for input {pie}.")

        bsig = data_folder / f"{prefix}{pie}{suffix}.bsig"
        generate_bsig(bsig)
        if side_load_callback:
            side_load_callback(bsig)

    if create_orphans:
        bsigs = [data_folder / f"{prefix}__orphan1__{suffix}.bsig", data_folder / f"{prefix}__orphan2__{suffix}.bsig"]
        for bsig in bsigs:
            generate_bsig(bsig)
            if side_load_callback:
                side_load_callback(bsig)


def create_local_db(output_folder, projects: List[str], data_folder: Path):
    sqlite_path = output_folder / "tsf.sqlite"
    Bootstrap.debugging_sqlite_db(sqlite_path, sync_globals=False)

    cp = ScopedConnectionProvider(sqlite=sqlite_path)
    with DatabaseConnector(cp) as dbc:

        for name in projects:
            dbc.global_data.add_project(name, "-", "-")
            dbc.processing_inputs.create_input_set(url=f"/{name}")

        ctr = 1
        for name in projects:
            for j in range(3):
                entries = []
                for k in range(random.randint(15, 25)):
                    rec_dir = "/" + "/".join(["".join(random.choices(string.ascii_uppercase, k=3)) for _ in range(10)])
                    rec_name = f"/test_input_{ctr:04d}.rrec"
                    ctr += 1
                    c_input = dbc.processing_inputs.create_input(rec_dir + rec_name)
                    entries.append(c_input)