from typing import Dict

from model.historyclass import HistoryClass
from model.holdingarea import HoldingArea

from projecttypes.dimensions import Dimensions
from project.projecttypes.location import Location


class Room(HistoryClass):
    """
    A class that describes a room.

    Attributes:
        type (str): Type of room.
        name (str): Name of room.
        dimensions (Dimensions): Dimensions of room.
        location (Location): Location of room.
        holdingarea_inventory (Dict[int, HoldingArea]): Dictionary of
        holding areas that are contained in room.
    """

    type: str
    name: str
    dimensions: Dimensions
    location: Location
    holdingArea_inventory: Dict[int, HoldingArea] = {}

    def __init__(self, type: str, name: str, dimensions: Dimensions):
        super().__init__()
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)

    def SetType(self, type: str):
        """
        Sets room type.

        Args:
            type (str): Room type.
        """
        self.type = type

    def GetType(self) -> str:
        """
        Gets room type.

        Returns:
            str: Room type.
        """
        return self.type

    def SetName(self, name: str):
        """
        Sets room name.

        Args:
            name (str): Room name.
        """
        self.name = name

    def GetName(self) -> str:
        """
        Gets room name.

        Returns:
            str: Room name.
        """
        return self.name

    def SetDimensions(self, dimensions: Dimensions):
        """
        Sets dimensions of the room instance.

        Args:
            dimensions (Dimensions): Dimensions assigned to the room instance.
        """
        self.dimensions = dimensions

    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the room instance.

        Returns:
            Dimensions: Dimensions assigned to the room instance.
        """
        return self.dimensions
    
    def SetLocation(self, location: Location):
        """
        Sets room location. Called when added to a facility.

        Args:
            location (Location): Location of room.
        """
        self.location = location

    def GetLocation(self) -> Location:
        """
        Gets location of room.

        Return:
            location (Location): Location of room.
        """
        return self.location

    def AddHoldingArea(self, holdingArea: HoldingArea):
        """
        Adds a holding area to the rooms's holding area inventory.

        Args:
            holdingArea (HoldingArea):
            Holding area to be added to inventory.
        """
        # Set new location to added holding area
        holdingArea_location = Location().SetFacility(self.location.GetFacility())
        holdingArea_location = holdingArea_location.SetRoom(self)
        holdingArea.SetLocation(holdingArea_location)

        # Add holding area to inventory
        self.holdingArea_inventory[holdingArea.id] = holdingArea

    def RemoveHoldingArea(self, holdingAreaID: int):
        """
        Removes a holding area from the rooms's holding area inventory.

        Args:
            holdingAreaID (int):
            ID of holding area to be removed from inventory.
        """
        if holdingAreaID not in self.holdingArea_inventory:
            raise KeyError(f"Holding area with ID {holdingAreaID} not found.")
        if len(self.holdingArea_inventory) == 1 and holdingAreaID in self.holdingArea_inventory:
            self.holdingArea_inventory.clear()
        else:
            del self.holdingArea_inventory[holdingAreaID]

    def GetHoldingAreaInventory(self) -> Dict[int, HoldingArea]:
        """
        Gets the room's holding area inventory.

        Returns:
            Dict[int, HoldingArea]:
            Dictionary of holding areas that are contained in room.
        """
        if not self.holdingArea_inventory:
            print("Inventory is empty.")
        else:
            for id, holdingArea in self.holdingArea_inventory.items():
                print(f"ID: {id}, Holding area: {holdingArea}")
        return self.holdingArea_inventory

    def CheckForEquipment(self):
        pass

    def PresentExitInventory(self):
        pass
