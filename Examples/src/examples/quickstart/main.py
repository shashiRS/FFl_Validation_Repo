#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quickstart example."""
import logging
import os
import sys
import tempfile
from pathlib import Path

from tsf.core.common import RelationOperator
from tsf.core.results import Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_generic_collection,
    register_signals,
    testcase_definition,
    teststep_definition,
)
from tsf.core.utilities import debug

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

ROOT_DIR = os.path.abspath(os.path.join(__file__, "../src/examples", ".."))
print(ROOT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)


@teststep_definition(
    step_number=1,
    name="Activation",
    description="Check for 'some activation'",
    expected_result=Result(operator=RelationOperator.GREATER_OR_EQUAL, numerator=100, unit="%"),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleTestStep(TestStep):
    """Example test step."""

    def process(self, **kwargs):
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")
            return

        activation_time = activation['ts'].iloc[0]
        self.result.measured_result = Result(100.0, unit="%")
        self.result.details["time"] = activation_time


@testcase_definition(
    "EX_EBA_000_001",
    "Example Usecase Test implementation",
    "This example demonstrates how to process carmaker erg files within the TSF test scripting framework.",
)
@register_generic_collection("Example ERG files", discipline="VSP")
class ExampleUsecaseTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [ExampleTestStep]


def main(temp_dir: Path = tempfile.mkdtemp(), open_explorer=True):
    # Entry point for debugging during development.
    test_bsigs = [os.path.join(temp_dir, "data", f"test_input_{k}.bsig") for k in range(2)]
    data_folder = os.path.join(temp_dir, "data")
    os.makedirs(data_folder, exist_ok=True)
    for b in test_bsigs:
        generate_bsig(b)
    debug(
        ExampleUsecaseTestCase,
        *test_bsigs,
        temp_dir=temp_dir,
        open_explorer=open_explorer,
    )


if __name__ == "__main__":
    main()
