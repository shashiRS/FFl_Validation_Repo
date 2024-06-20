#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ECU-SIL Testcase implementation.

One testcase with a single teststep without events, assessments, pre-processors, side-loaders or report customization.
This implementation is part of the integration test suite and must be executable with any new release.
"""
import logging
import os
import shutil
import sys
import tempfile
from pathlib import Path

from tsf.core.common import AggregateFunction, PathSpecification, RelationOperator
from tsf.core.results import ExpectedResult, Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_inputs,
    register_signals,
    tag,
    testcase_definition,
    teststep_definition,
    uri,
)
from tsf.core.utilities import debug
from tsf.io.signals import SignalDefinition

ROOT = str(Path(__file__).resolve().parent.parent)
if ROOT not in sys.path:
    sys.path.append(ROOT)


__author__ = "A AM ENP SIMU KPI"
__copyright__ = "2020-2022, Continental BA ADAS"
__status__ = "Production"

_log = logging.getLogger(__name__)


class ExampleSignals1(SignalDefinition):
    """Example signals."""

    class Columns(SignalDefinition.Columns):
        """Definition of the dataframe columns."""

        EGO_VELO = "ego_velo"
        MOT_STATE = "motion_state"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            # example of providing single signal and down-casting the values
            self.Columns.EGO_VELO: {
                "signal": [
                    "SIM VFB CEM200.AlgoVehCycle.VDY_VehDynMeas.Longitudinal.Velocity",
                    "AURIX.AlgoVehCycle.VDY_VehDynMeas.Longitudinal.Velocity",
                ],
            },
            self.Columns.MOT_STATE: {
                "signal": [
                    "SIM VFB CEM200.AlgoVehCycle.VDY_VehDynMeas.MotionState.MotState",
                    "AURIX.AlgoVehCycle.VDY_VehDynMeas.MotionState.MotState",
                ],
            },
        }


@teststep_definition(
    1,
    "Check ECU and SIL delay",
    "Check delay between ECU and SIL for an specific signal.",
    ExpectedResult(
        0.015,
        unit="s",
        operator=RelationOperator.LESS,
        aggregate_function=AggregateFunction.KPI,
    ),
)
# Defined two register signal decorators, one for ECU and one for SIL, which matches the Tags (ECU, SIL)
# given in the PathSpecification.
@register_signals(alias="example_1_ecu", definition=ExampleSignals1, tag="ECU")
@register_signals(alias="example_1_sil", definition=ExampleSignals1, tag="SIL")
@uri("teststep://examples/fcda7c47-863e-40ee-8a9d-0e7c029950b1")
@tag("teststep", "ECU", "SIL", "Reader")
class ExampleEcuSilReaderTestStep(TestStep):
    """Example ECU-SIL test step."""

    def process(self, **kwargs):
        """Check signal delay between ECU and SIL."""
        # Get the read data frame
        ecu_sigs = self.readers["example_1_sil"]

        sil_sigs = self.readers["example_1_ecu"]

        # check for raising flanks
        flanks_sil = ecu_sigs[ExampleSignals1.Columns.MOT_STATE].diff() > 0
        activations_sil = ecu_sigs.loc[flanks_sil]

        # check for raising flanks
        flanks_ecu = sil_sigs[ExampleSignals1.Columns.MOT_STATE].diff() > 0
        activations_ecu = sil_sigs.loc[flanks_ecu]

        diff = abs(activations_ecu["mts_ts"].iloc[0] - activations_sil["mts_ts"].iloc[0]) * 1e-6
        # Store the result
        self.result.measured_result = Result(diff, unit="s")


@testcase_definition("ECU-SIL Readers", "Example ECU-SIL Readers.")
@uri("testcase://examples/fcda7c46-863d-40ed-8a9c-0e7c029950b0")
@tag("testcase", "ECU", "SIL", "Reader")
@register_inputs("/Project-2/example-2")
class ExampleEcuSilReaderTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleEcuSilReaderTestStep,
        ]


def debug_minimal_example(data_folder: Path, output_folder: Path, open_explorer=True):
    """Read ECU-SIL data and execute the tests."""
    test_bsigs_sil = [data_folder / "SIL" / "2021.08.04_at_10.12.27_radar-mi_103_VDY.bsig"]
    debug(
        [
            ExampleEcuSilReaderTestCase,
        ],
        *test_bsigs_sil,
        input_pathspecs=[
            PathSpecification(data_folder / "ECU", extension=".bsig", tag="ECU"),
            PathSpecification(data_folder / "SIL", extension=".bsig", tag="SIL"),
        ],
        temp_dir=output_folder,
        open_explorer=open_explorer,
        clean_dir=True,
    )


if __name__ == "__main__":
    # Bootstrap, run once
    working_directory = Path(os.environ.get("TSF_TEMP_DIR", default=tempfile.mkdtemp("_tsf"))) / "ecu_sil_example"
    shutil.rmtree(working_directory, ignore_errors=True)

    data_folder = Path(ROOT) / "data" / "ecu-sil"
    output_folder = working_directory / "out"

    debug_minimal_example(data_folder=data_folder, output_folder=output_folder, open_explorer=True)
