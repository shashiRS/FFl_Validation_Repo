#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn to use how to use wildcards in signal definitions.
Wildcards allow use to read all signals which match the string preceding and succeeding the wildcard.
We use "%" as a wildcard.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path


TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
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
from tsf.io.compliance import ComplianceProp


from utilities.generate_data import _make_activation_signal, _make_binary_signal, ExampleSignalsCompliance, generate_bsig_compliance

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ExampleSignals(ExampleSignalsCompliance):
    """Example signal reading mapping for EBA signals."""

    class Columns(ExampleSignalsCompliance.Columns):
        """Column defines."""

        ACTIVATIONS = "all_activations"
        ECU = "ecu_signal"
        SIL = "sil_signal"
        ACTIVATION_A = "some_activation_a"
        ACTIVATION_B = "some_activation_b"
        BINARY_ACTIVATION_A = "binary_activation_a"
        BINARY_ACTIVATION_B = "binary_activation_b"
        EGO_VELO = "ego_velo"
        SOME_SIG = "some_sig"
        SIG_A = "some_sig_a"
        SIG_B = "some_sig_b"
        SIG_X = "some_other_sig_x"

    def __init__(self):
        super().__init__()

        self._root = ["Example Signal Data 1%", "Example Signal Data 2"]

        self.index_offset = {
            "ecu": 10,
            "sil": 5
        }

        self._properties = {
            self.Columns.ECU: ComplianceProp(signals="ecu_signal", tolerance=[0, 0]),
            self.Columns.SIL: ComplianceProp(signals="sil_signal", tolerance=[0, 0]),
            self.Columns.SOME_SIG: ComplianceProp(signals=".some_sig_%", tolerance=[0.1, 0.05], expected_result="> 5")
        }


@teststep_definition(
    step_number=1,
    name="Check for some_activation_a",
    description="Example for checking the activation of 'some_activation_a' Signal",
    expected_result="> 80 %",
)
@register_signals("SIGNALS", ExampleSignals)
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

        ex = ExampleSignals()
        self.result.details['ecu_offset'] = ex.index_offset['ecu']
        self.result.details['sil_offset'] = ex.index_offset['sil']

        example_signals = self.readers["SIGNALS"].signals
        ecu_df = example_signals[ExampleSignals.Columns.ECU][ex.index_offset['ecu']:]
        sil_df = example_signals[ExampleSignals.Columns.SIL][ex.index_offset['sil']:]
        some_sig_a_activation = example_signals.loc[(example_signals[(ExampleSignals.Columns.SOME_SIG, "a")] != 0)]

        if len(some_sig_a_activation) == 0 and eval(str(len(some_sig_a_activation)) + ex.signal_properties[ExampleSignals.Columns.SOME_SIG].expected_result):
            self.result.measured_result = Result(0, unit="%")
            return

        self.result.measured_result = Result(100.0, unit="%")


@verifies("req-001")
@testcase_definition(
    name="Minimal example",
    description="Example KPI Test implementation without events.",
)
class ExampleMinimalTestCase(TestCase):
    """Example test case."""

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleActivation,
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
        generate_bsig_compliance(b)

    debug(
        [
            ExampleMinimalTestCase,
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
