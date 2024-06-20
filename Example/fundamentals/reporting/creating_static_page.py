#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""In this example, you would learn how to create and customize a static page and add elements to it.

You can use these kinds of pages to help users of a report can use to look for references. Such as formulas, pictures,
graphs or animations.

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

from tsf.core.testcase import (
    CustomReportStaticReportContents,
    StaticReportContents,
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
            return

        self.result.measured_result = Result(100.0, unit="%")


###################################################################
# Note: Here we define custom reporting for the static page class #
###################################################################
class StaticPageReportClass(CustomReportStaticReportContents):
    """Example static page."""

    name = "Static Page"

    def overview(self) -> str:
        """Overview."""
        s = "<h3>You can formulas as shown below</h3>"
        s += """
        √(a² + b²) <br/>
        d = √(x2 − x1)² + (y2 − y1)²
        """
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
# Note: Here we define the static page class ######################
###################################################################
class StaticPageClass(StaticReportContents):
    """Example static page."""

    custom_report = StaticPageReportClass


@verifies("req-001")
@testcase_definition(
    name="Static page reporting",
    description="The most basic TSF example with a static page.",
)
class ExampleTestCase(TestCase):
    """Defined TestCase Class."""

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
        static_report_contents=StaticPageClass,
        temp_dir=temp_dir,
        open_explorer=open_explorer,
        kpi_report=False,
        dev_report=True,
    )


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))

    data_folder = working_directory / "data"
    out_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)

    _log.debug("All done.")
