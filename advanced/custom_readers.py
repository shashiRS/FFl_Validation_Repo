#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example demonstrates how to hook a custom reader replacing the default reader implementation.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.common import RelationOperator
from tsf.core.results import Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.io.datamodel import SignalDataFrame
from tsf.io.signals import SignalDefinition, SignalReader

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)


class MyCustomReader(SignalReader):
    def __init__(self, filename, signal_definition: SignalDefinition, **kwargs):
        super().__init__(filename, signal_definition, **kwargs)

    @property
    def signals(self) -> SignalDataFrame:
        ###################################################################
        # Note: Here we define a custom columns ###########################
        ###################################################################
        self._df["new_column"] = 1  # Add new_column with 1 as value over the whole dataframe
        self._df["sig_a_minus_sig_b"] = (
            self._df[self._defs.Columns.ACTIVATION_A] - self._df[self._defs.Columns.ACTIVATION_B]
        )  # Here we are subtracting values from two columns just for fun
        return self._df


@teststep_definition(
    step_number=1,
    name="Activation",
    description="Check for 'some activation'",
    expected_result=Result(operator=RelationOperator.GREATER_OR_EQUAL, numerator=100, unit="%"),
)
@register_signals(EXAMPLE, ExampleSignals, custom_reader_hook=MyCustomReader)
class ExampleActivation(TestStep):
    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        ###################################################################
        # Note: Here cross check the value defined in our custom reader ###
        ###################################################################
        if not (all(example_signals["new_column"]) and example_signals["sig_a_minus_sig_b"].unique() != [0, 1, -1]):
            self.result.measured_result = Result(0, unit="%")
            return

        self.result.measured_result = Result(100.0, unit="%")


@verifies("req-001")
@testcase_definition(
    name="Custom reader testcase",
    description="This example demonstrates how to assign and use custom readers.",
)
class ExampleMinimalTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleActivation,
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
        ExampleMinimalTestCase,
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
