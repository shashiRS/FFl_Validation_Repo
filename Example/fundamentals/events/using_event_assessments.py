#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example you would learn about events and how to assess those events.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.results import Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug, show_result
from tsf.db.assessments import AssessmentAttributeFactory as aaf
from tsf.db.assessments import AssessmentStateFactory as asf
from tsf.db.assessments import EventAssessment, ExplicitAssessment
from tsf.db.connect import DatabaseConnector
from tsf.db.events import AttributeType, Event, EventAttribute, TimeBase

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)


###################################################################
# Note: Here is how you define your assessments ###################
###################################################################
class MyAssessment1(EventAssessment, ExplicitAssessment):
    states = {
        "False Positive": asf.state(
            "False Positive",
            relevant=True,
            explanation="The assessed event is a false positive",
        ),
        "True Positive": asf.state(
            "True Positive",
            relevant=False,
            explanation="The assessed event is a true positive and shall not be counted in the KPI",
        ),
        "NOT ASSESSED": asf.state("Not assessed", relevant=False, explanation="No assessment available yet"),
    }

    # Example of an additional attribute
    problem_cluster = aaf.selection_attribute(
        "Problem Cluster",
        [
            "UseCase",
            "ARS_Ghost",
        ],
    )


###################################################################
# Note: Here is how you define your event #########################
###################################################################
class MyEvent1(Event):
    """Example for a custom EBA event."""

    assessment_type = MyAssessment1

    explain = EventAttribute("Explanation", AttributeType.STRING)

    def __init__(
        self,
        start_timestamp: int = None,
        end_timestamp: int = None,
    ):
        super().__init__(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            timebase=TimeBase.MTS_PACKAGE_TIMESTAMP,
        )


@teststep_definition(
    step_number=1,
    name="Compute events",
    description="Detect event and stores them in the db",
    expected_result="< 1 Events/km",
)
@register_signals(EXAMPLE, ExampleSignals)
class EventAssessmentExampleTeststep(TestStep):
    def __init__(self):
        super().__init__()

    def process(self):
        """Checks the given input dta for dynamic acute warnings."""
        _log.debug("Starting processing...")

        ###################################################################
        # Note: Here are some example events ##############################
        ###################################################################
        fp = MyEvent1(10, 12)
        fp.explain = "FP"

        tp = MyEvent1(20, 22)
        tp.explain = "TP"

        na = MyEvent1(30, 32)
        na.explain = "not assessed"

        na1 = MyEvent1(40, 42)
        na1.explain = "not assessed with assessment"

        na2 = MyEvent1(50, 52)
        na2.explain = "not assessed partial overlap only on start"

        na3 = MyEvent1(60, 62)
        na3.explain = "not assessed partial overlap only on end"

        self.result.add_event(fp)
        self.result.add_event(tp)
        self.result.add_event(na)
        self.result.add_event(na1)
        self.result.add_event(na2)
        self.result.add_event(na3)

        self.result.measured_result = Result(denominator=2.0, unit="1/km", numerator_is_events=True)


@verifies("req-001")
@testcase_definition(
    name="Event with assessments example",
    description="This example demonstrates how to map assessment types to events.",
)
class EventAssessmentExampleTestcase(TestCase):
    @property
    def test_steps(self):
        """Define the test steps."""
        return [EventAssessmentExampleTeststep]


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

    w, trid, cp = debug(
        EventAssessmentExampleTestcase,
        *test_bsigs,
        temp_dir=temp_dir,
        kpi_report=False,
        dev_report=True,
        open_explorer=open_explorer,
    )

    with DatabaseConnector(cp) as dbc:
        ###################################################################
        # Note: Here we are auto-labelling these events with assessments ##
        ###################################################################
        events = dbc.events.get_events()  # All for example purposes

        fp = MyAssessment1(events[0], state=MyAssessment1.states["False Positive"])
        tp = MyAssessment1(events[1], state=MyAssessment1.states["True Positive"])

        dbc.assessments.add_assessment(fp)
        dbc.assessments.add_assessment(tp)
        ###################################################################
        # Note: These assessments are generally done tools like Matchbox ##
        ###################################################################

        dbc.commit()

    show_result(w, trid, open_explorer=True, connection_provider=cp, build_dev_report=True)
    _log.debug("All done.")


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))

    data_folder = working_directory / "data"
    out_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)
