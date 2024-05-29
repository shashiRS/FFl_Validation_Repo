"""Same testcases as in the main but this time executed multiple times to generate 5 testruns.


"""
import json
import logging
import os
import random
import shutil
import string
import sys
import uuid
from pathlib import Path
from typing import List

import numpy as np

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core._internals.debugging_support import Bootstrap
from tsf.core.common import PathSpecification
from tsf.db.collections import InputNature
from tsf.db.connect import DatabaseConnector, ScopedConnectionProvider
from tsf.testbench._internals.config import Config
from tsf.testbench._internals.runner import LocalRunner
from tsf.testbench.report import report_locally

from utilities.generate_data import generate_testrun_data

_log = logging.getLogger(__name__)
np.random.seed(27)
random.seed(27)


def create_local_db(output_folder, projects: List[str], data_folder: Path):
    sqlite_path = output_folder / "tsf.sqlite"
    Bootstrap.debugging_sqlite_db(sqlite_path, sync_globals=False)

    cp = ScopedConnectionProvider(sqlite=sqlite_path)
    with DatabaseConnector(cp) as dbc:

        for name in projects:
            dbc.global_data.add_project(name, "-", "-")
            dbc.processing_inputs.create_input_set(url=f"/{name}")

        ctr = 1
        for name in projects:
            for j in range(3):
                entries = []
                for k in range(random.randint(15, 25)):
                    rec_dir = "/" + "/".join(["".join(random.choices(string.ascii_uppercase, k=3)) for _ in range(10)])
                    rec_name = f"/test_input_{ctr:04d}.rrec"
                    ctr += 1
                    c_input = dbc.processing_inputs.create_input(rec_dir + rec_name, nature=InputNature.RECORDING)
                    entries.append(c_input)

                dbc.processing_inputs.create_input_set(f"/{name}/example_{j}", entries)

        dbc.commit()

        # Debug: Dump all the processing inputs
        # # -------------------------------------
        # def p_coll(c: ProcessingInputSet, d=0):
        #     if not c.is_leaf:
        #         print(" " * d, c)
        #         for c1 in c.children:
        #             p_coll(c1, d + 1)
        #     else:
        #         print(" " * d, c)
        #         for e in c.entries:
        #             print(" " * (d + 1), e)
        #
        # for name in projects:
        #     c = dbc.processing_inputs.get_input_set(url=f"/{name}")
        #     p_coll(c)

    cfg = Config()
    cfg.temp_dir = output_folder
    cfg.testcase_names = [
        "kpi_rates.main.ExampleKpiTestCase",
        "kpi_rates.main.ExampleAllTestCase",
    ]
    cfg.testrun_name = "KPI RUN"
    cfg.sut_discipline = "ALGO"
    cfg.to_json(output_folder / "base_run_spec.json")

    return cp


def make_testrun(
    sut_name: str, project_name: str, output_folder: Path, data_folder: Path, cp: ScopedConnectionProvider
):
    tr_data = data_folder / f"tmp_{project_name}_{sut_name}"
    os.makedirs(tr_data, exist_ok=True)

    temp_dir = output_folder / f"tmp_{project_name}_{sut_name}"
    os.makedirs(temp_dir, exist_ok=True)

    with open(output_folder / "base_run_spec.json", "r") as fp:
        d = json.load(fp)
    cfg = Config(**d)
    cfg.project_name = project_name
    cfg.processing_input_set_names = [f"/{project_name}"]
    cfg.sut_name = sut_name
    cfg.testrun_name = f"Testrun {uuid.uuid4()}"
    cfg.path_specs = [PathSpecification(tr_data)]
    cfg.temp_dir = temp_dir
    cfg.to_json(output_folder / f"{project_name}_{sut_name}_run_spec.json")

    generate_testrun_data(tr_data, cfg.processing_input_set_names, cp)

    r = LocalRunner(
        cfg,
        with_multiprocessing=False,
        with_reporting=True,
        cp=cp,
        check_inputs=True,
    )
    r.setup()

    cmd = " ".join(sys.argv)
    cfg.add_itinearary_item(
        "Process locally",
        cmd,
    )
    cfg.to_json(
        file=os.path.join(cfg.temp_dir, "run_spec.json"),
        log_repo_revisions=True,
    )

    r.start_process_data()
    report_locally(
        cp,
        r.testrun_id,
        input_directories=[temp_dir],
        out_directory=temp_dir / "report",
        run_spec=temp_dir / "run_spec.json",
        redo_all=True,
    )

    report_locally(
        cp,
        r.testrun_id,
        input_directories=[temp_dir],
        out_directory=temp_dir / "report",
        run_spec=temp_dir / "run_spec.json",
        redo_all=True,
    )


if __name__ == "__main__":
    tmp = Path(r"d:\temp\rprt")  # Path(tempfile.mkdtemp("_tsf"))
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)

    bsig_dir = tmp / "data"
    shutil.rmtree(bsig_dir, ignore_errors=True)
    os.makedirs(bsig_dir, exist_ok=True)

    projects = [
        "Project_1",
        "Project_2",
        "Project_3",
    ]

    cp = create_local_db(tmp, projects, bsig_dir)

    make_testrun("SUT_1", "Project_1", tmp, bsig_dir, cp)
    make_testrun("SUT_2", "Project_1", tmp, bsig_dir, cp)
    make_testrun("SUT_2", "Project_1", tmp, bsig_dir, cp)
    make_testrun("SUT_2", "Project_1", tmp, bsig_dir, cp)

    make_testrun("SUT_1", "Project_2", tmp, bsig_dir, cp)
    make_testrun("SUT_1", "Project_2", tmp, bsig_dir, cp)
