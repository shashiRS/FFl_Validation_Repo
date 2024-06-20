#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quickstart example."""
import logging
import os
import sys
from typing import Dict, List, Tuple

import numpy as np
from plotly import graph_objects as go

TSF_BASE = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
if TSF_BASE not in sys.path:
    sys.path.append(TSF_BASE)

from tsf.core._internals.processing_utils import ProcessingResult, ProcessingResultsList
from tsf.core._internals.video_exporter.image_extractor import ReferenceImageExtractor
from tsf.core._internals.video_exporter.image_path import ImagePath
from tsf.core.common import AggregateFunction, RelationOperator
from tsf.core.report import CustomReportTestCase, CustomReportTestStep
from tsf.core.results import ExpectedResult, Result
from tsf.core.testcase import (
    TestCase,
    TestStep,
    register_inputs,
    register_signals,
    testcase_definition,
    teststep_definition,
)
from tsf.db.assessments import (
    AssessmentAttributeFactory,
    AssessmentStateFactory,
    ExplicitAssessment,
)
from tsf.db.events import Event
from tsf.db.results import TeststepResult

from utilities.signal_definitions import EXAMPLE, ExampleSignals

_log = logging.getLogger(__name__)


class ExampleAssessment(ExplicitAssessment):

    states = {
        "FP": AssessmentStateFactory.state(name="FP", relevant=True),
        "TP": AssessmentStateFactory.state(name="TP", relevant=False),
    }

    test = AssessmentAttributeFactory.selection_attribute("test", ["A", "B", "C"])


class ExampleEvent(Event):
    """Example Event"""

    assessment_type = ExampleAssessment


def html_escape(s):
    if not s:
        return ""

    return (
        s.replace("<", "	&#60;")
        .replace(">", "	&#62;")
        .replace("\\", "&#92;")
        .replace("'", "&#39;")
        .replace('"', "&#34;")
    )


class ExampleTestStepCustom(CustomReportTestStep):

    template_directories = [os.path.abspath(os.path.join(__file__, "../../quarantine", "templates"))]

    def __init__(self):
        super().__init__()
        self._image_path = ImagePath()
        self._rie = ReferenceImageExtractor()

    def make_ego_plots(self, event, details):
        fig = go.Figure()

        ts = details["scene_ts"].values
        ego_velocity = details["ego_velocity"]

        shapes = [
            # dict(
            #     type="rect",
            #     yref="paper",
            #     y0=0,
            #     y1=1,
            #     xref="x",
            #     x0=(event.start_timestamp - ego_velocity.index.values[0]) * 1e-6,
            #     x1=(event.end_timestamp - ego_velocity.index.values[0]) * 1e-6,
            #     fillcolor="LightSalmon",
            #     opacity=0.5,
            #     layer="below",
            #     line_width=0,
            # )
        ]

        fig.add_trace(
            go.Scatter(
                x=ego_velocity.index.values,
                y=ego_velocity.values * 3.6,
                name="Ego velocity [km/h]",
            )
        )

        for x, txt in [(event.start_timestamp, "Start"), (event.end_timestamp, "End")]:
            fig.add_shape(
                type="line",
                x0=x,
                y0=0,
                x1=x,
                y1=1,
                xref="x",
                yref="paper",
                layer="below",
                line=dict(color="black", width=2, dash="dot"),
            )
            fig.add_annotation(
                dict(
                    font=dict(color="black", size=12),
                    x=x,
                    y=1.02,
                    showarrow=False,
                    text=txt,
                    # textangle=-45,
                    xref="x",
                    yref="paper",
                    xanchor="left",
                    yanchor="bottom",
                    xshift=-10,
                )
            )

        fig.add_shape(
            type="line",
            x0=ts[0],
            y0=0,
            x1=ts[0],
            y1=1,
            xref="x",
            yref="paper",
            layer="below",
            name="playback_marker",
            line=dict(color="red", width=2, dash="dot"),
        )

        fig.update_layout(
            shapes=shapes,
            legend_title_text="Legend",
            title="Kinematics",
            xaxis_title="Time in seconds",
        )

        return fig.to_html(include_plotlyjs=False, full_html=False, config={"responsive": True})

    def event(self, event: "Event", details: dict) -> str:
        return html_escape(f"Event: {event.id} -> {event.state.name}<br>{details}")

    def event_with_online_assessment(self, event: Event, details) -> Tuple[str, str]:
        ts = details["scene_ts"]

        front_ts, front_frames, front_v = "", "", ""

        # rec = event.teststep_result.entry_adapter.reference
        # front_ts, front_frames, front_v = self.environment.asset.extract_snippet(event, rec, ts, RefCamAngle.FRONT)
        # left_ts, left_frames, left_v = self.environment.asset.extract_snippet(event, rec, ts, RefCamAngle.LEFT)
        # right_ts, right_frames, right_v = self.environment.asset.extract_snippet(event, rec, ts, RefCamAngle.RIGHT)

        event_start_frame = np.argmin(np.abs(ts - event.start_timestamp))
        event_end_frame = np.argmin(np.abs(ts - event.end_timestamp))

        context = {
            "front_video_path": front_v,
            "front_video_timestamps": [t for t in front_ts],
            "front_video_frame_time": [t for t in front_frames],
            "timestamps": [t for t in ts],
            "event_start_frame": event_start_frame,
            "event_end_frame": event_end_frame,
            "signal_plots": self.make_ego_plots(event, details),
        }

        vizu_callbacks = """
            // Plotly

      media_ctrl.add_vizu_listener(function(selectedTimestamp) {
          var update = {
                "shapes[2].x0": selectedTimestamp,
                "shapes[2].x1": selectedTimestamp
            };

          Plotly.animate($(".plotly-graph-div")[0], {layout: update}, {
              transition: {duration: 0},
              frame: {duration: 0, redraw: false}
          });
      });
        """

        # """
        #       // Middle video
        #       front_video_timestamp = $("#event-details").data("video-timestamps");
        #       front_video_frame_times = $("#event-details").data("video-frame-time");
        #
        #       media_ctrl.add_vizu_listener(function(selectedTimestamp) {
        #           var video_index = binarySearch(selectedTimestamp, front_video_timestamp);
        #               if (video_index >=0 && video_index < front_video_frame_times.length) {
        #                   $("#video")[0].currentTime = front_video_frame_times[video_index];
        #               } else {
        #                 console.log("Invalid index into video frames specified.");
        #               }
        #       });
        #
        #           """
        return self.render("assessment_ui.html.j2", context), vizu_callbacks

    def details(self, processing_details: ProcessingResult, teststep_result: TeststepResult) -> str:
        return html_escape(f"{teststep_result} -> {processing_details}")

    def overview(
        self,
        processing_details_list: ProcessingResultsList,
        teststep_result: List["TeststepResult"],
    ) -> str:
        return "<h3>TS Overview</h3>" + html_escape(f"# of results: {len(teststep_result)}.")


