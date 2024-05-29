#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example you would learn how to create a custom output of the testrun on the overview page using custom overview
plugin.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.report import CustomReportOverview
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
from tsf.testbench._internals.report import Report
from tsf.testbench._internals.report_common import TestrunContainer

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"

_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


###################################################################
# Note: Here we define the custom overview reporting class ########
###################################################################
class CustomOverview(CustomReportOverview):
    def build(self, testrun_container: TestrunContainer) -> str:
        r = ""

        for tc_name, tc_ctr in testrun_container.testcase_containers.items():
            r += f"<div>TC: {tc_name}"
            for ts_name, ts_ctr in tc_ctr.teststep_containers.items():
                r += f"<br>TS: {ts_name}<br/>Result: {ts_ctr.measured_result}</div>"

        return r


@teststep_definition(
    step_number=1,
    name="Check for some_activation_a",
    description="Example for checking the activation of 'some_activation_a' signal",
    expected_result="> 80 %",
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleActivation(TestStep):
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
    name="Overview plugin",
    description="The most basic TSF example with a custom overview plugin.",
)
class ExampleTestCase(TestCase):
    @property
    def test_steps(self):
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

    _, testrun_id, cp = debug(
        ExampleTestCase,
        *test_bsigs,
        temp_dir=temp_dir,
        open_explorer=open_explorer,
        dev_report=False,
    )
    return testrun_id, cp


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))

    data_folder = working_directory / "data"
    out_folder = working_directory / "out"

    testrun_id, cp = main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)

    run_spec = out_folder / "run_spec.json"
    report = Report(
        testrun_id,
        Path(os.path.join(out_folder, "report")),
        out_folder,
        run_spec,
        development_details=True,
        connection_provider=cp,
        redo_all=True,
        from_hpc_preprocessing=True,
        is_regression=False,
        overview_plugins=[
            "fundamentals.reporting.creating_custom_overview_plugin.CustomOverview",
        ],
    )

    report.make_all()
    _log.debug("All done.")
