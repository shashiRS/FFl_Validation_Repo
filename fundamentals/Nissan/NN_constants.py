
from tsf.io.signals import SignalDefinition


class ExampleSignals(SignalDefinition):
    """Example signal definition."""

    class Columns(SignalDefinition.Columns):
        """Column defines."""

        Trunk = "Trunk"
        sigstate = "sigstate"
        DOORFL = "DoorFL"
        DOORFR = "DoorFR"
        DOORBL = "DoorBL"
        DOORBR = "DoorBR"

    def __init__(self):
        """Initialize the signal definition."""
        super().__init__()

        self._properties = {
            self.Columns.Trunk: "M7board.CAN_Thread.TrunkLidStatusPort.open_nu",
            self.Columns.sigstate: "M7board.CAN_Thread.StarterStatusPort.signalState_nu",
            self.Columns.DOORFL: "M7board.CAN_Thread.DoorStatusPort.status.frontPsgr_nu",
            self.Columns.DOORFR: "M7board.CAN_Thread.DoorStatusPort.status.driver_nu",
            self.Columns.DOORBR: "M7board.CAN_Thread.DoorStatusPort.status.rearRight_nu",
            self.Columns.DOORBL: "M7board.CAN_Thread.DoorStatusPort.status.rearLeft_nu",

        }
