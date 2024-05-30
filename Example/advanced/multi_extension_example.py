#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example, you will learn how to create your own customer reader for your new data source and also read it
together with your bsigs.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict, List

import numpy as np

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.common import Artifact, PathSpecification, RelationOperator
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
from tsf.io.datamodel import SignalDataFrame
from tsf.io.generic import IReader, ISignalReader
from tsf.io.signals import SignalDefinition

from utilities.generate_data import generate_bsig, generate_bsig_multiple
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


###################################################################
# Note: Here is how you define your customer reader ###############
###################################################################
class MyCustomReader(IReader, ISignalReader):
    def __init__(self, filename: str, signal_definition: SignalDefinition, **kwargs):
        super().__init__(**kwargs)
        self.filename = filename
        self._defs = signal_definition

    @property
    def file_extensions(self) -> List[str]:
        return [".foo"]

    def open(self, use_regression_signal_mapping=False):
        """Opens the data source and prepares for reading."""
        pass

    def close(self):
        """Closes the data source."""
        pass

    @property
    def artifacts(self) -> List[Artifact]:
        return [Artifact(f, None, None) for f in self.filename]

    @property
    def signals(self) -> SignalDataFrame:
        """Returns read objects as subclassed pandas dataframe.

        :return: A object dataframe.
        """
        sdf = SignalDataFrame()
        sdf["new_column"] = range(1, 100)  # Adding some data to simulate data being read from the .foo file
        return sdf

    def signal_data(self, items: List[str]) -> Dict[str, np.array]:
        """Fetch list of signals in single call."""
        return {k: self._df[k].values for k in items}

    def __getitem__(self, item) -> np.array:
        """Expose the signal df.

        :return: Array
        """
        return self._df[item]


class AdditionalOutputs(SignalDefinition):
    """Example signal reading mapping for signals."""

    class Columns(SignalDefinition.Columns):
        FOO = "FOO"

    def __init__(self):
        super().__init__()

        self._root = None

        ###################################################################
        # Note: Here is how you can define signal list you want to read ###
        ###################################################################
        self._properties = {
            self.Columns.FOO: "Col1",
        }

        ###################################################################
        # Note: Here is how map the extension to your specific reader #####
        ###################################################################
        self._extension_map = {
            ".foo": MyCustomReader,
        }


@teststep_definition(
    step_number=1,
    name="Activation",
    description="Check for 'some activation'",
    expected_result=Result(operator=RelationOperator.GREATER_OR_EQUAL, numerator=100, unit="%"),
)
@register_signals(alias="FOO", definition=AdditionalOutputs)
@register_signals(EXAMPLE, ExampleSignals)
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

        foo = self.readers["FOO"]
        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) == 0 and not all(foo["new_column"]):
            self.result.measured_result = Result(0, unit="%")
            return

        self.result.measured_result = Result(100.0, unit="%")


@verifies("req-001")
@testcase_definition(
    name="Multi extension data",
    description="This example demonstrates how to read multi-extension data using custom readers.",
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
    os.makedirs(data_folder, exist_ok=True)
    test_recordings = [Path(rf"\\LUFS009X.li.de.conti.de\prj\RADAR\A\B\C\D\test_input_{k}.rrec") for k in range(3)]
    for rec in test_recordings:
        generate_bsig_multiple(data_folder, rec.stem + ".bsig")

    os.makedirs(data_folder / "foo", exist_ok=True)
    test_foo = [data_folder / "foo" / f"test_input_{k}.foo" for k in range(3)]

    for b in test_foo:
        generate_bsig(b)

    ###################################################################
    # Note: Here is how you can define the simulation output folders ##
    ###################################################################
    input_pathspecs = [
        PathSpecification(data_folder / "bin_data_1", prefix="", suffix="", extension=".bsig"),
        PathSpecification(data_folder / "bin_data_2", prefix="", suffix="", extension=".bsig"),
        PathSpecification(data_folder / "foo", prefix="", suffix="", extension=".foo"),
    ]

    debug(
        [
            ExampleMinimalTestCase,
        ],
        *test_recordings,
        input_pathspecs=input_pathspecs,
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
