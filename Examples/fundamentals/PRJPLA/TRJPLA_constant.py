
from tsf.io.signals import SignalDefinition, SignalReader


class ExampleSignals(SignalDefinition):
    """Example signal definition."""

    class Columns(SignalDefinition.Columns):
        """Column defines."""

        TRJPLA_DATA_uia = "uia"
        TRJPLA_DATA_valid_pak = "valid_pak"
        TRJPLA_DATA_dyn_obj="dyn_obj"
        TRJPLA_DATA_nopak_mark="nopak_mark"
        TRJPLA_DATA_static_obj="static_obj"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {

            self.Columns.TRJPLA_DATA_uia: "ADC5xx_Device.TRJPLA_DATA.TrjPlaParkingBoxPort.uiVersionNumber",
            self.Columns.TRJPLA_DATA_valid_pak: "ADC5xx_Device.TRJPLA_DATA.TrjPlaParkingBoxPort.numValidParkingBoxes_nu",
            self.Columns.TRJPLA_DATA_dyn_obj: "ADC5xx_Device.TRJPLA_DATA.TrjPlaEnvModelPort.numberOfDynamicObjects_u8",
            self.Columns.TRJPLA_DATA_nopak_mark: "ADC5xx_Device.TRJPLA_DATA.TrjPlaEnvModelPort.numberOfParkMarkings_u8",
            self.Columns.TRJPLA_DATA_static_obj: "ADC5xx_Device.TRJPLA_DATA.TrjPlaEnvModelPort.numberOfStaticObjects_u8",

        }
