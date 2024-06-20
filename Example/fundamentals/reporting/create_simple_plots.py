#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this example you would learn about events and how to compute events.
Just run the file.
"""
import base64
import logging
import os
import sys
import tempfile
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from plotly import graph_objects as go
from tsf.core._internals.processing_utils import ProcessingResult
from tsf.core.report import CustomReportTestCase, CustomReportTestStep
from tsf.core.results import Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_signals,
    testcase_definition,
    teststep_definition,
    verifies,
)
from tsf.core.utilities import debug
from tsf.db.assessments import AssessmentAttributeFactory as aaf
from tsf.db.assessments import AssessmentStateFactory as asf
from tsf.db.assessments import ExplicitAssessment
from tsf.db.events import AttributeType, Event, EventAttribute, TimeBase
from tsf.db.results import TeststepResult
from tsf.io.datamodel import SignalDataFrame

from utilities.generate_data import generate_bsig
from utilities.signal_definitions import EXAMPLE, ExampleSignals

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"

_log = logging.getLogger(__name__)


# ##################################################################
# Note: Here is how you define your custom TestStep Report Class ###
# ##################################################################
class TSReport(CustomReportTestStep):
    """TestStepReport Class"""

    template_directories = [os.path.abspath(os.path.join(__file__, "..", "templates"))]

    def __init__(self):
        super().__init__()

    def event(self, event, details):
        context = {}
        # Example Figure with Plotly.
        if "ego_velo" in details:
            ego_velocity = details["ego_velo"]
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=(ego_velocity.index.values - ego_velocity.index.values[0]) * 1e-6,
                    y=ego_velocity.values,
                    name="Ego velocity [km/h]",
                    showlegend=True,
                )
            )
            fig.update_layout(
                legend_title_text="Legend",
                title="Example Scatter Figure with Plotly, on Event Level.",
                xaxis_title="Time in seconds",
            )

            rrr = fig.to_html(full_html=False, include_plotlyjs=False)
            context["ego_velocity_plot"] = f"{rrr}"

        context["details"] = details

        # Example Figure with Matplotlib.
        fig = plt.figure(figsize=(17, 4))
        ax = fig.add_subplot()
        ax.plot(
            (ego_velocity.index.values - ego_velocity.index.values[0]) * 1e-6,
            ego_velocity.values,
            label="Ego velocity [km/h]",
        )

        x_axis = ((ego_velocity.index.values - ego_velocity.index.values[0]) * 1e-6,)
        plt.xticks(np.arange(x_axis[0].min(), x_axis[0].max() + 1, 50))
        ax.set_title("Example Figure with Matplotlib")
        ax.set_xlabel("time (s)")
        ax.set_ylabel("Velocity (km/h)")
        ax.grid()
        ax.legend()
        tmp_file = BytesIO()
        fig.savefig(tmp_file, format="png")
        encoded = base64.b64encode(tmp_file.getvalue()).decode("utf-8")
        html = "<img src='data:image/png;base64,{}'>".format(encoded)
        context["matplot_fig"] = html

        return self.render("event_details.html", context)


# ##################################################################
# Note: Here is how you define your custom TestCase Report Class ###
# ##################################################################
class TCReport(CustomReportTestCase):
    def __init__(self):
        self.time_hist = pd.Series({}, dtype=float)
        self.templates = [os.path.abspath(os.path.join(__file__, "..", "templates"))]
        file_loader = FileSystemLoader(searchpath=self.templates)
        self.jinja_env = Environment(
            loader=file_loader,
        )

    def overview(self):
        """Build reporting details computed on all Teststep results."""
        _log.debug("Overview customization called")

        def plot_histogram(
            name,
            data,
            title=None,
            xaxis_title=None,
            yaxis_title=None,
            xaxis_tickangle=0,
            steps=5,
        ):
            """Plot Histogram custom Function."""
            labels = {k: f"{k}-{k + steps}" for k in range(0, data.index.values.max() + steps, steps)}
            total_time_hist = data.rename(labels)
            fig = go.Figure()
            fig = fig.add_trace(
                go.Bar(
                    x=total_time_hist.index.values,
                    y=np.round(total_time_hist.values, 2),
                    name=name,
                )
            )
            fig.update_layout(
                legend_title_text="Legend",
                title=title,
                xaxis_title=xaxis_title,
                yaxis_title=yaxis_title,
                xaxis_tickangle=xaxis_tickangle,
            )
            return fig.to_html(full_html=False, include_plotlyjs=False)

        html = ""
        html += "<p>&nbsp;"

        # Get Time per Speed Range Histogram plot with Plotly.
        # You can call directly all Plotly functions, or create your own custom function.
        if not self.time_hist.empty:
            html += plot_histogram(
                name="Time per Speed Range Histogram",
                data=self.time_hist,
                title="Example Histogram with Plotly on TC level.",
                xaxis_title="Speed in km/h",
                yaxis_title="Time in secs",
                xaxis_tickangle=-45,
            )

        return (
            f"TC Overview: {html} <p>&nbsp;Here you can add any plot, fig, table or statistic for your TestCase. "
            "<p>&nbsp;"
            "<a href=https://plotly.com/python/creating-and-updating-figures/ target=_blank>How to Create plots "
            "with Plotly</a>"
        )

    def on_result(self, processing_details: ProcessingResult, teststep_result: TeststepResult):
        """Process each stored json result."""
        if "TIME_HIST" in processing_details:
            self.time_hist = self.time_hist.add(processing_details["TIME_HIST"], fill_value=0)


# ##################################################################
# Note: Here is how you define your assessments ###################
# ##################################################################
class MyAssessment1(ExplicitAssessment):
    states = {
        "False Positive": asf.state(
            "False Positive",
            relevant=True,
            explanation="The assessed event is a false positive",
        ),
        "True Positive": asf.state(
            "True Positive",
            relevant=False,
            explanation="The assessed event is a true positive and shall not be counted in the KPI",
        ),
        "NOT ASSESSED": asf.state("Not assessed", relevant=False, explanation="No assessment available yet"),
    }

    attr_1 = aaf.integer_attribute("Attribute 1", 0, 10, 1, default=5)


###################################################################
# Note: Here is how you define your event #########################
###################################################################
class MyEvent1(Event):
    """Example for a custom event."""

    assessment_type = MyAssessment1

    max_ego_velocity = EventAttribute("Max. EGO Velocity", AttributeType.FLOAT)

    def __init__(
        self,
        start_timestamp: int = None,
        end_timestamp: int = None,
    ):
        super().__init__(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            timebase=TimeBase.MTS_PACKAGE_TIMESTAMP,
        )


@teststep_definition(
    step_number=1,
    name="Compute events",
    description="Detect event and stores them in the db",
    expected_result="< 1 Events/km",
)
@register_signals(EXAMPLE, ExampleSignals)
class PlottingLibrariesExampleTeststep(TestStep):
    custom_report = TSReport

    def __init__(self):
        super().__init__()

        ###################################################################
        # Note: Here you can do some event computation ####################
        ###################################################################

    def process_event(self, activation: SignalDataFrame, ego_vel=None):
        """Compute the event base data and the custom attributes.

        :param activation: dataframe of only the activation.
        :param ego_vel: velocity.
        """
        _log.debug("Computing event statistics")

        event = MyEvent1(
            start_timestamp=activation.index.values[0],
            end_timestamp=activation.index.values[-1],
        )
        details = {}
        max_ego_velocity = activation[ExampleSignals.Columns.EGO_VELO].max()
        details["ego_velo"] = ego_vel

        # Attach the event to result, or not maybe some might be skipped automatically...
        if max_ego_velocity < 0:
            self.result.details["MyEvent1"]["unknown"] += 1
            return

        event.max_ego_velocity = max_ego_velocity
        self.result.add_event(event, details)

    def process(self):
        """Checks the given input dta for dynamic acute warnings."""
        _log.debug("Starting processing...")

        example_signals = self.readers[EXAMPLE].signals
        example_signals["row_idx"] = np.arange(0, len(example_signals))
        example_signals["time_s"] = example_signals["mts_ts"].diff() * 1e-6
        example_signals["ego_velo_kmh"] = example_signals["ego_velo"] * 3.6

        activation = example_signals.loc[(example_signals[ExampleSignals.Columns.ACTIVATION_A] != 0)].copy()

        self.result.measured_result = Result(denominator=10, unit="1/km", numerator_is_events=True)

        activation["event_start"] = activation["row_idx"].diff() != 1
        activation["event_idx"] = activation["event_start"].cumsum()

        _log.info("Found '{}' event(s)".format(activation["event_start"].sum()))

        activation.groupby(activation["event_idx"]).apply(self.process_event, example_signals["ego_velo_kmh"])

        def time_histogram_values(signals: object, min_value=0, max_value=50) -> object:
            """

            Parameters
            ----------
            signals : signals Data Frame
            min_value : min_value velocity
            max_value : max_value velocity

            Returns Time vs Speed Histogram. (in seconds).
            -------

            """
            # calculate speed_vs_time histogram values
            signals = signals[["time_s", "ego_velo_kmh"]]
            signals = signals.copy()

            t_bins = [k for k in range(5, max_value + 5, 5)]
            t_bins.insert(0, min_value)
            t_labels = t_bins[:-1]
            hist_values = pd.Series(0, index=t_labels)
            signals["time_bins"] = pd.cut(signals["ego_velo_kmh"], bins=t_bins, labels=t_labels, include_lowest=True)
            hist = pd.Series(signals.groupby(signals["time_bins"]).sum()["time_s"].values, t_labels)
            return hist_values.add(hist, fill_value=0)

        self.result.details["TIME_HIST"] = time_histogram_values(example_signals)


@verifies("req-001")
@testcase_definition(
    name="Example Plot Libraries",
    description="This example shows basic example how to use Plotly and Matplotlib.",
)
class PlottingLibrariesExampleTestcase(TestCase):
    custom_report = TCReport

    @property
    def test_steps(self):
        """Define the test steps."""
        return [PlottingLibrariesExampleTeststep]


def main(data_folder: Path, temp_dir: Path = None, open_explorer=True):
    """Optional, call to debug to set up debugging in the simplest possible way.

    When calling the test case you need to provide a valid input to
    execute the test (e.g. a BSIG file) and report the result.

    This is only meant to jump start testcase debugging.
    """
    test_bsigs = [data_folder / f"test_input_{k}.bsig" for k in range(3)]
    os.makedirs(data_folder, exist_ok=True)
    for b in test_bsigs:
        generate_bsig(b)

    debug(
        PlottingLibrariesExampleTestcase,
        *test_bsigs,
        temp_dir=temp_dir,
        kpi_report=False,
        dev_report=True,
        open_explorer=open_explorer,
    )
    _log.debug("All done.")


if __name__ == "__main__":
    working_directory = Path(tempfile.mkdtemp("_tsf"))

    data_folder = working_directory / "data"
    out_folder = working_directory / "out"

    main(data_folder=data_folder, temp_dir=out_folder, open_explorer=True)
