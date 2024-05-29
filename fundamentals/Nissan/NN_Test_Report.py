from typing import List
import numpy as np
import plotly.express as px
from plotly import graph_objects as go
import scipy
from tsf.db.results import TeststepResult

from tsf.core.report import (
    CustomReportTestStep,
    CustomReportTestCase,
    ProcessingResult,
    ProcessingResultsList)


class CustomTeststepReport(CustomReportTestStep):
    def overview(
            self,
            processing_details_list: ProcessingResultsList,
            teststep_result: List["TeststepResult"],
    ):
        s = "<h3>Additional Data</h3>"

        # Iterating over all processing details
        pr_list = processing_details_list
        for d in range(len(pr_list)):
            json_entries = ProcessingResult.from_json(pr_list.processing_result_files[d])
            s += "Item ID is : {}<br/><br/>".format(json_entries.item_id)
            s += "Result is : {}<br/><br/>".format(json_entries.details["Result"])
        return s

    def details(self, processing_details: ProcessingResult, teststep_result: "TeststepResult") -> str:
        s = "<h3>details part</h3>"
        for k, v in processing_details.details.items():
            s += "<div>{}:{}</div>".format(k, v)

        s += "<h3>Events part</h3>"
        for event in teststep_result.events:
            s += "<div>{}</div>".format(event)

        s += "<div>Measured (part) Result: {}</div>".format(teststep_result.measured_result)
        # s += "<h3>You can also add pie charts like the one below</h3>"
        # df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
        # df.loc[df["pop"] < 2.0e6, "country"] = "Other countries"  # Represent only large countries
        # fig = px.pie(df, values="pop", names="country", title="Population of European continent")

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=processing_details['mts'],
                y=processing_details['mts'],
                name="mts",
            )
        )
        fig = px.line(x=processing_details['mts'])
        # if 'mts' in processing_details:
        #     fig.add_trace(
        #         go.Scatter(
        #             x=processing_details['mts'],
        #             y=processing_details['mts'],
        #             name="mts",
        #         )
        #     )
        #     fig = px.line(x=processing_details['mts'])
        # else:
        #     fig = px.line(x=[10, 2, 3], y=[4, 5, 6])

        s += fig.to_html(full_html=False, include_plotlyjs=False)
        return s


class CustomTestcaseReport(CustomReportTestCase):
    def overview(self):
        s = "<h3>LSCA sample plots</h3>"

        # data_canada = px.data.gapminder().query("country == 'Canada'")
        # fig = px.bar(data_canada, x="year", y="pop")
        fig = px.line(x=[1, 2, 3], y=[1, 2, 3])
        s += fig.to_html(full_html=False, include_plotlyjs=False)
        return s
