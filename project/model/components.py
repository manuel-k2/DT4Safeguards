from dataclasses import dataclass, field
from typing import Dict

from model.monitoringsystem import IDClass

from projecttypes.dimensions import Dimensions


@dataclass
class HistoryClass(IDClass):
    """
    The base class for all instances that come with a history that
    tracks all changes made to the instance.

    Attributes:
        registry (Dict[int, dict]): Dictionary to store command
            specifications.
    """

    def __init__(self):
        super().__init__()
        self.registry: Dict[int, dict] = {}

    def Activation(self, cmd: "Command") -> None:
        """
        Registers a command and activates certain functions based on
        the command type.

        Args:
            cmd (Command): Instance of command to be processed.
        """
        self.UpdateHistory(cmd)

    def UpdateHistory(self, cmd: "Command") -> None:
        """
        Stores command specifications in a dictionary.

        Args:
            cmd (Command): Instance of command to be processed.
        """
        self.registry[cmd.id] = {"cmdType": cmd.type, "target": cmd.target}
    
    def GetHistory(self) -> Dict[int, dict]:
        """
        Gets history.
        
        Returns:
            Dict[int, dict]: History of an instance.
        """
        return self.registry
    
    def ShowHistory(self) -> None:
        """
        Shows history of instance.
        """
        if not self.registry:
            print("Registry is empty.")
        else:
            for id, instance in self.registry.items():
                print(f"Command with ID: {id}, {instance}")


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

    def __init__(self, type: str, name: str, dimensions: Dimensions):
        super().__init__()
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)
        self.room_inventory: Dict[int, "Room"] = {}

    def SetType(self, type: str) -> None:
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

    def SetName(self, name: str) -> None:
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

    def SetDimensions(self, dimensions: Dimensions) -> None:
        """
        Sets dimensions of the facility instance.

        Args:
            dimensions (Dimensions):
                Dimensions assigned to the facility instance.
        """
        self.dimensions = dimensions

    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the facility instance.

        Returns:
            Dimensions: Dimensions assigned to the facility instance.
        """
        return self.dimensions

    def AddRoom(self, room: "Room") -> None:
        """
        Adds a room to the facility's room inventory.

        Args:
            room (Room): Room to be added to inventory.
        """
        # Set new location to added room
        room_location = Location(self)
        room.SetLocation(room_location)

        # Add room to inventory
        self.room_inventory[room.id] = room

    def RemoveRoom(self, roomID: int) -> None:
        """
        Removes a room from the facility's room inventory.

        Args:
            roomID (int): ID of room to be removed from inventory.
        """
        if roomID not in self.room_inventory:
            raise KeyError(f"Room with ID {roomID} not found.")
        if len(self.room_inventory) == 1 and roomID in self.room_inventory:
            self.room_inventory.clear()
        else:
            del self.room_inventory[roomID]

    def GetRoomInventory(self) -> Dict[int, "Room"]:
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
                print(f"ID: {id}, Room: {room.name}")
        return self.room_inventory

    def PresentEntryInventory(self):
        pass


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

    def __init__(self, type: str, name: str, dimensions: Dimensions):
        super().__init__()
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)
        self.holdingArea_inventory: Dict[int, "HoldingArea"] = {}

    def SetType(self, type: str) -> None:
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

    def SetName(self, name: str) -> None:
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

    def SetDimensions(self, dimensions: Dimensions) -> None:
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

    def SetLocation(self, location: "Location") -> None:
        """
        Sets room location. Called when added to a facility.

        Args:
            location (Location): Location of room.
        """
        self.location = location

    def GetLocation(self) -> "Location":
        """
        Gets location of room.

        Return:
            location (Location): Location of room.
        """
        return self.location

    def AddHoldingArea(self, holdingArea: "HoldingArea") -> None:
        """
        Adds a holding area to the rooms's holding area inventory.

        Args:
            holdingArea (HoldingArea):
                Holding area to be added to inventory.
        """
        # Set new location to added holding area
        holdingArea_location = Location(self.location.GetFacility(), self)
        holdingArea.SetLocation(holdingArea_location)

        # Add holding area to inventory
        self.holdingArea_inventory[holdingArea.id] = holdingArea

    def RemoveHoldingArea(self, holdingAreaID: int) -> None:
        """
        Removes a holding area from the rooms's holding area inventory.

        Args:
            holdingAreaID (int):
                ID of holding area to be removed from inventory.
        """
        if holdingAreaID not in self.holdingArea_inventory:
            raise KeyError(f"Holding area with ID {holdingAreaID} not found.")
        if (
            len(self.holdingArea_inventory) == 1
            and holdingAreaID in self.holdingArea_inventory
        ):
            self.holdingArea_inventory.clear()
        else:
            del self.holdingArea_inventory[holdingAreaID]

    def GetHoldingAreaInventory(self) -> Dict[int, "HoldingArea"]:
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
                print(f"Holding area: {holdingArea.name}, ID: {id}")
        return self.holdingArea_inventory

    def CheckForEquipment(self):
        pass

    def PresentExitInventory(self):
        pass


class HoldingArea(HistoryClass):
    """
    A class that describes a holding area for containers.
    Each holding area may contain one container.

    Attributes:
        name (str): Name of holding area.
        location (Location): Location of holding area.
        occupationStatus (bool):
            True if holding area is occupied by container, False if not.
        container_inventory (Dict[int, Container]):
            Dictionary of container in holding area.
    """

    def __init__(self, name: str):
        super().__init__()
        self.SetName(name)
        self.SetOccupationStatus(False)
        self.container_inventory: Dict[int, "Container"] = {}

    def SetName(self, name: str) -> None:
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

    def SetLocation(self, location: "Location") -> None:
        """
        Sets holding area location. Called when added to room.

        Args:
            location (Location): Location of holding area.
        """
        self.location = location

    def GetLocation(self) -> "Location":
        """
        Gets location of holding area.

        Return:
            location (Location): Location of holding area.
        """
        return self.location

    def SetOccupationStatus(self, occupationStatus: bool) -> None:
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

    def AddContainer(self, container: "Container") -> None:
        """
        Adds container to holding area.

        Args:
            container (Container): Container to be added to holding area.
        """
        if self.occupationStatus is True:
            print("Holding Area is already occupied.")
        else:
            # Set new location to added container
            container_location = Location(
                self.location.GetFacility(), self.location.GetRoom(), self
            )
            container.SetLocation(container_location)

            # Add container to inventory
            self.container_inventory[container.id] = container
            self.occupationStatus = True

    def RemoveContainer(self) -> None:
        """
        Removes container from holding area.
        """
        for id, container in self.container_inventory.items():
            print(
                f"ID: {id}, Container: {container} removed from holding area."
            )
        self.container_inventory.clear()
        self.occupationStatus = False

    def GetContainer(self) -> "Container":
        """
        Gets the container contained in holding area.

        Returns:
            Container:
                Container that is contained in holding area.
        """
        if self.occupationStatus is False:
            print("No container in holding area.")
            pass
        else:
            for id, container in self.container_inventory.items():
                print(f"Container: {container.name}, ID: {id}")
                return container


class Container(HistoryClass):
    """
    A class that describes a container for nuclear material.

    Attributes:
            type (str): Type of container.
            name (str): Name of container.
            dimensions (Dimensions): Dimensions of container.
            location (Location): Location of container.

    """

    def __init__(self, type: str, name: str, dimensions: Dimensions):
        super().__init__()
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)
        self.SetLocation(None)

    def SetType(self, type: str) -> None:
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

    def SetName(self, name: str) -> None:
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

    def SetDimensions(self, dimensions: Dimensions) -> None:
        """
        Sets dimensions of the container instance.

        Args:
            dimensions (Dimensions):
                Dimensions assigned to the container instance.
        """
        self.dimensions = dimensions

    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the container instance.

        Returns:
            Dimensions: Dimensions assigned to the container instance.
        """
        return self.dimensions

    def SetLocation(self, location: "Location") -> None:
        """
        Sets container location.

        Args:
            location (Location): New location of container.
        """
        self.location = location

    def GetLocation(self) -> "Location":
        """
        Gets current location of container.

        Return:
            location (Location): Current location of container.
        """
        return self.location

    def Activation(self, cmd: "Command") -> None:
        """
        Activates certain functions based on
        the command type.

        Args:
            cmd (Command): Instance of command to be processed.

        """
        if self.id is not cmd.target.id:
            raise KeyError(
                f"""Target ID {cmd.target.id}
                does not match this instance's ID {self.id}."""
            )
        elif type(cmd) is TransportCmd:
            # Activate components at origin of transport
            current_holdingArea = self.GetLocation().GetHoldingArea()
            current_holdingArea.Activation(cmd)
            current_room = self.GetLocation().GetRoom()
            current_room.Activation(cmd)
            current_facility = self.GetLocation().GetFacility()
            current_facility.Activation(cmd)

            # Activate components at destination of transport
            destination_facility = cmd.destination.GetFacility()
            destination_facility.Activation(cmd)

            destination_room = cmd.destination.GetRoom()
            destination_room.Activation(cmd)

            destination_holdingArea = cmd.destination.GetHoldingArea()
            destination_holdingArea.Activation(cmd)

            # Update own location to destination
            self.SetLocation(cmd.destination)

        super().UpdateHistory(cmd)


