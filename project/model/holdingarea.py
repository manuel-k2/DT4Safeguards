from typing import Dict

from model.historyclass import HistoryClass
from model.container import Container

from project.projecttypes.location import Location


class HoldingArea(HistoryClass):
    """
    A class that describes a holding area for conainers.
    Each holding area may contain one container.

    Attributes:
        name (str): Name of holding area.
        location (Location): Location of holding area.
        occupationStatus (bool):
        True if holding area is occupied by container, False if not.
        container_inventory (Dict[int, Container]):
        Dictionary of container in holding area.
    """
    name: str
    location: Location
    occupationStatus: bool
    container_inventory: Dict[int, Container] = {}

    def __init__(self, name: str):
        super.__init__()
        self.SetName(name)

    def SetName(self, name: str):
        """
        Sets holding area name.

        Args:
            name (str): Holding area name.
        """
        self.name = name

    def GetName(self) -> str:
        """
        Gets holding area name.

        Returns:
            str: Holding area name.
        """
        return self.name
    
    def SetLocation(self, location: Location):
        """
        Sets holding area location. Called when added to room.

        Args:
            location (Location): Location of holding area.
        """
        self.location = location

    def GetLocation(self) -> Location:
        """
        Gets location of holding area.

        Return:
            location (Location): Location of holding area.
        """
        return self.location
    
    def SetOccupationStatus(self, occupationStatus: bool):
        """
        Sets occupation status to true or false.

        Args:
            occupationStatus (bool): New occupation status.
        """
        self.occupationStatus = occupationStatus
    
    def GetOccupationStatus(self) -> bool:
        """
        Gets current occupation status.
        
        Returns:
            bool: Current occupation status.
        """
        return self.occupationStatus
    
    def AddContainer(self, container: Container):
        """
        Adds container to holding area.

        Args:
            container (Container): Container to be added to holding area.
        """
        if self.occupationStatus == True:
            print("Holding Area is already occupied.")
        else:
            # Set new location to added container
            container_location = Location().SetFacility(self.location.GetFacility())
            container_location = container_location.SetRoom(self.location.GetRoom())
            container_location = container_location.SetHoldingArea(self)
            container.SetLocation(container_location)
            
            # Add container to inventory
            self.container_inventory[container.id] = container
            self.occupationStatus = True
            print(f"ID: {container.id}, Container: {container} added to holding area.")

    def RemoveContainer(self):
        """
        Removes container from holding area.
        """
        for id, container in self.container_inventory.items():
            print(f"ID: {id}, Container: {container} removed from holding area.")
        self.container_inventory.clear()
        self.occupationStatus = False