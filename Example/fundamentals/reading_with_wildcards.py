#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn to use how to use wildcards in signal definitions.
Wildcards allow use to read all signals which match the string preceding and succeeding the wildcard.
We use "%" as a wildcard.

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

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class NewExampleSignals(ExampleSignals):
    """Example signal reading mapping for EBA signals."""

    class Columns(ExampleSignals.Columns):
        """Column defines."""

        ACTIVATIONS = "some_activations"

    def __init__(self):
        super().__init__()

        self._root = "Example Signal Data"

        self._properties = [
            ###################################################################
            # Note: reading a signal using wildcard ###########################
            ###################################################################
            (
                self.Columns.ACTIVATIONS,
                ".activation.sig_%",  # "%" finds all the signals with similar structure i.e. sig_a, sig_b, sig_d
            )
        ]


@teststep_definition(
    step_number=1,
    name="Check for some_activation_a",
    description="Example for checking the activation of 'some_activation_a' Signal",
    expected_result="> 80 %",
)
@register_signals("SIGNALS", NewExampleSignals)
class ExampleActivation(TestStep):
    """Example for a testcase that can be tested by a simple pass/fail test.

    Objective
    ---------

    Check every occurrence when signal 'some_activation_a'

    Detail
    ------

    In case there is no signal change to 1 the testcase is failed.
    The test ist performed for all recordings of the collection
    """

    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers["SIGNALS"].signals
        activation = example_signals.loc[(example_signals[(NewExampleSignals.Columns.ACTIVATIONS, "a")] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")
            return

        self.result.measured_result = Result(100.0, unit="%")


@verifies("req-001")
@testcase_definition(
    name="Minimal example",
    description="Example KPI Test implementation without events.",
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
        [
            ExampleMinimalTestCase,
        ],
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
