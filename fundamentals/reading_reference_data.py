#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn how you can use RT range definition from TSF to read RT range from a bsig.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.results import DATA_NOK, Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_reference_object_list,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.io.reference_objects import RtRangeObjectDefinition

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


###################################################################
# Note: If you want to use TSF defined signal definition ##########
###################################################################
class MyRtRangeObjectDefinition(RtRangeObjectDefinition):
    def __init__(self):
        super().__init__()
        self._check_approaches = False  # Only set it to TRUE if you have a single recording with multiple approaches


@teststep_definition(
    step_number=1,
    name="Read reference data",
    description="Read RT-Range signals and objects.",
    expected_result="= 100 %",
)
@register_reference_object_list("RT", definition=MyRtRangeObjectDefinition)
class ReferenceReadingStep(TestStep):
    def process(self, **kwargs):
        self.result.measured_result = Result(0, unit="%")

        rt = self.readers["RT"].objects

        rt_ttc = None
        ego_velocity = None
        try:
            rt_ttc = pd.Series(rt.as_plain_df["long_ttc"].values, index=rt.as_plain_df["mts_ts"].values)
            ego_velocity = pd.Series(rt.as_plain_df["ego_velocity"].values, index=rt.as_plain_df["mts_ts"].values)
        except Exception as ex:
            _log.warning(f"Exception: {ex}")
            self.result.measured_result = DATA_NOK

        if rt_ttc is not None and ego_velocity is not None:
            self.result.measured_result = Result(100, unit="%")


@verifies("req-001")
@testcase_definition(
    name="RT range testcase",
    description="This example demonstrates how to assign RT Range data to a teststep.",
)
class ReferenceReadingExample(TestCase):
    @property
    def test_steps(self):
        """Define the test steps."""
        return [ReferenceReadingStep]


def main(temp_dir: Path = None, open_explorer=True):
    """Optional, call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    debug(
        ReferenceReadingExample,
        r"\\cw01.contiwan.com\root\Loc\lndp\didr2540\public_data\tsf_examples_data\bin_data_20\2020.02.20_at_11.03"
        r".48_radar-mi_630.bsig",
        temp_dir=temp_dir,
        open_explorer=open_explorer,
        kpi_report=False,
        dev_report=True,
    )
    _log.debug("All done.")


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))
    out_folder = working_directory / "out"
    main(temp_dir=out_folder, open_explorer=True)
