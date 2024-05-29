"""Needed methods to drive the examples."""

import logging

import numpy as np
from tsf.io.signals import SignalDefinition

_log = logging.getLogger(__name__)

EXAMPLE = "example"


class ExampleSignals(SignalDefinition):
    """Example signals."""

    class Columns(SignalDefinition.Columns):
        """Definition of the dataframe columns."""

        ACTIVATION_A = "some_activation_a"
        ACTIVATION_B = "some_activation_b"
        BINARY_ACTIVATION_A = "binary_activation_a"
        BINARY_ACTIVATION_B = "binary_activation_b"
        EGO_VELO = "ego_velo"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.ACTIVATION_A: "Example Signal Data 1.activation.sig_a",
            self.Columns.ACTIVATION_B: "Example Signal Data 1.activation.sig_b",
            self.Columns.BINARY_ACTIVATION_A: "Example Signal Data 1.aggregation_all.90_a",
            # example of providing list of signals and down-casting the values
            self.Columns.BINARY_ACTIVATION_B: {
                "signal": [
                    "Example Signal Data 1.aggregation_all.90_b",
                    "Some Device.aggregation_all.90_b",
                ],
                "as_type": np.int8,
            },
            # example of providing single signal and down-casting the values
            self.Columns.EGO_VELO: {
                "signal": "Example Signal Data 1.ego.velocity.x",
                "as_type": "float32",
            },
        }


class ExampleSignals2(SignalDefinition):
    """Another example signal definition."""

    class Columns(SignalDefinition.Columns):
        """Definition of the dataframe columns."""

        ACTIVATION_C = "some_activation_c"
        ACTIVATION_D = "some_activation_d"
        BINARY_ACTIVATION_C = "binary_activation_c"
        BINARY_ACTIVATION_D = "binary_activation_d"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.ACTIVATION_C: "Example Signal Data 2.activation.sig_c",
            self.Columns.ACTIVATION_D: "Example Signal Data 2.activation.sig_d",
            self.Columns.BINARY_ACTIVATION_C: "Example Signal Data 2.aggregation_all.90_c",
            self.Columns.BINARY_ACTIVATION_D: "Example Signal Data 2.aggregation_all.50_d",
        }


class ExampleSignals3(SignalDefinition):
    """Example signals with duplicate assignment."""

    class Columns(SignalDefinition.Columns):
        """Definition of the dataframe columns."""

        ACTIVATION_E = "some_activation_e"
        ACTIVATION_F = "some_activation_f"
        BINARY_ACTIVATION_E = "binary_activation_e"
        BINARY_ACTIVATION_F = "binary_activation_f"
        EGO_VELO = "ego_velo"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.ACTIVATION_E: "Example Signal Data 1.activation.sig_e",
            self.Columns.ACTIVATION_F: "Example Signal Data 1.activation.sig_e",
            self.Columns.BINARY_ACTIVATION_E: "Example Signal Data 1.aggregation_all.90_e",
            self.Columns.BINARY_ACTIVATION_F: "Example Signal Data 1.aggregation_all.50_f",
            self.Columns.EGO_VELO: "Example Signal Data 1.ego.velocity.x",
        }


class ExampleSignals4(SignalDefinition):
    """Example signals with duplicate assignment."""

    class Columns(SignalDefinition.Columns):
        """Definition of the dataframe columns."""

        ACTIVATION_E = "some_activation_e"
        ACTIVATION_F = "some_activation_f"
        BINARY_ACTIVATION_E = "binary_activation_e"
        BINARY_ACTIVATION_F = "binary_activation_f"
        EGO_VELO = "ego_velo"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.ACTIVATION_E: "Example Signal Data 1.activation.sig_e",
            self.Columns.ACTIVATION_F: "Example Signal Data 1.activation.sig_e",
            self.Columns.BINARY_ACTIVATION_E: "Example Signal Data 1.aggregation_all.90_e",
            self.Columns.BINARY_ACTIVATION_F: "Example Signal Data 1.aggregation_all.50_f",
            self.Columns.EGO_VELO: "Example Signal Data 1.ego.velocity.x",
        }
