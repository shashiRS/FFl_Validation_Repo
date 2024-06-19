#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example, we would learn how to side-load additional data while processing teststeps.

Here, we would side a CSV file while executing the teststep.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import shutil
import sys
import tempfile
from pathlib import Path
import random

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.common import PathSpecification
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_side_load,
    register_signals,
    testcase_definition,
    teststep_definition,
)
from tsf.core.utilities import debug
from tsf.db.results import Result
from tsf.io.sideload import CsvSideLoad
from tsf.misc.utilities import as_quoted_csv

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)


@teststep_definition(
    step_number=1,
    name="EXP_SideLoad 1",
    description="This example demonstrates how to side load data from the",
    expected_result="> 80 %",
)
@register_signals(EXAMPLE, ExampleSignals)
###################################################################
# Note: Here is how you register a side load data to teststep #####
###################################################################
@register_side_load(
    alias="RoadLabelRelative",
    side_load=CsvSideLoad,  # type of side loaders
    path_spec=PathSpecification(folder=os.path.join(TSF_BASE, "examples", "data", "road_labels"), extension=".csv")
    # Path specification to define which data to read glob-like to the given test inputs relative to the given input
    # data directory.
    # Here: Any csv from the given input folder.
    # If there are ambigious choices, it will report an error and end evaluation.
)
@register_side_load(
    alias="RoadLabelAbsolute",
    side_load=CsvSideLoad,  # type of side loaders
    path_spec=PathSpecification(
        folder=os.path.join(TSF_BASE, "examples", "data", "other_road_labels"),
        extension=".txt",
    )
    # Absolute path for the sideload.
)
class Exp1(TestStep):
    """Demonstrates the usage of sideloader."""

    def __init__(self):
        """Init."""
        super().__init__()

    def process(self):
        """Process data."""
        _log.debug("Starting processing...")
        df_r = self.side_load["RoadLabelRelative"]
        df_a = self.side_load["RoadLabelAbsolute"]

        if len(df_a) > 0 and len(df_r) > 0:
            self.result.measured_result = Result.from_string("100 %")


# Extend the CsvSideLoad call to define preprocessing for side loaders.
class CsvPreprocessSideLoad(CsvSideLoad):
    """A csv side loader with some preprocessing."""

    def __init__(self, filepath, **kwargs):
        """Initialize the CSV side loader."""
        super().__init__(filepath)

    @classmethod
    def preprocess(cls, filespec, recpath):
        """Generate CSV file if not exisiting."""
        file_name = Path(recpath).stem
        file = Path(f"{filespec.file_prefix}{filespec.folder}\\{file_name}{filespec.file_suffix}{filespec.extension}")
        if not file.exists():
            os.makedirs(Path(file).parent, exist_ok=True)
            with open(file, "w") as fp:
                fp.write(as_quoted_csv(["TS", "ASMT"]))

                for _ in range(random.randint(2, 10)):
                    fp.write(as_quoted_csv([random.random() * 1e6, "TP"]))


@teststep_definition(
    step_number=2,
    name="EXP_SideLoad 2",
    description="This example demonstrates how to side load data with preprocessing",
    expected_result="> 80 %",
)
@register_signals(EXAMPLE, ExampleSignals)
@register_side_load(
    alias="RoadLabelRelative",
    side_load=CsvPreprocessSideLoad, # type of side loaders
    path_spec=PathSpecification(folder=os.path.join(TSF_BASE, "examples", "data", "road_labels"), extension=".csv")
)
@register_side_load(
    alias="RoadLabelAbsolute",
    side_load=CsvPreprocessSideLoad,  # type of side loaders
    path_spec=PathSpecification(
        folder=os.path.join(TSF_BASE, "examples", "data", "other_road_labels"),
        extension=".txt",
    )
    # Absolute path for the sideload.
)
class Exp2(TestStep):
    """Demonstrates the usage of sideloader."""

    def __init__(self):
        """Init."""
        super().__init__()

    def process(self):
        """Process data."""
        _log.debug("Starting processing...")
        df_r = self.side_load["RoadLabelRelative"]
        df_a = self.side_load["RoadLabelAbsolute"]

        if len(df_a) > 0 and len(df_r) > 0:
            self.result.measured_result = Result.from_string("100 %")


@testcase_definition(
    spec_tag="EXP_000_005",  # Spec_tag attribute is deprecated, use instead URI decorator. (examples/docs/howto/uri.html).
    name="Side load example 1",
    description="Demonstrates the use of side loaders",
)
class ExpTc1(TestCase):
    """Example TC Class."""

    @property
    def test_steps(self):
        """Defined Test Steps."""
        return [
            Exp1,
            Exp2
        ]


def main(data_folder: Path = None, out_folder: Path = None, open_explorer=True):
    """Call to debug to setup debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    test_bsigs = [data_folder / f"test_input_{k}.bsig" for k in range(3)]
    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(out_folder, exist_ok=True)
    for b in test_bsigs:
        generate_bsig(b)

    debug(
        ExpTc1,
        *test_bsigs,
        temp_dir=out_folder,
        open_explorer=open_explorer,
        kpi_report=False,
        dev_report=True,
    )
    _log.debug("All done.")


if __name__ == "__main__":
    working_directory = Path(os.environ.get("TSF_TEMP_DIR", default=tempfile.mkdtemp("_tsf"))) / "side_load_example"
    shutil.rmtree(working_directory, ignore_errors=True)

    data_folder = working_directory / "data"
    out_folder = working_directory / "out"

    main(data_folder, out_folder)
