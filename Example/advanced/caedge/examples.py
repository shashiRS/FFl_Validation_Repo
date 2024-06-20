#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quickstart example."""
import logging
import sys
from typing import Dict, List

import numpy as np

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core._internals.processing_utils import ProcessingResult, ProcessingResultsList
from tsf.core.common import AggregateFunction, RelationOperator
from tsf.core.report import CustomReportTestCase, CustomReportTestStep, html_escape
from tsf.core.results import ExpectedResult, Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_inputs,
    register_signals,
    testcase_definition,
    teststep_definition,
)
from tsf.db.assessments import AssessmentStateFactory, ExplicitAssessment
from tsf.db.events import Event
from tsf.db.results import TeststepResult

from utilities.signal_definitions import EXAMPLE, ExampleSignals

_log = logging.getLogger(__name__)


class ExampleAssessment(ExplicitAssessment):
    """Example Assessment."""

    states = {
        "FP": AssessmentStateFactory.state(name="FP", relevant=True),
        "CORNER_CASE": AssessmentStateFactory.state(name="CORNER_CASE", relevant=True),
        "TP": AssessmentStateFactory.state(name="TP", relevant=False),
        "INVALID": AssessmentStateFactory.state(name="INVALID", relevant=False),
    }


class ExampleEvent(Event):
    """Example Event"""

    assessment_type = ExampleAssessment


class AnotherExampleEvent(Event):
    """Example Event"""

    assessment_type = ExampleAssessment


class YetAnotherEvent(Event):
    """Example Event"""

    assessment_type = ExampleAssessment


class ExampleTestStepCustom(CustomReportTestStep):
    """Test step customization."""

    def event(self, event: "Event", details: dict) -> str:
        """Custoize event."""
        return html_escape(f"Event: {event.id} -> {event.state.name}")

    def details(self, processing_details: ProcessingResult, teststep_result: TeststepResult) -> str:
        """Customizae details."""
        return html_escape(f"{teststep_result} -> {processing_details}")

    def overview(
        self,
        processing_details_list: ProcessingResultsList,
        teststep_result: List["TeststepResult"],
    ) -> str:
        """Customize overview."""
        return "<h3>TS Overview</h3>" + html_escape(f"# of results: {len(teststep_result)}.")


class ExampleTestCaseCustom(CustomReportTestCase):
    """Testcase customization."""

    def __init__(self):
        """Initialize the customization."""
        self._d = []

    def overview(self) -> str:
        """Build reporting details computed on all teststep results."""
        return str(self._d)

    def on_result(self, processing_details: Dict, teststep_result: "TeststepResult"):
        """Process details to aggregate data for the overview of the teststep.

        :param processing_details:
        :param teststep_result:
        """
        self._d.append(html_escape(f"{teststep_result} -> {processing_details}"))


