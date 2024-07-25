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
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)

    def SetType(self, type: str):
        """
        Sets facility type.

        Args:
            type (str): Facility type.
        """
        self.type = type
    
    def GetType(self) -> str:
        """
        Gets facility type.

        Returns:
            str: Facility type.
        """
        return self.type

    def SetName(self, name: str):
        """
        Sets facility name.

        Args:
            name (str): Facility name.
        """
        self.name = name
    
    def GetName(self) -> str:
        """
        Gets facility name.

        Returns:
            str: Facility name.
        """
        return self.name

    def SetDimensions(self, dimensions: Dimensions):
        """
        Sets dimensions of the facility instance.

        Args:
            dimensions (Dimensions): Dimensions assigned to the facility instance.
        """
        self.dimensions = dimensions
    
    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the facility instance.

        Returns:
            Dimensions: Dimensions assigned to the facility instance.
        """
        return self.dimensions

    def AddRoom(self, room: Room):
        """
        Adds a room to the facility's room inventory.

        Args:
            room (Room): Room to be added to inventory.
        """
        self.room_inventory[room.id] = room

    def RemoveRoom(self, roomID: int):
        """
        Removes a room from the facility's room inventory.

        Args:
            roomID (int): ID of room to be removed from inventory.
        """
        del self.room_inventory[roomID]

    def GetRoomInventory(self) -> Dict[int, Room]:
        """
        Gets the facility's room inventory.

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
