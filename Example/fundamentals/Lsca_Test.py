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

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"

_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

EXAMPLE = "example"

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


class ExampleSignals(SignalDefinition):
    """Example signal definition."""

    class Columns(SignalDefinition.Columns):
        """Column defines."""

        Trunk = "Trunk"
        sigstate = "sigstate"
        DOORFL = "DoorFL"
        DOORFR = "DoorFR"
        DOORBL = "DoorBL"
        DOORBR = "DoorBR"
        Driverseatbelt = "Driverseatbelt"
        Driverseatbeltoccupied = "Driverseatbeltoccupied"
        Ignition_status = "Ignition_status"
        Static_Objects = "Static_Objects"
        Dynamic_objects = "Dynamic_Objects"
        REQUESTMODE = "Request Mode"
        WarningTube = "Warning Tube"
        WarningBody = "Warning Body"
        WarningObject = "Warning Object"
        vel_mps = "vel_mps"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.Trunk: "M7board.CAN_Thread.TrunkLidStatusPort.open_nu",
            self.Columns.sigstate: "M7board.CAN_Thread.StarterStatusPort.signalState_nu",
            self.Columns.DOORFL: "M7board.CAN_Thread.DoorStatusPort.status.frontPsgr_nu",
            self.Columns.DOORFR: "M7board.CAN_Thread.DoorStatusPort.status.driver_nu",
            self.Columns.DOORBR: "M7board.CAN_Thread.DoorStatusPort.status.rearRight_nu",
            self.Columns.DOORBL: "M7board.CAN_Thread.DoorStatusPort.status.rearLeft_nu",
            self.Columns.Driverseatbeltoccupied: "M7board.ConfigurationTrace.MF_AP_LSCA_Parameter.functionBrake"
                                                 ".checkDriverSeatOccupied_nu",
            self.Columns.Driverseatbelt: "M7board.ConfigurationTrace.MF_AP_LSCA_Parameter.functionBrake"
                                         ".checkDriverSeatbelt_nu",
            self.Columns.Ignition_status: "M7board.CAN_Thread.AdditionalBCMStatusPort.ignition.ignitionOn_nu",
            self.Columns.Static_Objects: "M7board.EM_Thread.CollEnvModelPort.numberOfStaticObjects_u8",
            self.Columns.Dynamic_objects: "M7board.EM_Thread.CollEnvModelPort.numberOfDynamicObjects_u8",
            self.Columns.REQUESTMODE: "M7board.EM_Thread.LscaBrakePort.requestMode",
            self.Columns.WarningTube: "M7board.EM_Thread.LscaHMIPort.warningTube",
            self.Columns.vel_mps: "M7board.EM_Thread.EgoMotionPort.vel_mps",
            self.Columns.WarningBody: "M7board.EM_Thread.LscaHMIPort.warningBody",
            self.Columns.WarningObject: "M7board.EM_Thread.LscaHMIPort.warningObject"

        }


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
        # s += "<h3>You can also add pie charts like the one below</h3>"
        # df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
        # df.loc[df["pop"] < 2.0e6, "country"] = "Other countries"  # Represent only large countries
        # fig = px.pie(df, values="pop", names="country", title="Population of European continent")

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=processing_details['mts'],
                y=processing_details['mts'],
                name="mts",
            )
        )
        fig = px.line(x=processing_details['mts'])
        # if 'mts' in processing_details:
        #     fig.add_trace(
        #         go.Scatter(
        #             x=processing_details['mts'],
        #             y=processing_details['mts'],
        #             name="mts",
        #         )
        #     )
        #     fig = px.line(x=processing_details['mts'])
        # else:
        #     fig = px.line(x=[10, 2, 3], y=[4, 5, 6])

        s += fig.to_html(full_html=False, include_plotlyjs=False)
        return s


class CustomTestcaseReport(CustomReportTestCase):
    def overview(self):
        s = "<h3>LSCA sample plots</h3>"

        # data_canada = px.data.gapminder().query("country == 'Canada'")
        # fig = px.bar(data_canada, x="year", y="pop")
        fig = px.line(x=[1, 2, 3], y=[1, 2, 3])
        s += fig.to_html(full_html=False, include_plotlyjs=False)
        return s


