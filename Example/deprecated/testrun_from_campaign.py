#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example for generating testruns from campaigns from CLS result service.

(Replaced by result download in tsf_execution_service)
"""

# TODO:
# - Sync the add_testcase_definition() with the resolving from testcase name (otherwise it will currently crash with more than one scenario per campaign if for each scenario a testcase is added)
# - modify the register_signal() to automatically take the right signal names from the corrensponding input (bsig / erg)

import argparse
import json
import logging
import os
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List

import requests
from tsf.core._internals.debugging_support import Bootstrap, open_directory_in_explorer
from tsf.core.common import (
    ExecutionState,
    PathSpecification,
    RelationalOperator,
    Resolve,
)
from tsf.core.results import ExpectedResult, Result
from tsf.core.testcase import TestCase, TestStep, register_inputs, register_signals
from tsf.db.collections import InputNature
from tsf.db.connect import DatabaseConnector, ScopedConnectionProvider
from tsf.io.erg import ErgSignalDefinition
from tsf.io.signals import SignalDefinition
from tsf.testbench._internals.config import Config
from tsf.testbench._internals.report import Report
from tsf.testbench._internals.runner import LocalRunner

_log = logging.getLogger(__name__)


CFG_FILE_NAME = "run_spec.json"
SQLITE_FILE_NAME = "my.sqlite"

PROJECT = "EXAMPLE PROJ"
SUT = "SW 00.00.00-INT1"
TEST_DISCIPLINE = "CLS"
COMPONENT = "EBA"

INPUT_SET_URL = "/foo"

EBA = "eba"
EBA_CARMAKER = "eba_carmaker"

# to start the result service, follow the instructions from https://github.8675.ccp.continental.exchange/caedge-simulation/clsim-result-srv
API_URL = "http://localhost:5003/api/"


class EbaSignals(SignalDefinition):
    """Signal mapping for EBA from bsig."""

    class Columns(SignalDefinition.Columns):
        """Definition of the dataframe columns."""

        PRE_BRAKE_DECELL = "pre_brake_decell"
        PRE_BRAKE_DECELL_ENABLED = "pre_brake_decell_enabled"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.PRE_BRAKE_DECELL: "ARS540 Device.AlgoSenCycle.MEDIC_PreBrakeMeas.fPreBrakeDecel",
            self.Columns.PRE_BRAKE_DECELL_ENABLED: (
                "ARS540 Device.AlgoSenCycle.MEDIC_PreBrakeMeas.bPreBrakeDecelEnabled"
            ),
        }


class EbaCarmakerSignals(ErgSignalDefinition):
    """Signal mapping for EBA from carmaker files."""

    class Columns(ErgSignalDefinition.Columns):
        """Definition of the dataframe columns."""

        PRE_BRAKE_DECELL_ENABLED = "pre_brake_decell_enabled"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.TIMESTAMP: "Time",
            self.Columns.PRE_BRAKE_DECELL_ENABLED: "_MEDIC.PreBrake.bPreBrakeDecelEnabled",
        }


class GeneralTs(TestStep):
    """Generic teststep for different input files."""

    step_number = 1
    expected_result = ExpectedResult(0, unit="%", operator=RelationalOperator.GREATER)
    description = "description"

    def get_brake_signals(self):
        """Get the relevant braking signals from the input file."""
        return None

    def process(self, **kwargs):
        """Calculate the fraction of active braking signal."""
        pre_brake_decell_enabled = self.get_brake_signals()
        brake_active = len(pre_brake_decell_enabled[pre_brake_decell_enabled > 0]) / pre_brake_decell_enabled.size
        self.result.measured_result = Result(brake_active * 100, unit="%")


@register_signals(EBA, EbaSignals)
class BsigTs(GeneralTs):
    """Specific teststep for bsig input files."""

    name = "BsigTs"

    def get_brake_signals(self):
        """Get the relevant braking signals from the input file."""
        eba = self.readers[EBA]
        pre_brake_decell_enabled = eba[EbaSignals.Columns.PRE_BRAKE_DECELL_ENABLED]
        return pre_brake_decell_enabled


@register_signals(EBA_CARMAKER, EbaCarmakerSignals)
class CarmakerTs(GeneralTs):
    """Specific teststep for carmaker input files."""

    name = "CarmakerTs"

    def get_brake_signals(self):
        """Get the relevant braking signals from the input."""
        eba = self.readers[EBA_CARMAKER]
        pre_brake_decell_enabled = eba[EbaCarmakerSignals.Columns.PRE_BRAKE_DECELL_ENABLED]
        return pre_brake_decell_enabled


@register_signals(EBA_CARMAKER, EbaCarmakerSignals)
class CarmakerTs2(CarmakerTs):
    """Second dummy teststep for testing purpose."""

    name = "CarmakerTs2"
    step_number = 2


@register_inputs(INPUT_SET_URL)
class BsigTC(TestCase):
    """Testcase for bsig input files."""

    name = "BsigTC"

    @property
    def test_steps(self):
        """Return teststeps."""
        return [BsigTs]


@register_inputs(INPUT_SET_URL)
class CarmakerTC(TestCase):
    """Testcase for carmaker input files."""

    name = "CarmakerTC"

    @property
    def test_steps(self):
        """Return teststeps."""
        return [CarmakerTs, CarmakerTs2]


def parse_campaign_info(campaign_info: Dict):
    """Parse the campaign details."""
    campaign_name = campaign_info["label"]
    scenario_urls = campaign_info["scenario_urls"]

    return campaign_name, scenario_urls


def parse_scenario_info(scenario_info: Dict):
    """Parse the scenario details."""
    scenario_name = scenario_info["name"]
    scenario_description = scenario_info["description"]
    scenario_properties = scenario_info["properties"]
    scenario_properties = dict(
        [list(map(str.strip, v.split("="))) for v in scenario_properties.strip().strip(";").split(";")]
    )
    scenario_result_url = scenario_info["result_url"]

    return scenario_name, scenario_description, scenario_properties, scenario_result_url


def parse_result_info(result_info: Dict):
    """Parse the result details."""
    file_types = result_info["file_types"]
    status = result_info["status"]
    abstract = result_info["abstract"]

    return file_types, status, abstract


def get_result_files(result_id: str, file_types: List[str], data_dir: str):
    """Request the download of the zipped result files and extract."""
    files = []
    for file_type in file_types:
        download_result_file = API_URL + f"result/{result_id}/{file_type}"
        response = requests.get(download_result_file)
        open(data_dir / f"{result_id}.zip", "wb").write(response.content)
        with zipfile.ZipFile(data_dir / f"{result_id}.zip", "r") as zip_ref:
            file_names = zip_ref.namelist()
            zip_ref.extractall(data_dir)

            for file_name in file_names:
                files.append(data_dir / file_name)
    return files


def create_config(
    working_dir: Path,
    cfg_path: Path,
    path_specs: List[PathSpecification],
    proj_name: str,
    pis_url: str,
    sut_name: str,
    disc_name: str,
    tr_name: str,
    tr_id: str,
    testcase: str,
):
    """Create and write the runner config file."""
    cfg = Config()
    cfg.temp_dir = working_dir
    cfg.testcase_names = [Resolve.as_fqn(testcase)]
    cfg.sut_discipline = disc_name
    cfg.project_name = proj_name
    cfg.processing_input_set_names = [pis_url]
    cfg.sut_name = sut_name
    cfg.testrun_name = tr_name
    cfg.testrun_id = tr_id
    cfg.path_specs = path_specs
    cfg.to_json(cfg_path)

    return cfg


def setup(working_dir: Path, sqlite_path: Path, cfg_path: Path, campaign_url: str, testcase: TestCase):
    """Request the campaign data and create the testrun out of it."""
    if sqlite_path.exists():
        os.unlink(sqlite_path)

    Bootstrap.offline_sqlite_db(sqlite_path)

    cp = ScopedConnectionProvider(sqlite=sqlite_path)
    with DatabaseConnector(cp) as dbc:
        proj = dbc.global_data.add_project(PROJECT, "-", "-")

        pis = dbc.processing_inputs.create_input_set(url=INPUT_SET_URL)

        sut = dbc.results.add_subject_under_test(SUT, proj)
        disc = dbc.results.add_test_discipline(TEST_DISCIPLINE)
        comp = dbc.results.add_component(COMPONENT)

        campaign_id = campaign_url.split("/")[-1]

        campaign_info = requests.get(campaign_url).json()
        campaign_name, scenario_urls = parse_campaign_info(campaign_info)

        if campaign_name == "":
            campaign_name = campaign_id

        data_dir = working_dir

        tr = dbc.results.add_testrun(campaign_name, sut, disc, pis)

        for scenario_url in scenario_urls:
            scenario_info = requests.get(scenario_url).json()
            scenario_name, scenario_description, scenario_properties, scenario_result_url = parse_scenario_info(
                scenario_info
            )
            scenario_id = scenario_url.split("/")[-1]

            result_info = requests.get(scenario_result_url).json()
            file_types, status, abstract = parse_result_info(result_info)
            result_id = scenario_result_url.split("/")[-1]

            files = get_result_files(result_id, file_types, data_dir)

            entries = []
            path_specs = []
            for file in files:
                if file.suffix != ".info":
                    c_input = dbc.processing_inputs.create_input(file, nature=InputNature.SCENARIO)
                    entries.append(c_input)
                    path_specs.append(PathSpecification(data_dir, extension=file.suffix))

            pis = dbc.processing_inputs.create_input_set(url=INPUT_SET_URL + "/" + scenario_id, entries=entries)

            assignment = dbc.results.add_assignment(None, collection=pis)

            tc_def = dbc.results.add_testcase_definition(
                scenario_name + "-" + testcase.name,
                scenario_description,
                scenario_name + "-" + testcase.name,
                component=comp,
                class_=testcase,
                assignments=[assignment],
            )

            for ts in testcase().test_steps:
                ts_spec_tag = tc_def.spec_tag + f"-{ts.step_number:02d}"
                dbc.results.add_teststep_definition(
                    tc_def, ts.name, ts.description, ts_spec_tag, ts.expected_result, class_=ts
                )

            dbc.results.add_testcase_result(tr, tc_def, state=ExecutionState.INITIAL)

            dbc.commit()

        cfg = create_config(
            working_dir, cfg_path, path_specs, proj.name, pis.url, sut.name, disc.name, tr.name, tr.id, testcase
        )

    return cp, cfg


def process(cp: DatabaseConnector, cfg: Config, testrun_update: bool):
    """Process the testrun."""
    with DatabaseConnector(cp) as dbc:
        r = LocalRunner(
            cfg,
            with_multiprocessing=False,
            with_reporting=True,
            debug_enabled=True,
            cp=cp,
            check_inputs=True,
            testrun_update=testrun_update,
        )

        r.input_collection = dbc.processing_inputs.get_input_set(url=cfg.processing_input_set_names[0])
        r.testrun = dbc.results.get_testrun(id=cfg.testrun_id)
        r.testrun_id = cfg.testrun_id
        r.test_discipline = dbc.results.get_test_discipline(name=cfg.sut_discipline)
        r.subject_under_test = dbc.results.get_subject_under_test(name=cfg.sut_name)
        r.project = dbc.global_data.get_project(name=cfg.project_name)

        r.start_process_data()

    return r.testrun_id


def create_report(working_dir: Path, cp: DatabaseConnector, testrun_id: str, redo: bool):
    """Create the report."""
    reports_path = working_dir / "report"
    output_directory = reports_path
    working_directory = reports_path / "wd"
    report = Report(
        testrun_id,
        output_directory,
        working_directory,
        run_spec=None,
        development_details=True,
        connection_provider=cp,
        redo_all=redo,
    )

    report.make_all()


def run_campaign(
    create_testrun: bool, working_dir: Path, sqlite_path: Path, cfg_path: Path, campaign_url: str, testcase: TestCase
):
    """Run the campaign."""
    if create_testrun:
        cp, cfg = setup(working_dir, sqlite_path, cfg_path, campaign_url, testcase)
        update = False
    else:
        cp = ScopedConnectionProvider(sqlite=sqlite_path)
        d = json.load(open(cfg_path, "r"))
        cfg = Config(**d)
        update = True

    tr_id = process(cp, cfg, update)
    create_report(working_dir, cp, tr_id, update)


def main(*args):
    """Call the campaign method with the setted arguments."""
    parser = argparse.ArgumentParser(description="Testrun from campaign")
    parser.add_argument("--working_dir", type=str, help="Path to the working directory.")
    parser.add_argument("--sqlite_path", type=str, help="Path to the sqlite db file.")
    parser.add_argument("--cfg_path", type=str, help="Path to the cfg file.")
    parser.add_argument("--create_testrun", action="store_true", help="If setted, a new testrun will be created.")
    parser.add_argument("--testcase", type=str, help="Testcase to be used (given as fully qualified name).")
    parser.add_argument("--campaign_id", type=str, help="ID for campaign request.")
    args = parser.parse_args(*args)

    if args.working_dir:
        working_dir = Path(args.working_dir)
        os.makedirs(working_dir, exist_ok=True)
    else:
        working_dir = Path(tempfile.mkdtemp("_tsf"))

    if args.sqlite_path:
        sqlite_path = Path(args.sqlite_path)
    else:
        sqlite_path = working_dir / SQLITE_FILE_NAME

    if args.cfg_path:
        sqlite_path = Path(args.cfg_path)
    else:
        cfg_path = working_dir / CFG_FILE_NAME

    create_testrun = args.create_testrun
    if create_testrun:
        if args.testcase:
            testcase = Resolve.type_from_string(args.testcase)
        else:
            raise Exception("Testcase name is needed for creating the testrun!")
        if args.campaign_id:
            campaign_url = API_URL + f"campaign/{args.campaign_id}"
        else:
            raise Exception("Campaign ID is needed for creating the testrun!")
    else:
        campaign_url = None
        testcase = None

    run_campaign(create_testrun, working_dir, sqlite_path, cfg_path, campaign_url, testcase)

    open_directory_in_explorer(working_dir)
    _log.info(f"working directory: {working_dir}")


if __name__ == "__main__":
    main()
