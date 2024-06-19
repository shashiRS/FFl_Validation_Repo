"""Confusion matrix expected result example."""
import datetime
import logging
import os
import tempfile
from pathlib import Path

import numpy as np
from tsf.core.common import (
    AggregateFunction,
    ConfusionMatrixRate,
    RelationOperator,
    TimeBase,
)
from tsf.core.results import (
    ConfusionMatrixResult,
    ExpectedConfusionMatrixResult,
    ExpectedResult,
    Result,
)
from tsf.core.testcase import (
    ConfusionMatrixTestStep,
    TestCase,
    TestStep,
    register_generic_collection,
    register_signals,
    testcase_definition,
    teststep_confusion_matrix_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.db.events import Event
from tsf.io.bsig import BsigWriter
from tsf.io.signals import SignalDefinition, SignalReader

_log = logging.getLogger(__name__)

np.random.seed(27)

EXAMPLE = "example"


class ExampleSignals(SignalDefinition):
    """Signal mapping for EBA."""

    class Columns(SignalDefinition.Columns):
        """Definition of the dataframe columns."""

        ACTIVATION_A = "some_activation_a"
        ACTIVATION_B = "some_activation_b"
        EGO_VELO = "ego_velo"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.ACTIVATION_A: "Example Signal Data.activation.sig_a",
            self.Columns.ACTIVATION_B: "Example Signal Data.activation.sig_b",
            self.Columns.EGO_VELO: "Example Signal Data.ego.velocity.x",
        }


class KpiEvent(Event):
    """KPI event."""

    pass


