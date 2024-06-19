#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example, you can learn how to use confusion matrix as a teststep expected and measured result.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.common import ConfusionMatrixRate, RelationOperator, TimeBase
from tsf.core.results import ConfusionMatrixResult, ExpectedConfusionMatrixResult
from tsf.core.testcase import (
    ConfusionMatrixTestStep,
    TestCase,
    register_signals,
    testcase_definition,
    teststep_confusion_matrix_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.db.events import Event

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)


class ConfusionMatrixEvent(Event):
    """Confusion matrix event."""

    pass


@teststep_confusion_matrix_definition(
    step_number=1,
    name="Confusion Matrix TRUE POSITIVE RATE",
    description="TPR = TP / (TP + FN)",
    ###################################################################
    # Note: Here we set the expected result TPR Confusion Matrix ######
    ###################################################################
    expected_result=ExpectedConfusionMatrixResult(
        rate=ConfusionMatrixRate.TPR,
        value=0.8,
        operator=RelationOperator.GREATER_OR_EQUAL,
    ),
)
@register_signals(EXAMPLE, ExampleSignals)
class ConfusionMatrixTPR(ConfusionMatrixTestStep):
    """Example with events."""

    def process(self):
        """Process data."""
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation_tp = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] == 1)]
        tp = len(example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] == 1)])
        fp = len(example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_B] == 1)])

        for ts, row in activation_tp.iterrows():
            event = ConfusionMatrixEvent(start_timestamp=ts, end_timestamp=ts, timebase=TimeBase.MTS_PACKAGE_TIMESTAMP)
            self.result.add_event(event, {"all_tps": tp, "all_fps": fp})

        tn = 1
        fn = 1

        ###################################################################
        # Note: Here we set the measured result as Confusion matrix #######
        ###################################################################
        self.result.measured_result = ConfusionMatrixResult(
            true_positive=tp, false_positive=fp, false_negative=fn, true_negative=tn
        )


@teststep_confusion_matrix_definition(
    step_number=2,
    name="Confusion Matrix ACCURACY",
    description="Accuracy = (TP + TN) / (TP + TN + FP + FN)",
    ###################################################################
    # Note: Here measured result is set as Confusion Matrix           #
    #       Expected result                                           #
    ###################################################################
    expected_result=ExpectedConfusionMatrixResult(
        rate=ConfusionMatrixRate.ACCURACY,
        value=0.8,
        operator=RelationOperator.GREATER_OR_EQUAL,
    ),
)
@register_signals(EXAMPLE, ExampleSignals)
class ConfusionMatrixACC(ConfusionMatrixTestStep):
    """Example without events."""

    def process(self):
        """Process data."""
        _log.debug("Starting processing...")
        super().process()

        example_signals = self.readers[EXAMPLE].signals

        tp = len(example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] == 1)])
        fp = len(example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_B] == 1)])
        tn = 1
        fn = 1

        ###################################################################
        # Note: Here we set the measured result as Confusion matrix result
        ###################################################################
        self.result.measured_result = ConfusionMatrixResult(
            true_positive=tp, false_positive=fp, false_negative=fn, true_negative=tn
        )


@verifies("req-001")
@testcase_definition(
    spec_tag="Confusion Matrix Detector",  # Spec_tag attribute is deprecated, use instead URI decorator. (examples/docs/howto/uri.html).
    name="Confusion Matrix Testcase",
    description="Demo implementation",
)
class ConfusionMatrixTc(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [ConfusionMatrixTPR, ConfusionMatrixACC]


def main(data_folder: Path, temp_dir: Path = None, open_explorer=True):
    """Call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    test_bsigs = [data_folder / f"test_input_{k}.bsig" for k in range(3)]
    os.makedirs(data_folder, exist_ok=True)
    for b in test_bsigs:
        generate_bsig(b)

    debug(
        ConfusionMatrixTc,
        *test_bsigs,
        temp_dir=temp_dir,
        open_explorer=open_explorer,
        kpi_report=False,
        dev_report=True,
    )
    _log.debug("All done.")


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))

    data_folder = working_directory / "data"
    out_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)
