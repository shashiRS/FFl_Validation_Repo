#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example, you would learn how to create and customize statistics page and add elements to it.

These pages are used to provide the users an overview of the data processed in the report by aggregating it.

TRY IT OUT!
Just run the file.
"""
import logging
import os
import sys
import tempfile
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core._internals.processing_utils import ProcessingResult
from tsf.core.report import CustomReportStatistics
from tsf.core.testcase import (
    Statistics,
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.db.results import Result

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@teststep_definition(
    step_number=1,
    name="Check for some_activation_a",
    description="Example for checking the activation of 'some_activation_a' signal",
    expected_result="> 80 %",
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleActivation(TestStep):
    """Defined TestStep Class."""

    def __init__(self):
        """Init."""
        super().__init__()

    def process(self):
        """Process Data."""
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)]

        if len(activation) == 0:
            self.result.measured_result = Result(0, unit="%")
            self.result.details["Result"] = "Fail"
            self.result.details["Measured Result"] = 0
            return

        self.result.measured_result = Result(100.0, unit="%")
        self.result.details["Result"] = "Pass"
        self.result.details["Measured Result"] = 100


###################################################################
# Note: Here we define the custom reporting for statistic class ###
###################################################################
class CustomOverview(CustomReportStatistics):
    """Define the custom reporting for statistic class."""

    name = "Custom Overview"

    def overview(self) -> str:
        """Overview."""
        s = "<h3>You can fetch data from the report processing as shown below</h3>"
        for tcr in self._env.testrun.testcase_results:
            for ts_def in tcr.testcase_definition.teststep_definitions:
                pr_list = self.processing_details_for(ts_def)
                for i in range(len(pr_list)):
                    quantity = ProcessingResult.from_json(pr_list.processing_result_files[i]).details["Result"]
                    meas_res = ProcessingResult.from_json(pr_list.processing_result_files[i]).details["Measured Result"]
                    s += "Result of Test Run {} is : {}<br/>".format(ts_def.name, quantity)
                    s += "Measured Result is : {}%<br/><br/>".format(meas_res)

        s += "<h3>You can also add pie charts like the one below</h3>"
        df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
        df.loc[df["pop"] < 2.0e6, "country"] = "Other countries"  # Represent only large countries
        fig = px.pie(df, values="pop", names="country", title="Population of European continent")
        s += fig.to_html(full_html=False, include_plotlyjs=False)

        s += "<h3>You can also add bar charts like the one below</h3>"
        data_canada = px.data.gapminder().query("country == 'Canada'")
        fig = px.bar(data_canada, x="year", y="pop")
        s += fig.to_html(full_html=False, include_plotlyjs=False)

        s += "<h3>You can also add heatmaps like the one below</h3>"
        df = px.data.tips()
        fig = px.density_heatmap(df, x="total_bill", y="tip")
        s += fig.to_html(full_html=False, include_plotlyjs=False)

        s += "<h3>You can also add animations like the one below</h3>"
        df = px.data.gapminder()
        fig = px.scatter(
            df,
            x="gdpPercap",
            y="lifeExp",
            animation_frame="year",
            animation_group="country",
            size="pop",
            color="continent",
            hover_name="country",
            log_x=True,
            size_max=55,
            range_x=[100, 100000],
            range_y=[25, 90],
        )
        s += fig.to_html(full_html=False, include_plotlyjs=False)

        s += "<h3>You can also add 3d figures like the one below</h3>"
        import numpy as np

        np.random.seed(1)
        N = 70
        fig = go.Figure(
            data=[
                go.Mesh3d(
                    x=(70 * np.random.randn(N)),
                    y=(55 * np.random.randn(N)),
                    z=(40 * np.random.randn(N)),
                    opacity=0.5,
                    color="rgba(244,22,100,0.6)",
                )
            ]
        )

        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    nticks=4,
                    range=[-100, 100],
                ),
                yaxis=dict(
                    nticks=4,
                    range=[-50, 100],
                ),
                zaxis=dict(
                    nticks=4,
                    range=[-100, 100],
                ),
            ),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10),
        )
        s += fig.to_html(full_html=False, include_plotlyjs=False)

        return "<p>" + s + "</p>"


###################################################################
# Note: Here we define the statistics class #######################
###################################################################
@register_signals(EXAMPLE, ExampleSignals)
class StatisticsExample(Statistics):
    """Statistic Class Example."""

    custom_report = CustomOverview

    def process(self, **kwargs):
        """Process."""
        # in this we do nothing here, since we make stats on the teststep results...
        pass


@verifies("req-001")
@testcase_definition(
    name="Statistics reporting",
    description="The most basic TSF example with statistics page.",
)
class ExampleTestCase(TestCase):
    """Example TestCase Class."""

    @property
    def test_steps(self):
        """Test Steps."""
        return [
            ExampleActivation,
        ]


def main(data_folder: Path, temp_dir: Path = None, open_explorer=True):
    """Call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    test_bsigs = [data_folder / f"test_input_{k}.bsig" for k in range(3)]
    os.makedirs(data_folder, exist_ok=True)
    for b in test_bsigs:
        generate_bsig(b)

    debug(
        ExampleTestCase,
        *test_bsigs,
        temp_dir=temp_dir,
        open_explorer=open_explorer,
        statistics=StatisticsExample,
        kpi_report=False,
        dev_report=True,
    )
    _log.debug("All done.")


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))

    data_folder = working_directory / "data"
    out_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)