###################################################################
# Note: generate_bsig not relevant for users ######################
###################################################################
def generate_bsig(bsig: Path):
    """Generate a BSIG for the example signal definition."""
    exp_sd = ExampleSignals()
    with BsigWriter(bsig) as wrt:
        # timestamps are in microseconds (us) sampling as unit64 data type.
        f = 60e3  # ms
        N = np.random.randint(3000, 8000)
        jitter_max = 3e3  # ms

        # unix timestamp in us
        ts_0 = int(datetime.datetime.utcnow().timestamp() * 1e6)
        ts = np.cumsum(np.ones(N) * f + np.random.randint(0, int(jitter_max), N))
        ts += ts_0
        ts = ts.astype(np.uint64)
        wrt[SignalReader.MTS_TS_SIGNAL] = ts

        sig_a = np.zeros(N)
        samples_a = np.random.randint(1, 10)
        positions = np.random.choice(np.arange(N), samples_a)
        for position in positions:
            sample = np.random.randint(2, 7)
            sig_a[position: position + sample] = 1

        sig_b = np.zeros(N)
        samples_b = np.random.randint(1, 10)
        positions = np.random.choice(np.arange(N), samples_b)
        for position in positions:
            sample = np.random.randint(2, 7)
            sig_b[position: position + sample] = 1

        sig_d = np.zeros(N)
        samples_d = np.random.randint(1, 10)
        positions = np.random.choice(np.arange(N), samples_d)
        for position in positions:
            sample = np.random.randint(2, 7)
            sig_d[position: position + sample] = 1

        # 90% Chance of passing
        binary_activation_a = np.zeros(N)
        if random.random() > 0.02:
            binary_activation_a[N - 1000: N - 900] = 1

        binary_activation_b = np.zeros(N)
        if random.random() > 0.1:
            binary_activation_b[N - 1000: N - 900] = 1

        ego_vx = (np.random.random(N) - 0.5) * 0.2
        ego_vx[0] = 0.01
        corners = random.sample(range(1000, N - 1000), 2)
        u = np.zeros(N)
        c0 = min(corners)
        c1 = max(corners) + 2
        # Ramp to 30 km/h
        u[0:c0] = np.arange(c0) * 30 / (3.6 * c0)
        # constant 30 km/h
        u[c0:c1] = np.ones(c1 - c0) * 30 / 3.6
        # ramp down to 0
        u[c1:N] = 30 / 3.6 - np.arange(N - c1) * 30 / (3.6 * (N - c1))
        # mix with ego vx
        ego_vx = ego_vx + u
        ego_vx = scipy.signal.medfilt(ego_vx, 15)

        wrt[SignalReader.MTS_TS_SIGNAL] = ts
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.Trunk].signals[0]] = sig_a
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.Ignition_status].signals[0]] = sig_b
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.Driverseatbelt].signals[0]] = sig_d
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.Driverseatbeltoccupied].signals[0]] = binary_activation_a
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.DOORBL].signals[0]] = binary_activation_b
        wrt[exp_sd.signal_properties[ExampleSignals.Columns.DOORBR].signals[0]] = ego_vx


@teststep_definition(
    step_number=1,
    name="LSCA Activation",
    description="Checking the activation of LSCA function",
    expected_result="0",
)
@register_signals(EXAMPLE, ExampleSignals)
class LscaActivation(TestStep):
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

        activation = lsca_signals.loc[(lsca_signals[ExampleSignals.Columns.Trunk] == 0)
                                      & (lsca_signals[ExampleSignals.Columns.Ignition_status] == 1) &
                                      (lsca_signals[ExampleSignals.Columns.DOORBR] == 2) & (
                                              lsca_signals[ExampleSignals.Columns.DOORBL] == 2) & \
                                      (lsca_signals[ExampleSignals.Columns.DOORFL] == 2) & (
                                              lsca_signals[ExampleSignals.Columns.DOORFR] == 2) & \
                                      (lsca_signals[ExampleSignals.Columns.Driverseatbelt] == 0) & (
                                              lsca_signals[ExampleSignals.Columns.Driverseatbeltoccupied] == 0)]
        if activation is True:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the test-step
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("35897")
@testcase_definition(
    name="LSCA Activation",
    description="Checking Activation in LSCA",
)
class LSCATestCase(TestCase):
    """Example test case."""

    custom_report = CustomTestcaseReport

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            LscaActivation,
        ]


@teststep_definition(
    name="Static objects",
    description="Checking Static objects in LSCA",
    expected_result="> 10%",
)
@register_signals(EXAMPLE, ExampleSignals)
class StaticActivation(TestStep):
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

        static_signals = self.readers[EXAMPLE].signals

        self.result.details["mts"] = static_signals.as_plain_df[ExampleSignals.Columns.MTS_TS]

        activation = static_signals.loc[(static_signals[ExampleSignals.Columns.Static_Objects] >= 0)]

        if len(activation) >= 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep

        self.result.details["static_obj"] = static_signals.as_plain_df[ExampleSignals.Columns.MTS_TS]


