#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn how to use KPI and ALL aggregation in expected results for endurance and usecase reports
respectively.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

TSF_BASE = os.path.abspath(os.path.join(__file__, "", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.common import AggregateFunction, RelationOperator
from tsf.core.results import ExpectedResult, Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.db.events import Event

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)


class ExampleEvent(Event):
    """Example Event"""

    pass


@teststep_definition(
    step_number=1,
    name="KPI",
    description="Example for counting an activation rate. Over more than a single input.",
    expected_result=[
        ExpectedResult(
            0.3,
            unit="1/km",
            numerator_is_events=True,
            operator=RelationOperator.LESS_OR_EQUAL,
            aggregate_function=AggregateFunction.KPI,
        ),
        ExpectedResult(
            0.5,
            unit="s",
            operator=RelationOperator.GREATER_OR_EQUAL,
            aggregate_function=AggregateFunction.KPI,
            project_name="TEST Development",
        ),
    ],
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleKPITestStep(TestStep):
    """Example test step."""

    def process(self, **kwargs):
        """Count the activations flanks on the mileage (integral of the velocity over time)."""
        # Get the read data frame
        example_signals = self.readers[EXAMPLE].signals

        # check for raising flanks
        raising_flanks = example_signals[ExampleSignals.Columns.ACTIVATION_A].diff() > 0

        activations = example_signals.loc[raising_flanks]
        for idx, row in activations.iterrows():
            e = ExampleEvent(start_timestamp=idx, end_timestamp=idx)
            self.result.add_event(e)

        td = example_signals[ExampleSignals.Columns.MTS_TS].diff() * 1e-6
        mileage = np.sum(example_signals[ExampleSignals.Columns.EGO_VELO] * td) / 1000

        # Store the result
        self.result.measured_result = Result(len(activations), mileage, unit="1/km")


@teststep_definition(
    step_number=2,
    name="Usecase",
    description="Usecase like example. Check that we have a activation in every input.",
    expected_result=[
        ExpectedResult(
            0.7, unit="s", operator=RelationOperator.GREATER_OR_EQUAL, aggregate_function=AggregateFunction.ALL
        ),
        ExpectedResult(
            0.81,
            unit="s",
            operator=RelationOperator.GREATER_OR_EQUAL,
            aggregate_function=AggregateFunction.ALL,
            project_name="TEST Development",
        ),
    ],
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleALLTestStep(TestStep):
    """Example test step."""

    def process(self, **kwargs):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(None, unit="s")  # No activation
            return

        self.result.measured_result = Result(0.8, unit="s")  # An activation with fake result


@verifies("req-001")
@testcase_definition(
    name="Testcase with endurance and usecase teststeps",
    description="An example with KPI teststep and another teststep with aggregation function all.",
)
class ExampleTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleKPITestStep,
            ExampleALLTestStep,
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
        [
            ExampleTestCase,
        ],
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
