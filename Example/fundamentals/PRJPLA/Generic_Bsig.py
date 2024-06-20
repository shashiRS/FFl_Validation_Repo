from pathlib import Path
from TRJPLA_constant import ExampleSignals
from tsf.io.bsig import BsigWriter
import datetime
import numpy as np
from tsf.io.signals import SignalDefinition, SignalReader
import random

import scipy
###################################################################
# Note: generate_bsig not relevant for users ######################
###################################################################


def generate_bsig(bsig: Path):
    """Generate a BSIG for the example signal definition."""
    exp_sd = ExampleSignals()
    with BsigWriter(bsig) as wrt:
        # timestamps are in microseconds (us) sampling as unit64 data type.
        f = 60e3  # ms
        N = np.random.randint(3000, 8000)
        jitter_max = 3e3  # ms

        # unix timestamp in us
        ts_0 = int(datetime.datetime.utcnow().timestamp() * 1e6)
        ts = np.cumsum(np.ones(N) * f + np.random.randint(0, int(jitter_max), N))
        ts += ts_0
        ts = ts.astype(np.uint64)
        wrt[SignalReader.MTS_TS_SIGNAL] = ts

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
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.ACTIVATION_D].signals[0]] = sig_d
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.BINARY_ACTIVATION_A].signals[0]] = binary_activation_a
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.BINARY_ACTIVATION_B].signals[0]] = binary_activation_b
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.EGO_VELO].signals[0]] = ego_vx

