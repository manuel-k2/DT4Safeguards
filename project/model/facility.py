from typing import Dict

from model.room import Room
from model.historyclass import HistoryClass
from projecttypes.dimensions import Dimensions


class Facility(HistoryClass):
    """
    A class that describes a facility.

    Attributes:
        type (str): Type of facility.
        name (str): Name of facility.
        dimensions (Dimensions): Dimensions of facility.
        room_inventory (Dict[int, Room]): Dictionary of rooms that are
        contained in facility.
    """

    type: str
    name: str
    dimensions: Dimensions
    room_inventory: Dict[int, Room] = {}

    def __init__(self, type: str, name: str, dimensions: Dimensions):
        super().__init__()
        self.type = type
        self.name = name
        self.dimensions = dimensions

    def GetType(self) -> str:
        """
        Get facility type.

        Returns:
            str: Facility type.
        """
        return self.type

    def GetName(self) -> str:
        """
        Get facility name.

        Returns:
            str: Facility name.
        """
        return self.name

    def GetDimensions(self) -> Dimensions:
        """
        Get dimensions of the facility instance.

        Returns:
            Dimensions: The dimensions assigned to the instance.
        """
        return self.dimensions

    def AddRoom(self, room: Room):
        """
        Add a room to the facility's room inventory.

        Args:
            room (Room): Room to be added to inventory.
        """
        self.room_inventory[room.id] = room

    def RemoveRoom(self, roomID: int):
        """
        Remove a room from the facility's room inventory.

        Args:
            roomID (int): ID of room to be removed from inventory.
        """
        del self.room_inventory[roomID]

    def GetRoomInventory(self) -> Dict[int, Room]:
        """
        Get the facility's room inventory.

        Returns:
            Dict[int, Room]: Dictionary of rooms that are contained
            in facility.
        """
        if not self.room_inventory:
            print("Inventory is empty.")
        else:
            for id, room in self.room_inventory.items():
                print(f"ID: {id}, Room: {room}")
        return self.room_inventory

    # def PresentEntryInventory(self):
    #     pass
