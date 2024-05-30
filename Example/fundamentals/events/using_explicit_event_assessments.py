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
from tsf.db.assessments import ExplicitAssessment
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
class MyAssessment1(ExplicitAssessment):
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

    attr_1 = aaf.integer_attribute("Attribute 1", 0, 10, 1, default=5)


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


###################################################################
# Note: Here is how you define your other assessment ##############
###################################################################
class MyAssessment2(ExplicitAssessment):
    states = {
        "CAT1": asf.state("CAT1", relevant=False),
        "CAT2": asf.state("CAT2", relevant=False),
        "CAT3": asf.state("CAT3", relevant=False),
        "CAT4": asf.state("CAT4", relevant=True),
        "CAT5": asf.state("CAT5", relevant=True),
    }

    attr_1 = aaf.integer_attribute("Attribute 1", 0, 10, 1, default=5)


###################################################################
# Note: Here is how you define your other event ###################
###################################################################
class MyEvent2(Event):
    """Example for a custom EBA event."""

    assessment_type = MyAssessment2

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

        cat1 = MyEvent2(1, 2)
        cat1.explain = "cat1"
        cat2 = MyEvent2(3, 3)
        cat2.explain = "cat2"
        cat3 = MyEvent2(4, 5)
        cat3.explain = "cat3"
        cat4 = MyEvent2(6, 7)
        cat4.explain = "cat4"
        cat5 = MyEvent2(8, 9)
        cat5.explain = "cat5"

        na = MyEvent2(10, 11)
        na.explain = "na"

        self.result.add_event(cat1)
        self.result.add_event(cat2)
        self.result.add_event(cat3)
        self.result.add_event(cat4)
        self.result.add_event(cat5)
        self.result.add_event(na)

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
        gi = dbc.processing_inputs.get_input(name="test_input_0")
        fp = MyAssessment1(8, 14, collection_entry=gi, state=MyAssessment1.states["False Positive"])
        tp = MyAssessment1(18, 24, collection_entry=gi, state=MyAssessment1.states["True Positive"])
        na1 = MyAssessment1(38, 44, collection_entry=gi, state=MyAssessment1.states["NOT ASSESSED"])

        na2 = MyAssessment1(48, 51, collection_entry=gi, state=MyAssessment1.states["False Positive"])
        na3 = MyAssessment1(61, 64, collection_entry=gi, state=MyAssessment1.states["False Positive"])

        dbc.assessments.add_assessment(fp)
        dbc.assessments.add_assessment(tp)

        dbc.assessments.add_assessment(na1)
        dbc.assessments.add_assessment(na2)
        dbc.assessments.add_assessment(na3)

        c = MyAssessment2(1, 2, collection_entry=gi, state=MyAssessment2.states["CAT1"])
        dbc.assessments.add_assessment(c)
        c = MyAssessment2(3, 3, collection_entry=gi, state=MyAssessment2.states["CAT2"])
        dbc.assessments.add_assessment(c)
        c = MyAssessment2(4, 5, collection_entry=gi, state=MyAssessment2.states["CAT3"])
        dbc.assessments.add_assessment(c)
        c = MyAssessment2(6, 7, collection_entry=gi, state=MyAssessment2.states["CAT4"])
        dbc.assessments.add_assessment(c)
        c = MyAssessment2(8, 9, collection_entry=gi, state=MyAssessment2.states["CAT5"])
        dbc.assessments.add_assessment(c)
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
