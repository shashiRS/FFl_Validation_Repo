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
    CustomReportTestStep,
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)

from tsf.core.report import (
    CustomReportTestCase,
    ProcessingResult,
    ProcessingResultsList,
)

from tsf.core.utilities import debug
import pandas as pd
import plotly.express as px
from TRJPLA_constant import ExampleSignals
from pathlib import Path
from typing import List
from tsf.db.results import Result, TeststepResult

__author__ = "Shashikala R S"
__copyright__ = "2024-2023, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

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
##############################################################################################################

EXAMPLE = "uiVersionNumber"
#creatring 2nd testcase

@teststep_definition(
    step_number=1,
    name="Check for TrjPlaParkingBoxPort.uiVersionNumber",
    description="Example for checking the activation of 'TrjPlaParkingBoxPort.uiVersionNumber' signal",
    expected_result="= 100",
)
@register_signals(alias="EXAMPLE", definition=ExampleSignals)
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
    custom_report = CustomTeststepReport
    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers["EXAMPLE"]

        activation = example_signals.loc[(example_signals["uia"] == 0)]
        print(activation)
        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("req-001")
@testcase_definition(
    name="TRJPLA_DATA uiVersionNumber",
    description="Verify the value for the 'TrjPlaParkingBoxPort.numValidParkingBoxes_nu' is eqaul to 'zero' As of now no value is present in bsig",
)

class ExampleMinimalTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleActivation,

        ]

EXAMPLE = "numValidParkingBoxes_nu"
#creatring 2nd testcase
@teststep_definition(
    step_number=2,
    name="Check for TrjPlaParkingBoxPort.numValidParkingBoxes_nu",
    description="Example for checking the activation of 'TrjPlaParkingBoxPort.numValidParkingBoxes_nu' signal",
    expected_result="= 100",
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
    custom_report = CustomTeststepReport
    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals["valid_pak"] == 0)]
        print(activation)
        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("req-002")
@testcase_definition(
    name="TRJPLA_DATA numValidParkingBoxes_nu",
    description="Verify the value for the 'TrjPlaParkingBoxPort.numValidParkingBoxes_nu' is eqaul to 'zero' As of now no value is present in bsig",
)
class ExampleMinimalTestCase1(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleActivation1
        ]

###################################################################################
#       3rd testcase                                                              #
###################################################################################

EXAMPLE = "numberOfStaticObjects_u8"
#creatring 2nd testcase
@teststep_definition(
    step_number=2,
    name="Check for TrjPlaParkingBoxPort.numberOfStaticObjects_u8",
    description="Example for checking the activation of 'TrjPlaParkingBoxPort.numberOfStaticObjects_u8' signal",
    expected_result="= 100",
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
    custom_report = CustomTeststepReport
    def __init__(self):
        super().__init__()

    def process(self):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals["dyn_obj"] == 0)]
        print(activation)
        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("req-002")
@testcase_definition(
    name="TRJPLA_DATA numberOfStaticObjects_u8",
    description="Verify the value for the 'TrjPlaParkingBoxPort.numberOfStaticObjects_u8' is eqaul to 'zero' As of now no value is present in bsig",
)
class ExampleMinimalTestCase2(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleActivation2
        ]
############################################################################################
#3rd testcase and teststep completed here


###################################################################################
#       4th testcase                                                              #                                                                               #
###################################################################################

EXAMPLE = "numberOfDynamicObjects_u8"
#creatring 2nd testcase
@teststep_definition(
    step_number=2,
    name="Check for TrjPlaParkingBoxPort.numberOfDynamicObjects_u8",
    description="Example for checking the activation of 'TrjPlaParkingBoxPort.numberOfDynamicObjects_u8' signal",
    expected_result="= 100",
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleActivation3(TestStep):
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
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals["nopak_mark"] == 0)]
        print(activation)
        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("req-002")
@testcase_definition(
    name="TRJPLA_DATA numberOfDynamicObjects_u8",
    description="Verify the value for the 'TrjPlaParkingBoxPort.numberOfDynamicObjects_u8' is eqaul to 'zero' As of now no value is present in bsig",
)
class ExampleMinimalTestCase3(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleActivation3
        ]
############################################################################################
#4th testcase and teststep completed here

###################################################################################
#  5th testcase                                                                   #
###################################################################################

EXAMPLE = "numberOfParkMarkings_u8"
#creatring 2nd testcase
@teststep_definition(
    step_number=2,
    name="Check for TrjPlaParkingBoxPort.numberOfParkMarkings_u8",
    description="Example for checking the activation of 'TrjPlaParkingBoxPort.numberOfParkMarkings_u8' signal",
    expected_result="= 100",
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleActivation4(TestStep):
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
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals["static_obj"] == 0)]
        print(activation)
        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("req-002")
@testcase_definition(
    name="TRJPLA_DATA numberOfParkMarkings_u8",
    description="Verify the value for the 'TrjPlaParkingBoxPort.numberOfParkMarkings_u8' is eqaul to 'zero' As of now no value is present in bsig",
)
class ExampleMinimalTestCase4(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleActivation4
        ]
############################################################################################
#5th testcase and teststep completed here

def main(data_folder: Path,temp_dir: Path = tempfile.mkdtemp(), open_explorer=True):
    # Entry point for debugging during development.
    #test_recordings = [Path(rf"\\LUFS009X.li.de.conti.de\prj\RADAR\A\B\C\D\test_input_{k}.rrec") for k in range(3)]
    file_paths = [
    r'D:\JenkinsServer_Main\workspace\Backup_FFL_test\Next_repo\FFL_output\Usecase_1_E_mor_than_9kmph_Pedistrain_2.1.14.bsig',
    r'D:\JenkinsServer_Main\workspace\Backup_FFL_test\Next_repo\FFL_output\Usecase_1_E_mor_than_9kmph_Pedistrain_2.1.14rec2.bsig'
    ]

    test_bsigs = [os.path.join(temp_dir, "data", f"{k}") for k in file_paths]   
    print(test_bsigs)
    data_folder = os.path.join(temp_dir, "data")
    os.makedirs(data_folder, exist_ok=True)
    debug(
        [ExampleMinimalTestCase, ExampleMinimalTestCase1, ExampleMinimalTestCase2, ExampleMinimalTestCase3, ExampleMinimalTestCase4],
        *test_bsigs,
        temp_dir=temp_dir,
        open_explorer=open_explorer,
    )
    _log.debug("All done.")

if __name__ == "__main__":
    #working_directory = Path(tempfile.mkdtemp("_tsf"))
    import time
    timestr = time.strftime("%Y%m%d_%H%M%S")
    
    pat= r"\\cw01.contiwan.com\Root\Loc\blr3\didr3320\ADC544NN-Nissan\Report_Files\FFL_"+timestr
    working_directory = Path(pat)

    with open(r"\\cw01.contiwan.com\Root\Loc\blr3\didr3320\ADC544NN-Nissan\Report_Files\Jenkin_info.txt", "w") as f:
        
        contents = "".join(str(working_directory))
        f.write(contents)
        f.write("\n")


    data_folder = working_directory / "data"
    
    out_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)
