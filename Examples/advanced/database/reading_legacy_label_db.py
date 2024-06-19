#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn to use legacy database labels for reports.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import List

import plotly.graph_objects as go
from tsf.core._internals.processing_utils import ProcessingResult, ProcessingResultsList
from tsf.core.report import CustomReportTestStep

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.common import AggregateFunction, RelationOperator
from tsf.core.results import ExpectedResult
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.db.labels import CameraProject, LabelFunction, LabelTables, ObjectLabelType
from tsf.db.results import Result, TeststepResult

from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class CustomTeststepReport(CustomReportTestStep):
    def overview(
        self,
        processing_details_list: ProcessingResultsList,
        teststep_result: List["TeststepResult"],
    ):
        s = "<h3>Additional Data</h3>"

        s += "<h3>You can also add pie charts like the one below</h3>"

        plot = {"labels": ["label_a", "label_b", "label_c"], "values": [1, 6, 10]}

        fig = go.Figure(data=[go.Pie(labels=plot["labels"], values=plot["values"])])
        s += fig.to_html(full_html=False, include_plotlyjs=False)
        return s

    def details(self, processing_details: ProcessingResult, teststep_result: "TeststepResult") -> str:

        s = ""
        df = processing_details.details["data"]
        if type(df) == list:
            pass
        else:
            s += "<h3>You can also add tables like the one below</h3>"
            s += df.to_html()
        return s


@teststep_definition(
    step_number=1,
    name="Radar objects",
    description="Check if cut-in labels are found",
    expected_result="> 0",
    # default AggregateFunction.KPI is used in expected result. As the radar recording has two cut-in-labels,
    # and we provide two input files to the test, the test step will pass. For three input files and less than
    # three cut-in labels, the test step would fail, although labels are read.
    # Better formulation of expected result would be AggregateFunction.MAX
)
@register_signals(EXAMPLE, ExampleSignals)  # signals are mandatory
class ReadRadarObjectLabelExample(TestStep):
    """Example for a testcase that uses labels from legacy database.
    The labels from the TSF legacy label db are represented as dataframes.
    """

    custom_report = CustomTeststepReport

    def process(self):
        _log.info("Processing test step ReadRadarObjectLabelExample")

        # The Label data from the TSF legacy label db are returned as pandas DataFrames.
        ###################################################################
        # Note: Here we fetch radar object labels with type CUTIN #########
        ###################################################################
        cutin_label = self.legacy_Labels.get_radar_object_labels(obj_label_type=ObjectLabelType.CUTIN)
        _log.info("Found {} rows.".format(cutin_label.shape[0]))
        x = cutin_label.groupby(cutin_label["label_id"]).ngroups
        _log.info("Found {} different cutin labels".format(x))
        # In this case the measured result is the number of found of cutin labels.
        self.result.measured_result = Result(x)
        # The result status is passed although only one of the inputs has cutin-labels, but it has two labels (x=2)
        self.result.details["data"] = cutin_label


@teststep_definition(
    step_number=2,
    name="Generic labels",
    description="Check if generic labels are found",
    expected_result=ExpectedResult(
        numerator=0,
        operator=RelationOperator.GREATER,
        aggregate_function=AggregateFunction.MIN,
    )
    # both, the radar and the camera recording have a generic label,
    # that's why default AggregateFunction.KPI does not have a failing impact on test status here
    # Better formulation of expected result would be AggregateFunction.MAX
)
@register_signals(EXAMPLE, ExampleSignals)  # signals are mandatory
class ReadGenericRadarLabelExample(TestStep):

    custom_report = CustomTeststepReport

    def process(self, **kwargs):
        _log.info("Processing test step ReadGenericRadarLabelExample")
        ###################################################################
        # Note: Here we fetch generic radar labels ########################
        ###################################################################
        generic_labels = self.legacy_Labels.get_generic_radar_labels()  # get all generic labels or use enum
        # use enum GenericLabelType to select only labels of a specific type
        # generic_labels is a pandas DataFrame
        _log.info(
            "Found {} generic labels".format(generic_labels.shape[0])
        )  # ['label_id' 'absts' 'label_state_name' 'value' 'label_type_name']
        self.result.measured_result = Result(generic_labels.shape[0])
        # measured result is the number of rows in dataframe generic_labels
        self.result.details["data"] = generic_labels


@teststep_definition(
    step_number=3,
    name="Camera objects",
    description="Check if OD labels for camera can be read",
    expected_result=ExpectedResult(
        numerator=0,
        numerator_is_events=False,
        aggregate_function=AggregateFunction.MAX,
        operator=RelationOperator.GREATER,
    )
    # more than zero items (rows) shall be found, thus AggregateFunction.MAX
    # exp. result: max(labels in all processed input files) > 0  !!!
    # In this test case only the camera recording has OD labels.
)
@register_signals(EXAMPLE, ExampleSignals)  # signals are mandatory
class ReadCameraObjectDetectionLabels(TestStep):

    custom_report = CustomTeststepReport

    def process(self, **kwargs):
        _log.info("Processing test step ReadCameraObjectDetectionLabels")
        ###################################################################
        # Note: Here we fetch camera labels for MFC camera project ########
        ###################################################################
        cam_labels = self.legacy_Labels.get_camera_labels(
            od_project=CameraProject.MFC525_TRUCK,
            od_tables=LabelTables.LDROI_PLUS_LDSS,
            label_function=LabelFunction.OBJECT_DETECTION,
        )  # returns two dataframes in a list for labels if ODTables.LDROI_PLUS_LDSS is selected
        # if ODTables.LDROI is selected only LDROI data (plus some CD data) as single dataframe is returned
        # if ODTables.LDSS is selected only LDSS data (plus some CD data) as single dataframe is returned
        ldroi_df = cam_labels[0]
        _log.info("Found {} rows for LDROI.".format(ldroi_df.shape[0]))
        ldss_df = cam_labels[1]
        _log.info("Found {} rows for LDSS.".format(ldss_df.shape[0]))
        self.result.measured_result = Result(numerator=ldroi_df.shape[0] + ldss_df.shape[0])
        self.result.details["data"] = cam_labels


@verifies("req-001")
@testcase_definition(
    name="Legacy Label DB Example",
    description="Shows how you can read labels from legacy database.",
)
class LabelDatabaseExample(TestCase):
    """
    Example for usage of the legacy label db with the TSF interface.
    In the following three types of objects are read out.
    """

    @property
    def test_steps(self):
        return [
            ReadRadarObjectLabelExample,
            ReadGenericRadarLabelExample,
            ReadCameraObjectDetectionLabels,
        ]


def main(temp_dir: Path = None, open_explorer=True):
    """Optional, call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    debug(
        LabelDatabaseExample,
        r"\\cw01.contiwan.com\root\Loc\lndp\didr2540\public_data\tsf_examples_data\2019.08.01_at_19.36.22_radar"
        r"-mi_528.bsig",
        # r"\\cw01.contiwan.com\root\Loc\lndp\didr2540\public_data\tsf_examples_data\2019.08.01_at_19.36.22_radar"
        # r"-mi_528.bsig",
        temp_dir=temp_dir,
        open_explorer=open_explorer,
        kpi_report=False,
        dev_report=True,
    )
    # The radar recording has two cut-in labels, one generic label and no camera OD label rows.
    # The camera recording has no cut-in labels, one generic label and many OD label rows in LDSS and in LDROI.
    _log.debug("All done.")


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))
    out_folder = working_directory / "out"

    main(temp_dir=out_folder, open_explorer=True)
