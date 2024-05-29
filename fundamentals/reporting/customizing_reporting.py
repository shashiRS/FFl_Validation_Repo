#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example you would learn how to customize reporting of teststep page and testcase page.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import List

import plotly.express as px

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.report import (
    CustomReportTestCase,
    ProcessingResult,
    ProcessingResultsList,
)
from tsf.core.testcase import (
    CustomReportTestStep,
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.db.results import Result, TeststepResult

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"

_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


###################################################################
# Note: Here we define the custom reporting for teststep ##########
###################################################################
class CustomTeststepReport(CustomReportTestStep):
    def overview(
            self,
            processing_details_list: ProcessingResultsList,
            teststep_result: List["TeststepResult"],
    ):
        s = "<h3>Additional Data</h3>"

        # Iterating over all processing details
        pr_list = processing_details_list
        for d in range(len(pr_list)):
            json_entries = ProcessingResult.from_json(pr_list.processing_result_files[d])
            s += "Item ID is : {}<br/><br/>".format(json_entries.item_id)
            s += "Result is : {}<br/><br/>".format(json_entries.details["Result"])
        return s

    def details(self, processing_details: ProcessingResult, teststep_result: "TeststepResult") -> str:
        s = "<h3>details part</h3>"
        for k, v in processing_details.details.items():
            s += "<div>{}:{}</div>".format(k, v)

        s += "<h3>Events part</h3>"
        for event in teststep_result.events:
            s += "<div>{}</div>".format(event)

        s += "<div>Measured (part) Result: {}</div>".format(teststep_result.measured_result)
        s += "<h3>You can also add pie charts like the one below</h3>"
        df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
        df.loc[df["pop"] < 2.0e6, "country"] = "Other countries"  # Represent only large countries
        fig = px.pie(df, values="pop", names="country", title="Population of European continent")
        s += fig.to_html(full_html=False, include_plotlyjs=False)
        return s


###################################################################
# Note: Here we define the custom reporting for testcase ##########
###################################################################
class CustomTestcaseReport(CustomReportTestCase):
    def overview(self):
        # s = "<h3>You can also add bar charts like the one below</h3>"
        s = "<h3> First plot </h3>"

        data_canada = px.data.gapminder().query("country == 'India'")
        fig = px.bar(data_canada, x="year", y="pop")
        s += fig.to_html(full_html=False, include_plotlyjs=False)
        return s


@teststep_definition(
    step_number=1,
    name="Check for some_activation_a",
    description="Example for checking the activation of 'some_activation_a' signal",
    expected_result="> 80 %",
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleActivation(TestStep):
    custom_report = CustomTeststepReport

    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")
            self.result.details["Result"] = "Fail"
            return

        self.result.measured_result = Result(100.0, unit="%")
        self.result.details["Result"] = "Pass"


@verifies("req-001")
@testcase_definition(
    name="Custom reporting",
    description="The most basic TSF example with custom reporting.",
)
class ExampleTestCase(TestCase):
    custom_report = CustomTestcaseReport

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

    debug(
        ExampleTestCase,
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
