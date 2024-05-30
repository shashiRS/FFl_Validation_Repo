#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn how to perform object association using some project bsigs and project specific
implementations in a teststep.

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
    register_object_list,
    register_reference_object_list,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.io.reference_objects import RtRangeObjectDefinition
from tsf.io.sensorics_objects import SensoricsObjectDefinition
from tsf.io.signals import SignalDefinition
from tsf.misc.association import GenericObjectAssociation

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


########################################################################################################################
# PROJECT SPECIFIC CODE ################################################################################################
########################################################################################################################
class ARS540BW11TpfObject(SensoricsObjectDefinition):
    """Example TPF object list mapping."""

    class Columns(SensoricsObjectDefinition.Columns):
        """Extended object properties which are not defined as default already.

        .. warning: TRY NOT TO OVERRIDE DEFAULTS FROM PARENT!
        """

        CLASSIFICATION = "classification"
        VREL_Y = "vrel_y"

    def __init__(self):
        super().__init__()

        # Signal root
        self._root = "SIM VFB ALL.TPF.TpObjectList.aObject"

        # Max number of objects / array size of TPF object list
        self._size = 99

        # Map signal column name to object property signal names.
        # Note : These signals are defined starting after the aObject[N] part
        # of signal names
        self._properties = [
            # Mappings for the **mandatory** defaults
            # General
            (self.Columns.MAINTENANCE_STATE, r".general.eMaintenanceState"),
            (self.Columns.DIST_X, r".kinematic.fDistX"),
            (self.Columns.DIST_Y, r".kinematic.fDistY"),
            (self.Columns.VREL_X, r".kinematic.fVrelX"),
            (self.Columns.POS_X0, r".shapePoints.aShapePointCoordinates[0].fPosX"),
            (self.Columns.POS_X1, r".shapePoints.aShapePointCoordinates[1].fPosX"),
            (self.Columns.POS_X2, r".shapePoints.aShapePointCoordinates[2].fPosX"),
            (self.Columns.POS_X3, r".shapePoints.aShapePointCoordinates[3].fPosX"),
            (self.Columns.POS_Y0, r".shapePoints.aShapePointCoordinates[0].fPosY"),
            (self.Columns.POS_Y1, r".shapePoints.aShapePointCoordinates[1].fPosY"),
            (self.Columns.POS_Y2, r".shapePoints.aShapePointCoordinates[2].fPosY"),
            # mapping for the additional signals
            # Note: Signal order is not relevant, but will be reflected in the
            # data frame column order...
            (self.Columns.CLASSIFICATION, r".classification.eClassification"),
            (self.Columns.VREL_Y, r".kinematic.fVrelY"),
        ]


class EBASimOutputs(SignalDefinition):
    """Example signal reading mapping for EBA signals."""

    class Columns(SignalDefinition.Columns):
        PB_ENABLE = "PREBRAKE_ENABLE"
        PB_ACTIVE_HYP = "PREBRAKE_ACTIVE_HYP"
        HYP_CRITICAL_ITEM_ID = "HYP_CRITICAL_ITEM_ID"

    def __init__(self):
        super().__init__()

        self._root = "SIM VFB ALL.AlgoSenCycle"

        self._properties = [
            # Mappings for the **mandatory** columns and signals
            (
                self.Columns.PB_ENABLE,
                ".MEDIC_PreBrakeMeas.bPreBrakeDecelEnabled",
            ),
            (
                self.Columns.PB_ACTIVE_HYP,
                ".MEDIC_PreBrakeMeas.HypInfo.uActiveHyp",
            ),
            (
                self.Columns.HYP_CRITICAL_ITEM_ID,
                ".ACDC2_HypothesisMeas.Hypothesis[%].CriticalItem.i_itemID",
            ),
        ]


########################################################################################################################
########################################################################################################################
########################################################################################################################


c_eba = EBASimOutputs.Columns
c_tpf = ARS540BW11TpfObject.Columns
c_rt = RtRangeObjectDefinition.Columns


class MyRtRangeObjectDefinition(RtRangeObjectDefinition):
    def __init__(self):
        super().__init__()
        self._check_approaches = False  # Only set it to TRUE if you have a single recording with multiple approaches


@teststep_definition(
    step_number=1,
    name="Perform object association with TPF objects",
    description="Read EBA signals, TPF objects and RT-Range objects.",
    expected_result="= 100 %",
)
@register_signals("EBA", definition=EBASimOutputs)
@register_object_list("TPF", definition=ARS540BW11TpfObject)
@register_reference_object_list("RT", definition=MyRtRangeObjectDefinition)
class ReferenceReadingStep(TestStep):
    def process(self, **kwargs):
        ttc_pass = 2.1  # requirement from project

        # Default results is failed:
        self.result.measured_result = Result(0, unit="%")

        eba = self.readers["EBA"].signals  # reading signals

        # Account for TPF shift wrt to RT reference data
        tpf = self.readers["TPF"].objects
        tpf["orig_x"] = tpf[ARS540BW11TpfObject.Columns.DIST_X]
        tpf[ARS540BW11TpfObject.Columns.DIST_X] = tpf[ARS540BW11TpfObject.Columns.DIST_X] - 3.075 - 0.87

        rt = self.readers["RT"].objects  # reading signals

        # Check for desired activation
        activation = eba.loc[eba[c_eba.PB_ENABLE] != 0]
        if activation.empty:
            # Nothing more we can do since there was no activation
            return

        _log.debug("Starting to check activation in time or not")
        a0 = activation.iloc[0]
        a0_ts = a0[c_eba.MTS_TS]
        a0_active_hyp = a0[c_eba.PB_ACTIVE_HYP]
        a0_tpf_track_idx = a0[(c_eba.HYP_CRITICAL_ITEM_ID, a0_active_hyp)]

        ###################################################################
        # Note: Here we perform generic object association ################
        ###################################################################
        goa = GenericObjectAssociation()
        tpf, rt = goa.associate(tpf, rt)

        # Get the tsf index
        tsf_idx = tpf.loc[
            (tpf[c_tpf.MTS_TS] == a0_ts) & (tpf[c_tpf.TRACK] == a0_tpf_track_idx),
            c_tpf.TSF_INDEX,
        ].values[0]

        tsf_hyp_obj = tpf[tpf[c_tpf.TSF_INDEX] == tsf_idx]

        if any(~tsf_hyp_obj["matched_to"].isna()):
            # if positive match of object took place
            long_ttc = rt.loc[rt[c_rt.MTS_TS] <= a0_ts, c_rt.LONG_TTC].values[-1]
            long_ttc_a = rt.loc[rt[c_rt.MTS_TS] <= a0_ts, c_rt.LONG_TTC_A].values[-1]
            long_range = rt.loc[rt[c_rt.MTS_TS] <= a0_ts, c_rt.LONG_RANGE].values[-1]

            self.result.details["long_ttc"] = long_ttc  # saving additional information to json
            self.result.details["long_ttc_a"] = long_ttc_a  # saving additional information to json
            self.result.details["long_range"] = long_range  # saving additional information to json
            self.result.measured_result = Result(50, unit="%")

            if long_ttc >= ttc_pass:
                self.result.measured_result = Result(100, unit="%")


@verifies("req-001")
@testcase_definition(
    name="RT range testcase",
    description="This example demonstrates how to assign RT Range data to a teststep and perform object association.",
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
        r"\\cw01.contiwan.com\root\Loc\lndp\didr2540\public_data\tsf_examples_data\bin_data_60\2020.02.20_at_11.03"
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