class Location:
    """
    A class that specifies the location of an instance
    based on facility, room and holding area.
    Needs at least a facility for initialization.

    Attributes:
        facility (Facility): Corresponding   facility instance.
        room (Room): Corresponding room instance.
        holdingArea (HoldingArea): Corresponding holding area instance.
    """

    def __init__(self, *args):
        if len(args) > 0:
            self.SetFacility(args[0])
        else:
            self.SetFacility(None)
        if len(args) > 1:
            self.SetRoom(args[1])
        else:
            self.SetRoom(None)
        if len(args) > 2:
            self.SetHoldingArea(args[2])
        else:
            self.SetHoldingArea(None)

    def SetFacility(self, facility: Facility) -> None:
        """
        Sets facility.

        Args:
                facility (Facility): Facility instance.
        """
        self.facility = facility

    def GetFacility(self) -> Facility:
        """
        Gets facility.

        Returns:
                facility: Facility instance.
        """
        return self.facility

    def SetRoom(self, room: Room) -> None:
        """
        Sets room.

        Args:
                room (Room): Room instance.
        """
        self.room = room

    def GetRoom(self) -> Room:
        """
        Gets room.

        Returns:
                Room: Room instance.
        """
        return self.room

    def SetHoldingArea(self, holdingArea: HoldingArea):
        """
        Sets holding area.

        Args:
                holdingArea (HoldingArea): Holding area instance.
        """
        self.holdingArea = holdingArea

    def GetHoldingArea(self) -> HoldingArea:
        """
        Gets holding area.

        Returns:
                HodingArea: Holding area instance.
        """
        return self.holdingArea

    def PrintLocation(self) -> None:
        """
        Prints facility and room IDs of location.
        """
        if self.facility is not None:
            print(f"Facility: {self.facility.name}, ID: {self.facility.id}")
        if self.room is not None:
            print(f"Room: {self.room.name}, ID: {self.room.id}")
        if self.holdingArea is not None:
            hAN = self.holdingArea.name
            hAID = self.holdingArea.id
            print(f"Holding Area: {hAN}, ID: {hAID}")


