from model.historyclass import HistoryClass

from projecttypes.dimensions import Dimensions


class Room(HistoryClass):
    """
    A class that describes a room.

    Attributes:
            type (str): Type of facility.
            name (str): Name of facility.
            dimensions (Dimensions): Dimensions of facility.
    """

    type: str
    name: str
    dimensions: Dimensions

    def __init__(self, type: str, name: str, dimensions: Dimensions):
        super().__init__()
        self.type = type
        self.name = name
        self.dimensions = dimensions

    def CheckForEquipment(self):
        pass

    def PresentExitInventory(self):
        pass
