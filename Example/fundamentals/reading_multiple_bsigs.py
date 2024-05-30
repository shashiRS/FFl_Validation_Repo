#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn how to read two bsigs in parallel with debug(..) function.

TRY IT OUT!
Just run the file.
"""
import logging
import tempfile
from pathlib import Path

from tsf.core.common import PathSpecification
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

from utilities.generate_data import generate_bsig_multiple
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

c = ExampleSignals.Columns


@teststep_definition(
    step_number=1,
    name="Check for some_activation_a",
    description="Example for checking the activation of 'some_activation_a' Signal",
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
            self.result.measured_result = Result(0, unit="%")
            return

        self.result.measured_result = Result(50.0, unit="%")

@teststep_definition(
    step_number=1,
    name="Check for some_activation_b",
    description="Example for checking the activation of 'some_activation_a' Signal",
    expected_result="> 80 %",
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleActivation2(TestStep):
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
            ExampleActivation2,
        ]


def main(data_folder: Path, temp_dir: Path = None, open_explorer=True):
    """Minimal example how to use 2 bsigs in parallel with debug(...)."""

    ###################################################################
    # Note: Here is how you can list of recordings of interest ########
    ###################################################################
    test_recordings = [Path(rf"\\LUFS009X.li.de.conti.de\prj\RADAR\A\B\C\D\test_input_{k}.rrec") for k in range(3)]
    for rec in test_recordings:
        generate_bsig_multiple(data_folder, rec.stem + ".bsig")

    ###################################################################
    # Note: Here is how you can define the simulation output folders ##
    ###################################################################
    input_pathspecs = [
        PathSpecification(data_folder / "bin_data_1", prefix="", suffix="", extension=".bsig"),
        PathSpecification(data_folder / "bin_data_2", prefix="", suffix="", extension=".bsig"),
    ]

    debug(
        [
            ExampleMinimalTestCase,
        ],
        *test_recordings,
        input_pathspecs=input_pathspecs,
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
