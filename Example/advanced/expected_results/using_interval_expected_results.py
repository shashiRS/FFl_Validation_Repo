#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example you can learn how to make expected result of a teststep interval based.
As in if the measured result is between the defined interval then the teststep would be considered PASSED.

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

from tsf.core.common import RelationOperator
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.db.results import ExpectedResult, Result

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@teststep_definition(
    step_number=1,
    name="Expected Result Interval",
    description="Check if the activation is between two numerator values.",
    ###################################################################
    # Note: Here we set the expected result with two numerator values #
    ###################################################################
    expected_result=ExpectedResult(numerator=70, numerator2=90, unit="%", operator=RelationOperator.BETWEEN),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExpectedResultInterval(TestStep):
    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")
            return

        if 1 <= len(activation) < 10:
            self.result.measured_result = Result(50, unit="%")
            return

        self.result.measured_result = Result(100.0, unit="%")


@teststep_definition(
    step_number=2,
    name="Expected Result Interval from string",
    description="Check if the activation is between two numerator values defined using a string.",
    ###################################################################
    # Note: Here we set the expected result as a list of two          #
    #       numerator values defined using a string                   #
    ###################################################################
    expected_result="[2/100, 15/100] 1/km",
)
@register_signals(EXAMPLE, ExampleSignals)
class ExpectedResultIntervalFromString(TestStep):
    """Example for a testcase that can be tested by a simple pass/fail test."""

    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        self.result.measured_result = Result(
            numerator=len(activation), denominator=100, numerator_is_events=True, unit="1/km"
        )


@verifies("req-001")
@testcase_definition(
    name="Expected Result Interval Example",
    description="Run teststeps with expected results given as an interval.",
)
class ExpectedResultIntervalTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExpectedResultInterval,
            ExpectedResultIntervalFromString,
        ]


def main(data_folder: Path, temp_dir: Path = None, open_explorer=True):
    """Optional, call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    test_bsigs = [data_folder / f"test_input_{k}.bsig" for k in range(3)]
    os.makedirs(data_folder, exist_ok=True)
    for b in test_bsigs:
        generate_bsig(b)

    debug(
        ExpectedResultIntervalTestCase,
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
