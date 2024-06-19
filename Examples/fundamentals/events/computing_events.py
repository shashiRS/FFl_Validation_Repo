#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example you would learn about events and how to compute events.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

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
from tsf.core.utilities import debug
from tsf.db.assessments import AssessmentAttributeFactory as aaf
from tsf.db.assessments import AssessmentStateFactory as asf
from tsf.db.assessments import ExplicitAssessment
from tsf.db.events import AttributeType, Event, EventAttribute, TimeBase
from tsf.io.datamodel import SignalDataFrame

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

    max_ego_velocity = EventAttribute("Max. EGO Velocity", AttributeType.FLOAT)

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
class EventComputationExampleTeststep(TestStep):
    def __init__(self):
        super().__init__()

        ###################################################################
        # Note: Here you can do some event computation ####################
        ###################################################################

    def process_event(self, activation: SignalDataFrame):
        """Compute the event base data and the custom attributes.

        :param activation: dataframe of only the activation
        """
        _log.debug("Computing event statistics")

        event = MyEvent1(
            start_timestamp=activation.index.values[0],
            end_timestamp=activation.index.values[-1],
        )

        max_ego_velocity = activation[ExampleSignals.Columns.EGO_VELO].max()

        # Attach the event to result, or not maybe some might be skipped automatically...
        if max_ego_velocity < 0:
            self.result.details["MyEvent1"]["unknown"] += 1
            return

        event.max_ego_velocity = max_ego_velocity

        self.result.add_event(event)

    def process(self):
        """Checks the given input dta for dynamic acute warnings."""
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals
        example_signals["row_idx"] = np.arange(0, len(example_signals))

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)].copy()

        self.result.measured_result = Result(denominator=10, unit="1/km", numerator_is_events=True)

        activation["event_start"] = activation["row_idx"].diff() != 1
        activation["event_idx"] = activation["event_start"].cumsum()

        _log.info("Found '{}' event(s)".format(activation["event_start"].sum()))

        activation.groupby(activation["event_idx"]).apply(self.process_event)


@verifies("req-001")
@testcase_definition(
    name="Event with assessments example",
    description="This example demonstrates how to computes events.",
)
class EventComputationExampleTestcase(TestCase):
    @property
    def test_steps(self):
        """Define the test steps."""
        return [EventComputationExampleTeststep]


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
        EventComputationExampleTestcase,
        *test_bsigs,
        temp_dir=temp_dir,
        kpi_report=False,
        dev_report=True,
        open_explorer=open_explorer,
    )
    _log.debug("All done.")


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))

    data_folder = working_directory / "data"
    out_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)
