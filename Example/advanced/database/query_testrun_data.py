#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example we would learn to query and extract testrun results from the DB.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import pprint
import sys

import pandas as pd

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.db.connect import DatabaseConnector

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)

project_name = "ARS540BW11"
testrun_id = 7000


if __name__ == "__main__":

    ###################################################################
    # Note: Here we connect to the TSF database and fetch results #####
    ###################################################################
    with DatabaseConnector() as dbc:
        globals = dbc.global_data
        results = dbc.results

        project = globals.get_project(name=project_name)
        testrun = results.get_testrun(id=testrun_id)
        # also possible with other filters such as name, subject_under_test, test_discipline, project etc.

        results_of_interest = []

        # testcase_names
        for tc_res in testrun.testcase_results:
            tc_def = tc_res.testcase_definition

            row = {
                "Testcase ID": tc_def.spec_tag,
                "Testcase name": tc_def.name,
            }

            for ts_res in tc_res.teststep_results:
                ts_def = ts_res.teststep_definition
                ts_name = ts_def.name

                row["Recording"] = ts_res.entry_adapter.reference.file_path
                if ts_res.measured_result:
                    row[f"Status {ts_name}"] = (
                        ts_def.expected_result_for(project).compute_result_status(ts_res.measured_result)[1].name
                    )
                else:
                    row[f"Status {ts_name}"] = "No Data"

                row[f"Expected Results {ts_def.name}"] = ts_def.expected_result_for(project).as_dict
                row[f"Measured Results {ts_def.name}"] = ts_res.measured_result.as_dict
                results_of_interest.append(row)

        df = pd.DataFrame(results_of_interest)
        # you can export the dataframe to a csv also if required.
        # df.to_csv("export.csv", sep=";", decimal=",")

        pprint.pprint(results_of_interest)
