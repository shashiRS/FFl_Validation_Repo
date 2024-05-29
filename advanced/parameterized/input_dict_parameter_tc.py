#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn how to define multiple test cases with one or more param iterations.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

from tsf.core.common import RelationOperator
from tsf.db.processing_input import ProcessingInputSet

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core._internals.signal_registry import Assignment
from tsf.core.parameterized_testcase import (
    ParameterizedTestCase,
    ParameterSet,
    TeststepParameter,
)
from tsf.core.results import Result
from tsf.core.testcase import TestStep, register_signals, teststep_definition
from tsf.core.utilities import debug

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


input_dict = {
    "TestcaseA": {
        "ExampleActivationA": 75,
        "ExampleActivationB": 90,
    },
    "TestcaseB": {
        "ExampleActivationA": 65,
        "ExampleActivationB": 10,
    },
    "TestcaseC": {
        "ExampleActivationA": 55,
        "ExampleActivationB": 17,
    },
    "TestcaseD": {
        "ExampleActivationA": 45,
        "ExampleActivationB": 19,
    },
}


@teststep_definition(
    step_number=1,
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleActivationA(TestStep):
    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")
            return

        self.result.measured_result = Result(100.0, unit="%")


@teststep_definition(
    step_number=2,
    name="Activation B",
    description="Check for 'some activation_b'",
    expected_result=Result(operator=RelationOperator.GREATER_OR_EQUAL, numerator=100, unit="%"),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleActivationB(TestStep):
    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")
            return

        self.result.measured_result = Result(100.0, unit="%")


class ParametersExample(ParameterizedTestCase):
    parameter_sets = []

    for testcase in input_dict.keys():
        parameter_set = ParameterSet(
            name=f"{testcase}",
            description="This is a testcase with input dictionary",
            assignments=[
                Assignment(
                    ctype=ProcessingInputSet,
                    name="Debug",
                )
            ],
            verifies=[f"req_{testcase}"],
            teststep_parameters=[
                TeststepParameter(
                    test_step=ExampleActivationA,
                    name="Activation A",
                    description="Check for 'some activation_a'",
                    expected_result=Result(operator=RelationOperator.GREATER_OR_EQUAL, numerator=100, unit="%"),
                    doors_url="-",
                ),
                TeststepParameter(
                    test_step=ExampleActivationB,  # the rest is defined in the test step itself
                ),
            ],
        )
        parameter_sets.append(parameter_set)


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
        [ParametersExample],
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
