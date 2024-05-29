"""Same testcases as in the main but this time executed multiple times to generate 5 testruns.


"""
import argparse
import logging
import os
import random
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List

import numpy as np

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core._internals.debugging_support import Bootstrap
from tsf.core.common import PathSpecification
from tsf.db.connect import DatabaseConnector, ScopedConnectionProvider
from tsf.testbench._internals.config import Config

from utilities.generate_data import generate_bsig_multiple

_log = logging.getLogger(__name__)
np.random.seed(27)
random.seed(27)


def create_local_db(output_folder, projects: List[str], s3_urls: List[str]):
    sqlite_path = output_folder / "tsf.sqlite"
    Bootstrap.debugging_sqlite_db(sqlite_path, sync_globals=False)

    cp = ScopedConnectionProvider(sqlite=sqlite_path)
    with DatabaseConnector(cp) as dbc:

        for name in projects:
            dbc.global_data.add_project(name, "-", "-")
            dbc.processing_inputs.create_input_set(url=f"/{name}")

        input_entries = []
        for s3_url in s3_urls:
            e = dbc.processing_inputs.create_input(s3_url)
            input_entries.append(e)

        dbc.processing_inputs.create_input_set(url="/SYSHADHA22/s3_reading_test", entries=input_entries)

        dbc.commit()

    return cp


def main(workdir: str, **kwargs):
    """Create a localsql"""
    tmp = Path(workdir)
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)

    projects = [
        "Project_1",
        "Project_2",
        "SYSHADHA22",
        "Project_3",
    ]

    s3_rec_urls = [
        "s3://honda-datalake-drivedata-prj-dev/20201010093856_91/test_input_0.rrec",
        "s3://honda-datalake-drivedata-prj-dev/20201010093856_91/test_input_1.rrec",
        "s3://honda-datalake-drivedata-prj-dev/20201010093856_91/test_input_2.rrec",
    ]

    cp = create_local_db(tmp, projects, s3_rec_urls)

    with DatabaseConnector(cp) as dbc:
        pies = dbc.processing_inputs.get_input_set(url="/SYSHADHA22/s3_reading_test")

        for pie in pies.entries:
            base_dir = tmp / "local_bsig_data"
            os.makedirs(base_dir, exist_ok=True)
            generate_bsig_multiple(base_dir, f"{pie.stem}.bsig")

    cfg = Config()
    cfg.temp_dir = tmp / "processing"
    cfg.project_name = "SYSHADHA22"
    cfg.testrun_name = "CAEDGE Example"
    cfg.sut_discipline = "algo"
    cfg.sut_name = "000.000.001"
    cfg.processing_input_set_names = ["/SYSHADHA22"]
    cfg.testcase_names = [
        "caedge.examples.ExampleKpiTestCase",
        "caedge.examples.ExampleAllTestCase",
    ]
    cfg.path_specs = [
        PathSpecification(tmp / "local_bsig_data" / "bin_data_1", extension=".bsig"),
        PathSpecification(tmp / "local_bsig_data" / "bin_data_2", extension=".bsig"),
    ]
    cfg.to_json(tmp / "runner_local_data.json")

    cfg = Config()
    cfg.temp_dir = tmp / "processing_s3"
    cfg.project_name = "SYSHADHA22"
    cfg.testrun_name = "CAEDGE Example from S3"
    cfg.sut_discipline = "algo"
    cfg.sut_name = "000.000.001"
    cfg.processing_input_set_names = ["/SYSHADHA22"]
    cfg.testcase_names = [
        "caedge.examples.ExamplereportTestCase",
        "caedge.examples.ExampleAllTestCase",
    ]
    cfg.path_specs = [
        PathSpecification("s3://tsf-251/test-002/bin_data_1", extension=".bsig"),
        PathSpecification("s3://tsf-251/test-002/bin_data_2", extension=".bsig"),
    ]
    cfg.to_json(tmp / "runner_s3_data.json")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-w", "--workdir", type=str, default=tempfile.mkdtemp())
    namespace = args.parse_args()
    main(**vars(namespace))
