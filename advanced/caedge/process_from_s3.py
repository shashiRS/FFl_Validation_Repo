import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.db.connect import ScopedConnectionProvider
from tsf.testbench._internals.runner import Config, LocalRunner
from tsf.testbench.report import report_locally


def main(workdir: str, **kwargs):
    workdir = Path(workdir)

    with open(workdir / "runner_s3_data.json", "r") as fp:
        d = json.load(fp)
    cfg = Config(**d)
    os.makedirs(cfg.temp_dir, exist_ok=True)

    cp = ScopedConnectionProvider(sqlite=workdir / "tsf.sqlite")

    r = LocalRunner(
        cfg,
        with_multiprocessing=False,
        with_reporting=True,
        cp=cp,
        check_inputs=True,
        testrun_update=True,
    )
    r.setup()

    cfg.add_itinearary_item(
        "Process locally",
        "-",
    )
    cfg.to_json(
        file=cfg.temp_dir / "run_spec.json",
        log_repo_revisions=True,
    )

    r.start_process_data()
    report_locally(
        cp,
        r.testrun_id,
        input_directories=[cfg.temp_dir],
        out_directory=cfg.temp_dir / "report",
        run_spec=cfg.temp_dir / "run_spec.json",
        redo_all=True,
        with_online_assessment=True,
        development_details=True,
    )


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-w", "--workdir", type=str, default=tempfile.mkdtemp())
    args.add_argument(
        "--with_bootstrap", action="store_true"
    )  # Pass this arg if you want the preparation for the processing of the report to take place
    namespace = args.parse_args()

    if namespace.with_bootstrap:
        from advanced.caedge.bootstrap_s3 import main as bootstrap_main

        bootstrap_main(**vars(namespace))

    main(**vars(namespace))