@teststep_definition(
    1,
    "Count activations of signal A",
    "Example for counting an activation rate. Over more than a single input.",
    ExpectedResult(
        20,
        100,
        unit="1/km",
        numerator_is_events=True,
        operator=RelationOperator.LESS_OR_EQUAL,
        aggregate_function=AggregateFunction.KPI,
    ),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleAEBTestStep1(TestStep):
    """Example test step."""

    def process(self, **kwargs):
        """Count the activations (raising flanks on the mileag (integral of the velocity over time)."""
        # Get the read data frame
        exmpl = self.readers[EXAMPLE]

        # check for raising flanks
        flanks = exmpl[ExampleSignals.Columns.ACTIVATION_A].diff() > 0

        activations = exmpl.loc[flanks]
        all_activations_in_input = len(activations)

        for ts, row in activations.iterrows():
            e = KpiEvent(start_timestamp=ts, end_timestamp=ts, timebase=TimeBase.MTS_PACKAGE_TIMESTAMP)
            self.result.add_event(e, {"all_activations": all_activations_in_input})

        td = exmpl[ExampleSignals.Columns.TS].diff() * 1e-6
        mileage = np.sum(exmpl[ExampleSignals.Columns.EGO_VELO] * td) / 1000

        # Store the result
        self.result.measured_result = Result(None, mileage, unit="1/km")


@teststep_definition(
    2,
    "Count activations of signal B",
    "Example for counting an activation rate. Over more than a single input.",
    ExpectedResult(50, 1000, unit="1/km", operator=RelationOperator.GREATER, aggregate_function=AggregateFunction.KPI),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleAEBTestStep2(TestStep):
    """Example test step."""

    def process(self, **kwargs):
        """Count the activations (raising flanks on the mileag (integral of the velocity over time)."""
        # Get the read data frame
        exmpl = self.readers[EXAMPLE]

        # check for raising flanks
        flanks = exmpl[ExampleSignals.Columns.ACTIVATION_B].diff() > 0

        activations = exmpl.loc[flanks]

        td = exmpl[ExampleSignals.Columns.TS].diff() * 1e-6
        mileage = np.sum(exmpl[ExampleSignals.Columns.EGO_VELO] * td) / 1000

        # Store the result
        self.result.measured_result = Result(len(activations), mileage, unit="1/km")


class ConfusionMatrixEvent(Event):
    """Confusion matrix event."""

    pass


@teststep_confusion_matrix_definition(
    step_number=1,
    name="Confusion Matrix Detector",
    description="TPR = TP / (TP + FN)",
    expected_result=ExpectedConfusionMatrixResult(
        rate=ConfusionMatrixRate.TPR,
        value=0.8,
        operator=RelationOperator.GREATER_OR_EQUAL,
        # project_name="test"
    ),
)
@register_signals(EXAMPLE, ExampleSignals)
class ConfusionMatrixTs(ConfusionMatrixTestStep):
    """Example with events."""

    def process(self):
        """Perform the evaluation and generates events and a result."""
        exmpl = self.readers[EXAMPLE]

        # check for raising flanks
        flanks = exmpl[ExampleSignals.Columns.ACTIVATION_A].diff() > 0
        tp = exmpl.loc[flanks]
        all_tps = len(tp)

        flanks = exmpl[ExampleSignals.Columns.ACTIVATION_B].diff() > 0
        fp = exmpl.loc[flanks]
        all_fps = len(fp)

        for ts, row in tp.iterrows():
            e = ConfusionMatrixEvent(start_timestamp=ts, end_timestamp=ts, timebase=TimeBase.MTS_PACKAGE_TIMESTAMP)
            self.result.add_event(e, {"all_tps": all_tps, "all_fps": all_fps})

        self.result.measured_result = ConfusionMatrixResult(
            true_positive=all_tps, false_positive=all_fps, false_negative=2
        )


@teststep_confusion_matrix_definition(
    step_number=2,
    name="Confusion Matrix Detector 2",
    description="Accuracy = (TP + TN) / (TP + TN + FP + FN)",
    expected_result=ExpectedConfusionMatrixResult(
        rate=ConfusionMatrixRate.ACCURACY,
        value=0.8,
        operator=RelationOperator.GREATER_OR_EQUAL,
    ),
)
@register_signals(EXAMPLE, ExampleSignals)
class ConfusionMatrixTs2(ConfusionMatrixTestStep):
    """Example without events."""

    def process(self):
        """Perform the evaluation and generates events and a result."""
        super().process()
        self.result.measured_result = ConfusionMatrixResult(true_positive=3, false_positive=4, false_negative=2)


@verifies("dummy-req")
@testcase_definition(
    name="Confusion Matrix Testcase",
    description="Demo implementation",
)
@register_generic_collection("BCR_100_BASE_COLLECTION")
class ConfusionMatrixTc(TestCase):
    """Example with confusion matrix results."""

    @property
    def test_steps(self):
        return [ConfusionMatrixTs, ConfusionMatrixTs2]


@verifies("dummy-req2")
@testcase_definition(
    name="Kpi Testcase",
    description="Demo implementation",
)
@register_generic_collection("BCR_100_BASE_COLLECTION")
class KpiTc(TestCase):
    """Example KPI TC with 2 steps with normal KPI results."""

    @property
    def test_steps(self):
        return [ExampleAEBTestStep1, ExampleAEBTestStep2]


def main(temp_dir: Path = tempfile.mkdtemp(), open_explorer=True):
    # Entry point for debugging during development.
    exp_sd = ExampleSignals()
    data_folder = os.path.join(temp_dir, "data")
    os.makedirs(data_folder, exist_ok=True)

    for k in range(5):
        _log.debug(f"Producing bisg {k}.")

        bsig_1 = os.path.join(data_folder, f"test_input_{k:02d}.bsig")
        with BsigWriter(bsig_1) as wrt:
            # timestamps are in microseconds (us) sampling as unit64 data type.
            f = 60e3  # ms
            N = np.random.randint(2000, 8000)
            jitter_max = 3e3  # ms

            # unix timestamp in us
            ts_0 = int(datetime.datetime.utcnow().timestamp() * 1e6)
            ts = np.cumsum(np.ones(N) * f + np.random.randint(0, int(jitter_max), N))
            ts += ts_0
            ts = ts.astype(np.uint64)

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

            ego_vx = np.ones(N) * 30 / 3.6 + (np.random.random(N) - 0.5) * 0.2

            wrt[SignalReader.MTS_TS_SIGNAL] = ts
            wrt[exp_sd.signal_properties[ExampleSignals.Columns.ACTIVATION_A].signals[0]] = sig_a
            wrt[exp_sd.signal_properties[ExampleSignals.Columns.ACTIVATION_B].signals[0]] = sig_b
            wrt[exp_sd.signal_properties[ExampleSignals.Columns.EGO_VELO].signals[0]] = ego_vx

    sample_inputs = (os.path.join(temp_dir, "data", f"test_input_{k:02d}.bsig") for k in range(5))

    debug(
        [KpiTc, ConfusionMatrixTc],
        *sample_inputs,
        temp_dir=os.path.join(temp_dir, "out"),
        open_explorer=open_explorer,
        clean_dir=True,
        kpi_report=False,
        dev_report=True,
    )


if __name__ == "__main__":
    main()