class Command(IDClass):
    """
    The base class for all instances that specify commands.

    Attributes:
        type (str): Type of command.
        target (HistoryClass): Instance that is targeted by command.
    """

    def __init__(self, type: str, target: HistoryClass):
        super().__init__()
        self.SetType(type)
        self.SetTarget(target)

    def SetType(self, type: str) -> None:
        """
        Sets command type.

        Args:
                type (str): Command type.
        """
        self.type = type

    def GetType(self) -> str:
        """
        Gets command type.

        Returns:
                str: Command type.
        """
        return self.type

    def SetTarget(self, target: HistoryClass) -> None:
        """
        Set instance targeted with a command.

        Args:
                target (HistoryClass): Targeted instance.
        """
        self.target = target

    def GetTarget(self) -> HistoryClass:
        """
        Gets instance targeted with a command.

        Returns:
                HistoryClass: Targeted instance.
        """
        return self.target


class TransportCmd(Command):
    """
    A class that specifies a transport command from an origin to a destination.

    Attributes:
        target (HistoryClass): Instance that is targeted by command.
        origin (Location): Origin of transport.
        destination (Location): Destination of transport.
    """

    def __init__(self, target: HistoryClass, origin: Location, destination: Location):
        super().__init__("transport", target)
        self.SetOrigin(origin)
        self.SetDestination(destination)

    def SetOrigin(self, origin: Location) -> None:
        """
        Sets origin of transport.

        Args:
                origin (Location): Origin of transport.
        """
        self.origin = origin

    def GetOrigin(self) -> Location:
        """
        Gets origin of transport.

        Returns:
                Location: Origin of transport.
        """
        return self.origin

    def SetDestination(self, destination: Location) -> None:
        """
        Sets destination of transport.

        Args:
                destination (Location): Destination of transport.
        """
        self.destination = destination

    def GetDestination(self) -> Location:
        """
        Gets destination of transport.

        Returns:
                Location: Destination of transport.
        """
        return self.destination

    def PrintCommand(self) -> None:
        """
        Prints details of transport command.
        """
        print(f"Transport command with target: {self.target}")
        print("Origin:")
        self.origin.PrintLocation()
        print("Destination:")
        self.destination.PrintLocation()
