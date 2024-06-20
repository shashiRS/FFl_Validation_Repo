#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a quickstart example of reading an ERG file

"""
import logging
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = str(Path(__file__).resolve().parent.parent)
if ROOT not in sys.path:
    sys.path.append(ROOT)

from tsf.core.common import PathSpecification, RelationOperator
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
from tsf.io.erg import ErgSignalDefinition

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

ERG_EXAMPLE = "erg_example"


class MyErgSd(ErgSignalDefinition):
    """Example definition."""

    def __init__(self):
        """Initialize the definition."""
        super().__init__()
        self._properties = {
            "velocity": "Car.v",
            "acceleration": "Car.Fr1.ax",
            "Car.YawRate": "Car.Fr1.ay",
        }


@teststep_definition(
    step_number=1,
    name="Activation",
    description="Example for checking the average of velocity signal",
    expected_result=Result(operator=RelationOperator.LESS, numerator=100, unit="km/h"),
)
@register_signals(ERG_EXAMPLE, MyErgSd)
class ErgExampleActivation(TestStep):
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

        example_signals = self.readers[ERG_EXAMPLE].signals
        example_signals["vel_kmh"] = example_signals["velocity"] * 3.6
        print("test.")

        res = example_signals["vel_kmh"].mean()
        self.result.measured_result = Result(res, unit="km/h")


@verifies("req-001")
@testcase_definition(
    name="Erg example",
    description="Example KPI Test implementation without events.",
)
class ExampleErgTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the erg test steps."""
        return [
            ErgExampleActivation,
        ]


def main(data_folder: Path, temp_dir: Path = None, open_explorer=True):
    """Optional, call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    test_erg = [data_folder / "SetSpeed110.erg"]
    debug(
        [
            ExampleErgTestCase,
        ],
        *test_erg,
        input_pathspecs=[
            PathSpecification(data_folder, extension=".erg"),
        ],
        temp_dir=output_folder,
        open_explorer=open_explorer,
        clean_dir=True,
    )


if __name__ == "__main__":
    working_directory = Path(os.environ.get("TSF_TEMP_DIR", default=tempfile.mkdtemp("_tsf"))) / "erg_example"
    shutil.rmtree(working_directory, ignore_errors=True)

    data_folder = Path(ROOT) / "data" / "erg"
    output_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=output_folder, open_explorer=True)