@verifies("35906")
@testcase_definition(
    name="Static Activation",
    description="Checking Activation in Static objects",
)
class LSCATestCase1(TestCase):
    """Example test case."""
    custom_report = CustomTestcaseReport

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            StaticActivation,
        ]


@teststep_definition(
    name="Dynamic objects",
    description="Checking dynamic obstacles is received or not",
    expected_result="> 10%",
)
@register_signals(EXAMPLE, ExampleSignals)
class DynamicActivation(TestStep):
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

        dynamic_signals = self.readers[EXAMPLE].signals

        self.result.details["mts"] = dynamic_signals.as_plain_df[ExampleSignals.Columns.MTS_TS]

        activation = dynamic_signals.loc[(dynamic_signals[ExampleSignals.Columns.Dynamic_objects] >= 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("35907")
@testcase_definition(
    name="Dynamic Activation",
    description="Checking Activation in Dynamic objects",
)
class LSCATestCase2(TestCase):
    """Example test case."""
    custom_report = CustomTestcaseReport

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            DynamicActivation,
        ]


@teststep_definition(
    name="static braking",
    description="static braking analysis",
    expected_result="> 10%",
)
@register_signals(EXAMPLE, ExampleSignals)
class Staticbrake(TestStep):
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

        static_brake_signals = self.readers[EXAMPLE].signals

        self.result.details["mts"] = static_brake_signals.as_plain_df[ExampleSignals.Columns.MTS_TS]

        activation = static_brake_signals.loc[(static_brake_signals[ExampleSignals.Columns.Static_Objects] >= 0) &
                                              (static_brake_signals[ExampleSignals.Columns.REQUESTMODE] == 2)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("35908")
@testcase_definition(
    name="Static Braking",
    description="Static brake analysis",
)
class LSCATestCase3(TestCase):
    """Example test case."""
    custom_report = CustomTestcaseReport

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            Staticbrake,
        ]


@teststep_definition(
    name="LSCA Core check",
    description="LSCA core activation check",
    expected_result="> 10%",
)
@register_signals(EXAMPLE, ExampleSignals)
class LscaCore(TestStep):
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

        lsca_core_signals = self.readers[EXAMPLE].signals

        self.result.details["mts"] = lsca_core_signals.as_plain_df[ExampleSignals.Columns.MTS_TS]

        activation = lsca_core_signals.loc[(lsca_core_signals[ExampleSignals.Columns.vel_mps] <= 0) &
                                           (lsca_core_signals[ExampleSignals.Columns.Trunk] == 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("36001")
@testcase_definition(
    name="Lsca Core",
    description="Lsca Core deactivation",
)
class LSCATestCase4(TestCase):
    """Example test case."""
    custom_report = CustomTestcaseReport

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            LscaCore,
        ]


@teststep_definition(
    name="Dynamic objects analysis",
    description="analyze Dynamic Objects",
    expected_result="> 10%",
)
@register_signals(EXAMPLE, ExampleSignals)
class DynamicObjectsCheck(TestStep):
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

        Dynamic_obj_signals = self.readers[EXAMPLE].signals

        self.result.details["mts"] = Dynamic_obj_signals.as_plain_df[ExampleSignals.Columns.MTS_TS]

        activation = Dynamic_obj_signals.loc[(Dynamic_obj_signals[ExampleSignals.Columns.vel_mps] > 0) &
                                             (Dynamic_obj_signals[ExampleSignals.Columns.WarningObject] == 2) &
                                             (Dynamic_obj_signals[ExampleSignals.Columns.WarningTube] == 2) &
                                             (Dynamic_obj_signals[ExampleSignals.Columns.WarningBody] == 2)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")  # Setting 0 fails the teststep
            return

        self.result.measured_result = Result(100.0, unit="%")  # Setting 100 passes the teststep


@verifies("35996")
@testcase_definition(
    name="Dynamic objects deactivation",
    description="Dynamic objects deactivation check",
)
class LSCATestCase5(TestCase):
    """Example test case."""
    custom_report = CustomTestcaseReport

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            DynamicObjectsCheck,
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
        LSCATestCase,
        LSCATestCase1,
        LSCATestCase2,
        LSCATestCase3,
        LSCATestCase4,
        LSCATestCase5
    ],
        r"D:\TATA\bsigs\exported_file__D2023_10_08_T16_39_56.bsig",
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