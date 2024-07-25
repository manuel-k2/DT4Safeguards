from model.historyclass import HistoryClass

from project.projecttypes.command import Command
from projecttypes.dimensions import Dimensions
from project.projecttypes.location import Location


class Container(HistoryClass):
    """
    A class that describes a container for nuclear material.

    Attributes:
            type (str): Type of container.
            name (str): Name of container.
            dimensions (Dimensions): Dimensions of container.
            location (Location): Location of container.

    """
    type: str
    name: str
    dimensions: Dimensions
    location: Location

    def __init__(self, type: str, name: str, dimensions: Dimensions, location: Location):
        super().__init__()
        self.type = type
        self.name = name
        self.dimensions = dimensions
        self.SetLocation(location)
    
    def SetType(self, type: str):
        """
        Sets container type.

        Args:
            type (str): Container type.
        """
        self.type = type
    
    def GetType(self) -> str:
        """
        Gets container type.

        Returns:
            str: Container type.
        """
        return self.type

    def SetName(self, name: str):
        """
        Sets container name.

        Args:
            name (str): Container name.
        """
        self.name = name
    
    def GetName(self) -> str:
        """
        Gets container name.

        Returns:
            str: Container name.
        """
        return self.name

    def SetDimensions(self, dimensions: Dimensions):
        """
        Sets dimensions of the container instance.

        Args:
            dimensions (Dimensions): Dimensions assigned to the container instance.
        """
        self.dimensions = dimensions
    
    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the container instance.

        Returns:
            Dimensions: Dimensions assigned to the container instance.
        """
        return self.dimensions
    
    def SetLocation(self, location: Location):
        """
        Sets container location.

        Args:
            location (Location): New location of container.
        """
        self.location = location

    def GetLocation(self) -> Location:
        """
        Gets current location of container.

        Return:
            location (Location): Current location of container.
        """
        return self.location

    def Activation(self, cmd: Command):
        """
        Activates certain functions based on
        the command type.

        Args:
            cmd (Command): Instance of command to be processed.
        
        """
        if cmd.type == "transport":
            self.SetLocation(cmd.destination)
        return super().Activation(cmd)
        
