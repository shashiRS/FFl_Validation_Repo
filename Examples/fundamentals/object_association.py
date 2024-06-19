#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn how to perform object association using some project bsigs and project specific
implementations.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)


from tsf.io.reference_objects import RtRangeObjectDefinition, RtRangeObjectsReader
from tsf.io.sensorics_objects import SensoricObjectsReader, SensoricsObjectDefinition
from tsf.misc.association import GenericObjectAssociation

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class MyRtRangeObjectDefinition(RtRangeObjectDefinition):
    def __init__(self):
        super().__init__()
        self._check_approaches = False


#######################################################################
# PROJECT SPECIFIC CODE ###############################################
#######################################################################
class ARS540BW11TpfObject(SensoricsObjectDefinition):
    """Example TPF object list mapping."""

    class Columns(SensoricsObjectDefinition.Columns):
        """Extended object properties which are not defined as default already.

        .. warning: TRY NOT TO OVERRIDE DEFAULTS FROM PARENT!
        """

        # Clasification
        OBJ_CLASSIFICATION = "object_classification"
        # Dynamic Property
        OBJ_DYNAMIC_PROPERTY = "obj_dynamic_property"
        # qualifiers
        OBJ_PROB_OF_EXISTENCE = "obj_probability_of_existence"

        # Kinematics
        # TPF object attributes
        OBJ_ABS_ACCELERATION_X = "object_abs_accel_x"
        OBJ_ABS_ACCELERATION_Y = "object_abs_accel_y"

        OBJ_DISTANCE_X = "dist_x"
        OBJ_DISTANCE_Y = "dist_y"

        OBJ_ABS_VELOCITY_X = "obj_abs_velocity_x"
        OBJ_ABS_VELOCITY_Y = "obj_abs_velocity_y"

        OBJ_REL_VELOCITY_X = "obj_rel_velocity_x"
        OBJ_REL_VELOCITY_Y = "obj_rel_velocity_y"

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
            # Dynamic Property
            (self.Columns.OBJ_DYNAMIC_PROPERTY, r".dynamicProperty.eDynamicProperty"),
            # Kinematics
            (self.Columns.OBJ_ABS_ACCELERATION_X, ".kinematic.fAabsX"),
            (self.Columns.OBJ_ABS_ACCELERATION_Y, ".kinematic.fAabsY"),
            (self.Columns.OBJ_DISTANCE_X, ".kinematic.fDistX"),
            (self.Columns.OBJ_DISTANCE_Y, ".kinematic.fDistY"),
            (self.Columns.OBJ_ABS_VELOCITY_X, ".kinematic.fVabsX"),
            (self.Columns.OBJ_ABS_VELOCITY_Y, ".kinematic.fVabsY"),
            (self.Columns.OBJ_REL_VELOCITY_X, ".kinematic.fVrelX"),
            (self.Columns.OBJ_REL_VELOCITY_Y, ".kinematic.fVrelY"),
            # Classification
            (self.Columns.OBJ_CLASSIFICATION, ".classification.eClassification"),
        ]


if __name__ == "__main__":

    filenames = [
        r"\\cw01.contiwan.com\root\Loc\lndp\didr2540\public_data\tsf_examples_data\bin_data_20\2020.02.20_at_11.03"
        r".48_radar-mi_630.bsig",
        r"\\cw01.contiwan.com\root\Loc\lndp\didr2540\public_data\tsf_examples_data\bin_data_60\2020.02.20_at_11.03"
        r".48_radar-mi_630.bsig",
    ]

    rt_rdr = RtRangeObjectsReader(filenames, MyRtRangeObjectDefinition())
    rt_rdr.open()

    tpf_rdr = SensoricObjectsReader(filenames, ARS540BW11TpfObject())
    tpf_rdr.open()

    rt = rt_rdr.objects
    tpf = tpf_rdr.objects

    ###################################################################
    # Note: Here we perform generic object association ################
    ###################################################################
    goa = GenericObjectAssociation()
    tpf, rt = goa.associate(tpf, rt)

    # have a look at the matched_to column:
    if any(~tpf["matched_to"].isna()):
        print("Positive match with TPF object.")
    if any(~rt["matched_to"].isna()):
        print("Positive match with RT object.")

    print("Thats it.")
