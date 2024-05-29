#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read Recording Example."""
import logging
import os
import sys
from typing import List, Type

from tsf.io.signals import SignalDefinition

TSF_BASE = os.path.abspath(os.path.join(__file__, "../quarantine/legacy", "..", "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core.common import AggregateFunction, RelationOperator
from tsf.core.results import ExpectedResult, Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    register_versioned_collection,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2021, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
""" To be used with new RecordingReader from TSF 1.1
Preconditions:
- .NET Core v3.1 or higher installed
- pythonnet v3.0 or higher installed in used Python installation
"""


class MySignalDefinition(SignalDefinition):
    """Signal Definition Class."""

    class Columns(SignalDefinition.Columns):
        """Definition of column names for recording dataframe."""

        DRIVER_ATTENTION_STATE = "driver_attention_state"
        PREBRAKE_STANDSTILL_REQ = "prebrake_standstill_request"
        CYCLE_COUNTER = "cycle_counter"
        BRIGHTNESS_STATE = "brightness_state"
        LANE_QUALITY = "lane_quality"
        DRIVER_HANDS_OFF = "driver_hands_off"
        GEAR_POS = "gear_pos"
        HEATING_ACTIVATION_REQUEST = "heating_activation_request"
        CRC_OBJECT_DETECTION = "crc_object_detection"
        LIGHT_STYLE_4 = "light_style_4"
        RT_REL_HEADING = "rt_rel_heading"
        GPS_SPEED = "gps_speed"

    def __init__(self):
        """Init."""
        super().__init__()
        self._properties = [
            (
                self.Columns.DRIVER_ATTENTION_STATE,
                "MFC5xx Device.FCTVehicle.pDIMOutputCustom.eDriverAttentionState",
            ),
            (
                self.Columns.PREBRAKE_STANDSTILL_REQ,
                "MFC5xx Device.FCTVehicle.pHEADOutputCustom.sPreBrake.bPreBrakeStdstillRequest",
            ),
            (
                self.Columns.CYCLE_COUNTER,
                "MFC5xx Device.FCTVehicle.pHEADOutputGeneric.sSigHeader.uiCycleCounter",
            ),
            (
                self.Columns.BRIGHTNESS_STATE,
                "MFC5xx Device.HLA.RTE_HLAF_HeadlightControl.Common.BrightnessState",
            ),
            (
                self.Columns.LANE_QUALITY,
                "MFC5xx Device.LD.ABDLaneData.asLaneBoundary[0:9].sStatus.iQuality"
                # array signal with slices, signal_url shall have [first_index : last_index] for all needed array
                # elements. If you don't need the whole array you can specify something like ...[2:3]...
            ),
            (
                self.Columns.GEAR_POS,
                "Vehicle_CAN_Ford.FORD_FOCUS_Y2018_CGEA1_3_CMDB_B_v18_07__HS2.PowertrainData_10_HS2.GearPos_No_Cs",
            ),
            (
                self.Columns.CRC_OBJECT_DETECTION,
                "ADAS_Local_Private_CAN.ADAS_Private_Bus_LRR_CAM_MFC500.ObjectListChecksum.CRC_ObjectDetection",
            ),
            (
                self.Columns.HEATING_ACTIVATION_REQUEST,
                "ADAS_Global_CAN_FD.ADAS_CAN_FD_V1.CamBlockage.HeatingActivationRequest",
            ),
            (
                self.Columns.LIGHT_STYLE_4,
                "ADAS_Global_CAN_FD.ADAS_CAN_FD_V1.HeadlightState_GFA_0_4.LightStyle_Lt_4",
            ),
            (self.Columns.RT_REL_HEADING, "Ethernet RT-Range.Target01.RelativeToHunter.RelativeHeading_rad"),
            (self.Columns.GPS_SPEED, "GPS_Device.Speed"),
        ]


@teststep_definition(
    step_number=1,
    name="RecordingReader-TS",
    description="check if recording can be read",
    expected_result=ExpectedResult(
        numerator=0,
        operator=RelationOperator.GREATER,
        aggregate_function=AggregateFunction.MAX,
    ),
    doors_url="none",
)
@register_signals(
    alias="rec",
    definition=MySignalDefinition,
    project="MFC5xx",
    custom_reader_hook=None,
    discipline="SystemTest",
)
class RecordingReaderTestStep(TestStep):
    """Recording Reader Test Step Class."""

    def __init__(self):
        """Init."""
        super().__init__()

    def process(self, **kwargs):
        """Process Data."""
        _log.debug("Start processing RecordingReaderTestStep")
        rec_signals = self.readers["rec"]
        lane_quality_1 = rec_signals[(MySignalDefinition.Columns.LANE_QUALITY, 1)]
        _log.info("Length of lane_quality_1: {}".format(len(lane_quality_1)))
        size = rec_signals.shape
        _log.debug("Read {} rows and {} columns".format(size[0], size[1]))
        self.result.measured_result = Result(numerator=size[0])
        pass


@testcase_definition(
    spec_tag="TSF-spec-00x-00y",  # Spec_tag attribute is deprecated, use instead URI decorator. (examples/docs/howto/uri.html).
    name="ReadRecording",
    description="check if recording can be read",
    doors_url="-",
)
@verifies(requirement="TSF shall be able to read recordings", doors_url="none")
@register_versioned_collection(collection_path="versioned_example_collection")
class RecordingReaderTestCase(TestCase):
    """Recording Reader TC Class."""

    def __init__(self):
        """Init."""
        super().__init__()

    @property
    def test_steps(self) -> List[Type["TestStep"]]:
        """Defined Test Steps."""
        return [RecordingReaderTestStep]


if __name__ == "__main__":
    debug(
        RecordingReaderTestCase,
        os.path.join(
            TSF_BASE,
            "examples",
            "data",
            "recordings",
            "2019.08.21_at_15.07.55_camera-mi_503.rrec",
        ),
    )
    _log.debug("Finished")