class ExampleTestCaseCustom(CustomReportTestCase):
    def __init__(self):
        self._d = []

    def overview(self) -> str:
        """Build reporting details computed on all teststep results."""
        return str(self._d)

    def on_result(self, processing_details: Dict, teststep_result: "TeststepResult"):
        """Process details to aggregate data for the overview of the teststep.

        :param processing_details:
        :param teststep_result:
        """
        self._d.append(html_escape(f"{teststep_result} -> {processing_details}"))


@teststep_definition(
    1,
    "Activation check",
    "Usecase like example. Check that we have a activation in every input.",
    ExpectedResult(1.1, unit="s", operator=RelationOperator.GREATER_OR_EQUAL, aggregate_function=AggregateFunction.ALL),
)
@register_signals(EXAMPLE, ExampleSignals)
class ExampleAEBTestStep1All1(TestStep):
    """Example test step."""

    custom_report = ExampleTestStepCustom

    def process(self, **kwargs):
        """Count the activations (raising flanks on the mileage (integral of the velocity over time))."""
        # Get the read data frame
        exmpl = self.readers[EXAMPLE]

        # check for raising flanks
        flanks = exmpl[ExampleSignals.Columns.ACTIVATION_A].diff() > 0

        activations = exmpl.loc[flanks]
        for idx, row in activations.iterrows():
            e = ExampleEvent(start_timestamp=idx, end_timestamp=idx)

            mask = (exmpl[ExampleSignals.Columns.TS] >= idx - 3e6) & (
                exmpl[ExampleSignals.Columns.TS] <= idx - 1e6
            )

            details = dict(
                v_ego=row[ExampleSignals.Columns.EGO_VELO],
                scene_ts=exmpl.loc[mask, ExampleSignals.Columns.TS],
                ego_velocity=exmpl.loc[mask, ExampleSignals.Columns.EGO_VELO],
            )
            self.result.add_event(e, details)

        td = exmpl[ExampleSignals.Columns.TS].diff() * 1e-6
        mileage = np.sum(exmpl[ExampleSignals.Columns.EGO_VELO] * td) / 1000

        # Store the result
        self.result.measured_result = Result(None, mileage, unit="1/km", numerator_is_events=True)


@testcase_definition("EX_EBA_001_003", "KPI 3 (ALL)", "Example KPI Test with aggregation function all.")
@register_inputs("/SYSHADHA22/s3_reading_test")
@register_inputs("/SYSHADHA22/FOT")
class ExampleAllTestCase(TestCase):
    """Example test case."""

    custom_report = ExampleTestCaseCustom

    @property
    def test_steps(self):
        """Define the test steps."""
        return [
            ExampleAEBTestStep1All1,
            # ExampleAEBTestStep1All2,
        ]
