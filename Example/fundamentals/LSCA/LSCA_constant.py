
from tsf.io.signals import SignalDefinition, SignalReader


class ExampleSignals(SignalDefinition):
    """Example signal definition."""

    class Columns(SignalDefinition.Columns):
        """Column defines."""

        LSCA_Brake_Port = "ADC5xx_Device.EM_DATA.EmLscaBrakePort.sSigHeader.eSigStatus"
        ACTIVATION_A = "ADC5xx_Device.TRJPLA_DATA.TrjPlaParkingBoxPort.uiVersionNumber"
        ACTIVATION_B = "ADC5xx_Device.TRJPLA_DATA.TrjPlaParkingBoxPort.numValidParkingBoxes_nu"
        ACTIVATION_D = "ADC5xx_Device.TRJPLA_DATA.TrjPlaEnvModelPort.numberOfStaticObjects_u8"
        BINARY_ACTIVATION_A = "binary_activation_a"
        BINARY_ACTIVATION_B = "binary_activation_b"
        EGO_VELO = "ego_velo"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.LSCA_Brake_Port: "Example Signal ADC5xx_Device.EM_DATA.EmLscaBrakePort.sSigHeader.eSigStatus",
            self.Columns.ACTIVATION_A: "Example Signal Data.activation.sig_a",
            self.Columns.ACTIVATION_B: "Example Signal Data.activation.sig_b",
            self.Columns.ACTIVATION_D: "Example Signal Data.activation.sig_d",
            self.Columns.BINARY_ACTIVATION_A: "Example Signal Data.aggregation_all.90",
            self.Columns.BINARY_ACTIVATION_B: "Example Signal Data.aggregation_all.50",
            self.Columns.EGO_VELO: "Example Signal Data.ego.velocity.x",
        }
