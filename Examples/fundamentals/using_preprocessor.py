#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn how to create the pre-processors and use them in tandem with teststeps.
Pre-processors allow for single reading of data and generate an intermediate dataframe which can be later used with all
the teststeps.
Thus, reducing the amount of open and close operations with each teststep.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.testcase import (
    PreProcessor,
    TestCase,
    TestStep,
    register_pre_processor,
    register_signals,
    testcase_definition,
    teststep_definition,
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


class MyPreprocessor(PreProcessor):
    ###################################################################
    # Note: Here is how you create a preprocessor #####################
    ###################################################################
    def pre_process(self):
        # Compute an activation df
        example_signals = self.readers[EXAMPLE].signals
        example_signals["row_idx"] = np.arange(0, len(example_signals))

        # Check for activations
        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)].copy()

        # Can be accessed in ts by self.pre_processors["alias"]
        return activation


@teststep_definition(
    step_number=1,
    name="EXP 1",
    description="A Teststep",
    expected_result="> 80 %",
)
@register_signals(alias=EXAMPLE, definition=ExampleSignals)
###################################################################
# Note: Here is how you register a preprocessor ###################
###################################################################
@register_pre_processor(alias="some_activation", pre_processor=MyPreprocessor)
class Exp1(TestStep):
    """Demonstrates the usage of preprocessors."""

    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        df = self.pre_processors["some_activation"]

        if len(df) > 0:
            self.result.measured_result = Result.from_string("100 %")


@teststep_definition(
    step_number=2,
    name="EXP 2",
    description="Another Teststep",
    expected_result="> 80 %",
)
@register_signals(alias=EXAMPLE, definition=ExampleSignals)
###################################################################
# Note: Here is how you register a preprocessor ###################
###################################################################
@register_pre_processor("some_activation", MyPreprocessor)
class Exp2(TestStep):
    """Second teststep."""

    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        df = self.pre_processors["some_activation"]

        if len(df) > 0:
            self.result.measured_result = Result.from_string("100 %")

        self.result.measured_result = Result(0, unit="%")


@teststep_definition(
    step_number=1,
    name="EXP 3",
    description="Another Teststep but mapped to another testcase",
    expected_result="> 80 %",
)
@register_signals(alias=EXAMPLE, definition=ExampleSignals)
###################################################################
# Note: Here is how you register a preprocessor ###################
###################################################################
@register_pre_processor("some_activation", MyPreprocessor)
class Exp3(TestStep):
    """Second teststep."""

    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        df = self.pre_processors["some_activation"]

        if len(df) > 0:
            self.result.measured_result = Result.from_string("100 %")


@testcase_definition(
    name="PreProcessor example 1",
    description="Demonstrates the use of preprocessors",
)
class ExpTc1(TestCase):
    @property
    def test_steps(self):
        return [Exp1, Exp2]


@testcase_definition(
    name="PreProcessor example 2",
    description="Verifies the functionality across test cases",
)
class ExpTc2(TestCase):
    @property
    def test_steps(self):
        return [
            Exp3,
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
        [ExpTc1, ExpTc2],
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
