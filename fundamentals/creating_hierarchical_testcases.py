#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""
In this example you would learn how to use group in defining testcases.
You can have multiple testcases belonging to a particular group which would enable for easy filtering and viewing.

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

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@teststep_definition(
    step_number=2,
    name="Teststep2",
    description="Result should be 0.0",
    expected_result="> 80 %",
)
@register_signals(EXAMPLE, ExampleSignals)
class Zero(TestStep):
    """Example for a testcase that can be tested by a simple pass/fail test.

    Objective
    ---------

    Check if measured result is 0%

    Detail
    ------
    Returns Result as Zero
    The test is performed for all recordings of the collection
    """

    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        self.result.measured_result = Result(0, unit="%")


@teststep_definition(
    step_number=1,
    name="Teststep1",
    description="Result should be 100.0",
    expected_result="> 80 %",
)
@register_signals(EXAMPLE, ExampleSignals)
class Hundred(TestStep):
    """Example for a testcase that can be tested by a simple pass/fail test.

    Objective
    ---------

    Check if measured result is 100%

    Detail
    ------
    Returns Result as a hundred
    The test is performed for all recordings of the collection
    """

    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        self.result.measured_result = Result(100, unit="%")


@verifies("req-001")
@testcase_definition(
    name="Testcase1",
    description="Here we are defining this testcase with group 1",
    ###################################################################
    # Note: Here is how you can add a group to testcases ##############
    ###################################################################
    group="Group1",
)
class BasicTestCase1(TestCase):
    @property
    def test_steps(self):
        return [
            Zero,
            Hundred,
        ]


@verifies("req-002")
@testcase_definition(
    name="Testcase2",
    description="Here we are defining this testcase with group 2",
    ###################################################################
    # Note: Here is how you can add a group to testcases ##############
    ###################################################################
    group="Group2",
)
class BasicTestCase2(TestCase):
    @property
    def test_steps(self):
        return [
            Zero,
            Hundred,
        ]


@verifies("req-003")
@testcase_definition(
    name="Testcase3",
    description="Here we are defining this testcase with group 3",
    ###################################################################
    # Note: Here is how you can add a group to testcases ##############
    ###################################################################
    group="Group3",
)
class BasicTestCase3(TestCase):
    @property
    def test_steps(self):
        return [
            Zero,
            Hundred,
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
            BasicTestCase1,
            BasicTestCase2,
            BasicTestCase3,
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