@teststep_definition(
    1,
    "Count activations of signal A",
    "Example for counting an activation rate. Over more than a single input.",
    ExpectedResult(
        0.3,
        unit="1/km",
        numerator_is_events=True,
        operator=RelationOperator.LESS_OR_EQUAL,
        aggregate_function=AggregateFunction.KPI,
    ),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleAEBTestStep1(TestStep):
    """Example test step."""

    custom_report = ExampleTestStepCustom

    def process(self, **kwargs):
        """Count the activations (raising flanks on the mileag (integral of the velocity over time)."""
        # Get the read data frame
        exmpl = self.readers[EXAMPLE]

        # check for raising flanks
        flanks = exmpl[ExampleSignals.Columns.ACTIVATION_A].diff() > 0

        activations = exmpl.loc[flanks]
        for idx, row in activations.iterrows():
            e = ExampleEvent(start_timestamp=idx, end_timestamp=idx)
            self.result.add_event(e)

        td = exmpl[ExampleSignals.Columns.TS].diff() * 1e-6
        mileage = np.sum(exmpl[ExampleSignals.Columns.EGO_VELO] * td) / 1000

        # Store the result
        self.result.measured_result = Result(len(activations), mileage, unit="1/km")


@teststep_definition(
    2,
    "Count activations of signal B",
    "Example for counting an activation rate. Over more than a single input.",
    ExpectedResult(
        0.1,
        unit="1/km",
        operator=RelationOperator.GREATER,
        aggregate_function=AggregateFunction.KPI,
        numerator_is_events=True,
    ),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleAEBTestStep2(TestStep):
    """Example test step."""

    custom_report = ExampleTestStepCustom

    def process(self, **kwargs):
        """Count the activations (raising flanks on the mileag (integral of the velocity over time)."""
        # Get the read data frame
        exmpl = self.readers[EXAMPLE]

        # check for raising flanks Signal B
        flanks = exmpl[ExampleSignals.Columns.ACTIVATION_B].diff() > 0
        activations = exmpl.loc[flanks]
        for idx, row in activations.iterrows():
            e = AnotherExampleEvent(start_timestamp=idx, end_timestamp=idx)
            self.result.add_event(e)

        td = exmpl[ExampleSignals.Columns.TS].diff() * 1e-6
        mileage = np.sum(exmpl[ExampleSignals.Columns.EGO_VELO] * td) / 1000

        # Store the result
        self.result.measured_result = Result(denominator=mileage, unit="1/km", numerator_is_events=True)


@teststep_definition(
    3,
    "Count activations of signal A and D",
    "Example for counting an activation rate. Over more than a single input.",
    ExpectedResult(
        0.3,
        unit="1/km",
        numerator_is_events=True,
        operator=RelationOperator.LESS_OR_EQUAL,
        aggregate_function=AggregateFunction.KPI,
    ),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleAEBTestStep3(TestStep):
    """Example test step."""

    custom_report = ExampleTestStepCustom

    def process(self, **kwargs):
        """Count the activations (raising flanks on the mileag (integral of the velocity over time)."""
        # Get the read data frame
        exmpl = self.readers[EXAMPLE]

        # check for raising flanks Signal A
        flanks = exmpl[ExampleSignals.Columns.ACTIVATION_A].diff() > 0
        activations = exmpl.loc[flanks]
        for idx, row in activations.iterrows():
            e = ExampleEvent(start_timestamp=idx, end_timestamp=idx)
            self.result.add_event(e)

        # check for raising flanks Signal D
        flanks = exmpl[ExampleSignals.Columns.ACTIVATION_D].diff() > 0
        activations = exmpl.loc[flanks]
        for idx, row in activations.iterrows():
            e = YetAnotherEvent(start_timestamp=idx, end_timestamp=idx)
            self.result.add_event(e)

        td = exmpl[ExampleSignals.Columns.TS].diff() * 1e-6
        mileage = np.sum(exmpl[ExampleSignals.Columns.EGO_VELO] * td) / 1000

        # Store the result
        self.result.measured_result = Result(len(activations), mileage, unit="1/km")


@testcase_definition("EX_EBA_001_001", "KPI 1", "Example KPI Test implementation without events.")
@register_inputs("/SYSHADHA22/EBA/Usecase/CCRm_EV40_TV20_OVERLAP+50")
class ExampleKpiTestCase(TestCase):
    """Example test case."""

    custom_report = ExampleTestCaseCustom

    @property
    def test_steps(self):
        """Define the test steps."""
        return [ExampleAEBTestStep1, ExampleAEBTestStep2, ExampleAEBTestStep3]


@teststep_definition(
    1,
    "Activation check",
    "Usecase like example. Check that we have a activation in every input.",
    ExpectedResult(1.1, unit="s", operator=RelationOperator.GREATER_OR_EQUAL, aggregate_function=AggregateFunction.ALL),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleAEBTestStep1All1(TestStep):
    """Example test step."""

    def process(self, **kwargs):
        """Count the activations (raising flanks on the mileag (integral of the velocity over time)."""
        # Get the read data frame
        exmpl = self.readers[EXAMPLE]

        # check for raising flanks
        flanks = exmpl[ExampleSignals.Columns.BINARY_ACTIVATION_A].diff() > 0

        # Please note: This is a invalid oversimplification:
        #
        #  * We are not checking for more than a single activation
        #  * We do no check against the TTC
        #  * We do not validate the approach conditions
        #
        # But this is for example purposes what TSF will do not how proper test are implemented.
        activations = exmpl.loc[flanks]

        if activations.empty:
            # Store the result
            self.result.measured_result = Result(None, unit="s")  # No activation
        else:
            # Again, totally fake...
            self.result.measured_result = Result(1.2, unit="s")  # An activation


@teststep_definition(
    2,
    "Activation check 2",
    "Usecase like example. Check that we have a activation in every input.",
    ExpectedResult(0.7, unit="s", operator=RelationOperator.GREATER_OR_EQUAL, aggregate_function=AggregateFunction.ALL),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleAEBTestStep1All2(TestStep):
    """Example test step."""

    def process(self, **kwargs):
        """Count the activations (raising flanks on the mileag (integral of the velocity over time)."""
        # Get the read data frame
        exmpl = self.readers[EXAMPLE]

        # check for raising flanks
        flanks = exmpl[ExampleSignals.Columns.BINARY_ACTIVATION_B].diff() > 0

        # Please note: This is a invalid oversimplification:
        #
        #  * We are not checking for more than a single activation
        #  * We do no check against the TTC
        #  * We do not validate the approach conditions
        #
        # But this is for example purposes what TSF will do not how proper test are implemented.
        activations = exmpl.loc[flanks]

        if activations.empty:
            # Store the result
            self.result.measured_result = Result(None, unit="s")  # No activation
        else:
            # Again, totally fake...
            self.result.measured_result = Result(0.8, unit="s")  # An activation


@testcase_definition("EX_EBA_001_003", "KPI 3 (ALL)", "Example KPI Test with aggregation function all.")
@register_inputs("/SYSHADHA22/s3_reading_test")
class ExampleAllTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleAEBTestStep1All1,
            ExampleAEBTestStep1All2,
        ]
