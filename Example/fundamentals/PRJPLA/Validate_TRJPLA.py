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

from TRJPLA_constant import ExampleSignals
from pathlib import Path


__author__ = "Shashikala R S"
__copyright__ = "2024-2023, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

EXAMPLE = "uiVersionNumber"
#creatring 2nd testcase

@teststep_definition(
    step_number=1,
    name="Check for TrjPlaParkingBoxPort.uiVersionNumber",
    description="Example for checking the activation of 'TrjPlaParkingBoxPort.uiVersionNumber' signal",
    expected_result="=100",
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


def main(data_folder: Path, temp_dir: Path = None, open_explorer=True):
    """Optional, call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """

    debug(
        [ExampleMinimalTestCase,ExampleMinimalTestCase1,ExampleMinimalTestCase2,ExampleMinimalTestCase3,ExampleMinimalTestCase4],
        r'D:\JenkinsServer_Main\workspace\FFL_testing\Next_repo\FFL_output\Usecase_1_E_mor_than_9kmph_Pedistrain_2.1.14.bsig',
        temp_dir=temp_dir,
        open_explorer=open_explorer,
        kpi_report=False,
        dev_report=True,
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
