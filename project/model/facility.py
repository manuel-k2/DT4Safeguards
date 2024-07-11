from typing import Dict

from model.room import Room
from model.historyclass import HistoryClass

from projecttypes.dimensions import Dimensions


class Facility(HistoryClass):
    """
    A class that describes a facility.

    Attributes:
		id (int): Unique ID of facility.
		name (str): Name of facility.
				dimensions (Dimensions): Dimensions of facility.
		room_inventory (Dict[int, Room]):
			Dictionary of rooms that are contained in facility.
    """

    id: int
    name: str
    dimensions: Dimensions
    room_inventory: Dict[int, Room] = {}

    def __init__(self, name: str, dimensions: Dimensions):
        super().__init__()
        self.name = name
        self.dimensions = dimensions

    def GetDimensions(self) -> Dimensions:
        """
            Get dimensions of the facility instance.

            Returns:
        Dimensions: The dimensions assigned to the instance.
        """
        return self.dimensions

    def AddRoom(self, room: Room):
        """ """
        pass

    # def PresentEntryInventory(self):
    # 	pass
