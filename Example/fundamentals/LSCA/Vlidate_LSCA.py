#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is most basic example which you can have for TSF.
In this example we are creating a single testcase with a single teststep.
In this would be defining a signal definition and our own bsigs for easy execution.

TRY IT OUT!
Just run the file.
"""


import logging
import os
import sys
import tempfile

from tsf.io.bsig import BsigWriter

from Generic_Bsig import generate_bsig

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.db.results import Result

from LSCA_constant import  ExampleSignals
from pathlib import Path


__author__ = "Shashikala R S"
__copyright__ = "2024-2023, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

EXAMPLE = "example"


@teststep_definition(
    step_number=1,
    name="Check for some_activation_a",
    description="Example for checking the activation of 'some_activation_a' signal",
    expected_result="> 80 %",
)
@register_signals(EXAMPLE, ExampleSignals)
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

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("req-001")
@testcase_definition(
    name="Minimal example1",
    description="The most basic TSF example.",
)

class ExampleMinimalTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleActivation,
        ]

EXAMPLE = "example1"
#creatring 2nd testcase
@teststep_definition(
    step_number=2,
    name="Check for some_activation_b",
    description="Example for checking the activation of 'some_activation_b' signal",
    expected_result="> 90 %",
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleActivation1(TestStep):
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

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.LSCA_Brake_Port] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("req-002")
@testcase_definition(
    name="Minimal example2",
    description="The most basic TSF example.",
)
class ExampleMinimalTestCase1(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleActivation1
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
    #working_directory = Path(tempfile.mkdtemp("_tsf"))
    working_directory = Path('\\Ozl9704w\d\Reports_FFL')

    print(working_directory)
    data_folder = working_directory / "data"
    
    out_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)
