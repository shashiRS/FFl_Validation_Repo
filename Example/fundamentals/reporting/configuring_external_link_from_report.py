#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example you would learn how to create and customize static page and add an external link to it.
You can use these kind of pages to help users of report can use to look another connected. Such as formulas, pictures,
graphs or animations.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import tempfile
from pathlib import Path

from tsf.core.report import CustomReportExternalLink, CustomReportStaticReportContents
from tsf.core.results import Result
from tsf.core.testcase import (
    ExternalLink,
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition, StaticReportContents,
)
from tsf.core.utilities import debug

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


###################################################################
# Note: Here we define custom reporting for the external link #####
###################################################################
class ExternalLinkReportClass(CustomReportExternalLink):
    """Example External link page."""

    url_name = "External Link Pages"
    link = "file://cw01.contiwan.com/root/Loc/lndp/didr2540/public_data/reports/" \
           "development_reports/endurance_report/html/index.html"


class ExternalLinkReportClassNoLinks(CustomReportExternalLink):
    """Example External link page with no external links added.
    In case if the user did not provide the link, the element will not be added to drop down.
    """
    url_name = "External No Link"

###################################################################
# Note: Here is how you can define static page with external link #
###################################################################
class StaticPageReportClass(CustomReportStaticReportContents, CustomReportExternalLink):
    """Example static page and External Link page"""

    name = "Static Page"
    CustomReportExternalLink.name = "External Link"
    link = "file://cw01.contiwan.com/root/Loc/lndp/didr2540/public_data/reports/" \
           "development_reports/endurance_report/html/index.html"

    def overview(self) -> str:
        return "Static Demo Page"


class StaticPageClass(ExternalLink, StaticReportContents):
    """Example static page with External link"""

    custom_report = StaticPageReportClass
    external_link_report = StaticPageReportClass


class ExternalLinkPageClass(ExternalLink):
    """Example external link page."""

    external_link_report = ExternalLinkReportClass


class ExternalLinkPageClassNoLink(ExternalLink):
    """Example external link page."""

    external_link_report = ExternalLinkReportClassNoLinks


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


@testcase_definition(
    name="Example Usecase Test implementation",
    description="This example demonstrates how to process carmaker erg files within the TSF test scripting framework.",
)
class ExampleUsecaseTestCase(TestCase):
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
        ExampleUsecaseTestCase,
        *test_bsigs,
        static_report_contents=StaticPageClass,
        external_report_contents=[
            ExternalLinkPageClass,
            ExternalLinkPageClassNoLink,
            StaticPageClass
        ],
        temp_dir=temp_dir,
        open_explorer=open_explorer,
        kpi_report=False,
        dev_report=True,
    )


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))

    data_folder = working_directory / "data"
    out_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)

    _log.debug("All done.")
