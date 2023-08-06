from enum import Enum


class MachineOperatingStatusType(Enum):
    Available = 0
    InOperating = 1
    InRepair = 2
    Pause = 3
