#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example, you can learn how to use boolean as expected and measured results.

This DOESN'T work at moment.
NEEDS TO BE FIXED.
Check https://jira.auto.continental.cloud/browse/KPITSF-703 ticket for status.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.results import FALSE, TRUE, BooleanResult
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
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


@teststep_definition(
    step_number=1,
    name="Checks for a signal hold",
    description="Checks for a signal hold condition and if passed returns true as result",
    ###################################################################
    # Note: Here you can define a boolean result ######################
    ###################################################################
    expected_result=BooleanResult(TRUE),
)
@register_signals(alias=EXAMPLE, definition=ExampleSignals)
class BooleanResultTeststep(TestStep):
    """Boolean Test Step Class."""

    def process(self):
        """Process Data."""
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) > 0:
            ###################################################################
            # Note: Here we set the measured result as TRUE ###################
            ###################################################################
            self.result.measured_result = TRUE

        ###################################################################
        # Note: Here we set the measured result as FALSE ###################
        ###################################################################
        self.result.measured_result = FALSE


@verifies("req-001")
@testcase_definition(
    spec_tag="EXP_TC_100_001",  # Spec_tag attribute is deprecated, use instead URI decorator. (examples/docs/howto/uri.html).
    name="Example for boolean result",
    description="This example testcase demonstrate how to define, create and work with boolean results.",
)
class BooleanResultTestcase(TestCase):
    """Boolean TC class."""

    @property
    def test_steps(self):
        """Defined Test Steps."""
        return [
            BooleanResultTeststep,
        ]


def main(data_folder: Path, temp_dir: Path = None, open_explorer=True):
    """Call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    test_bsigs = [data_folder / f"test_input_{k}.bsig" for k in range(3)]
    os.makedirs(data_folder, exist_ok=True)
    for b in test_bsigs:
        generate_bsig(b)

    debug(
        BooleanResultTestcase,
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
