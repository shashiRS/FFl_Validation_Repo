#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the most basic example which you can have for TSF.
In this example we are creating a single testcase with a single teststep.
In this would be defining a signal definition and our own bsigs for easy execution.

TRY IT OUT!
Just run the file.
"""

import datetime
import logging
import os
import random
import sys
import tempfile
from pathlib import Path
from typing import List

import numpy as np
import plotly.express as px
from plotly import graph_objects as go
import scipy
from tsf.db.results import TeststepResult
from tsf.io.bsig import BsigWriter
from tsf.io.signals import SignalDefinition, SignalReader

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.utilities import debug
from tsf.db.results import Result
from fundamentals.Nissan.NN_constants import ExampleSignals
from fundamentals.Nissan.NN_Test_Report import *

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"

_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

EXAMPLE = "example"

from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)


@teststep_definition(
    step_number=1,
    name="Bsig Activation check",
    description="Checking the activation of a function",
    expected_result="0",
)
@register_signals(EXAMPLE, ExampleSignals)
class SmokeTest(TestStep):
    """Example for a testcase that can be tested by a simple pass/fail test.

    Objective
    ---------

    Check every occurrence when signal 'some_activation_a'

    Detail
    ------

    In case there is no signal change to 1 the testcase is failed.
    The test ist performed for all recordings of the collection
    """
    custom_report = CustomTeststepReport

    def __init__(self):
        super().__init__()

    def process(self):
        # import pdb;pdb.set_trace()
        _log.debug("Starting processing...")

        lsca_signals = self.readers[EXAMPLE].signals

        self.result.details["mts"] = lsca_signals.as_plain_df[ExampleSignals.Columns.MTS_TS]

        activation = lsca_signals.loc[(lsca_signals[ExampleSignals.Columns.Trunk] == 0) &
                                      (lsca_signals[ExampleSignals.Columns.DOORBR] == 2) & (
                                              lsca_signals[ExampleSignals.Columns.DOORBL] == 2) & \
                                      (lsca_signals[ExampleSignals.Columns.DOORFL] == 2) & (
                                              lsca_signals[ExampleSignals.Columns.DOORFR] == 2)]
        if activation is True:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the test-step
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("35897")
@testcase_definition(
    name="BSIG Activation",
    description="Checking Activation in Bsig",
)
class SmokeTestCase(TestCase):
    """Example test case."""

    custom_report = CustomTestcaseReport

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            SmokeTest,
        ]

def main(data_folder: Path, temp_dir: Path = None, open_explorer=True):
    """Optional, call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    # test_bsigs = [data_folder / f"test_input_{k}.bsig" for k in range(3)]
    # os.makedirs(data_folder, exist_ok=True)
    # for b in test_bsigs:
    #     generate_bsig(b)

    debug([
        SmokeTestCase
    ],
        r"D:\\JenkinsServer_Main\\workspace\\FFl_Build\\FFL_output\\Usecase_1_E_mor_than_9kmph_Pedistrain_2.1.14.bsig",
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
