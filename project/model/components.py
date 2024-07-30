from dataclasses import dataclass
from typing import Dict
from contextlib import contextmanager

from model.monitoringsystem import MonitoringSystem, IDClass

from projecttypes.units import Dimensions, Position


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

    def Activation(self, cmd: "Command", caller: "Commander") -> None:
        """
        Public activation function that ensures caller's identity before
        before calling private activation function.

        Args:
            cmd (Command): Instance of command that is meant to be processed.
            caller (Commander):
                Caller that needs to be instance of Commander class.
        """
        if caller != Commander._authorized_commander:
            raise PermissionError(
                "Activation can only be called within CreateTransportCommand."
            )
        self._activation(cmd)

    def _activation(self, cmd: "Command") -> None:
        """
        Registers a command passed to this instance and
        activates certain functions based on the command type.

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
        Gets history of instance.

        Returns:
            Dict[int, dict]: History of instance.
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

    def __init__(
        self, type: str, name: str, dimensions: Dimensions, position: Position
    ):
        super().__init__()
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)
        self.SetPosition(position)
        self.room_inventory: Dict[int, "Room"] = {}

    def SetType(self, type: str) -> None:
        """
        Sets facility type.

        Args:
            type (str): Facility type.
        """
        self.type: str = type

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
        self.name: str = name

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
        self.dimensions: Dimensions = dimensions

    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the facility instance.

        Returns:
            Dimensions: Dimensions assigned to the facility instance.
        """
        return self.dimensions

    def SetPosition(self, position: Position) -> None:
        """
        Sets cartesian position of facility instance.

        Args:
            position (Position):
                Position assigned to facility instance.
        """
        self.position: Position = position

    def GetPosition(self) -> Position:
        """
        Gets position of facility instance.

        Returns:
            Position: Position assigned to facility instance.
        """
        return self.position

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

    def __init__(
        self, type: str, name: str, dimensions: Dimensions, position: Position
    ):
        super().__init__()
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)
        self.location: Location = None
        self.SetPosition(position)
        self.holdingArea_inventory: Dict[int, "HoldingArea"] = {}

    def SetType(self, type: str) -> None:
        """
        Sets room type.

        Args:
            type (str): Room type.
        """
        self.type: str = type

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
        self.name: str = name

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
        self.dimensions: Dimensions = dimensions

    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the room instance.

        Returns:
            Dimensions: Dimensions assigned to the room instance.
        """
        return self.dimensions

    def SetLocation(self, location: "Location") -> None:
        """
        Sets room location room.
        Called when added to a facility.

        Args:
            location (Location): Location of room.
        """
        if location.GetFacility() is None:
            raise KeyError("Facility must not be NoneType.")
        elif location.GetRoom() is not None:
            raise KeyError("Room must be NoneType.")
        elif location.GetHoldingArea() is not None:
            raise KeyError("Holding area must be NoneType.")
        else:
            self.location: Location = location

    def GetLocation(self) -> "Location":
        """
        Gets location of room instance.

        Return:
            location (Location): Location of room.
        """
        return self.location

    def SetPosition(self, position: Position) -> None:
        """
        Sets cartesian position of room instance.

        Args:
            position (Position):
                Position assigned to room instance.
        """
        self.position: Position = position

    def GetPosition(self) -> Position:
        """
        Gets position of room instance.

        Returns:
            Position: Position assigned to room instance.
        """
        return self.position

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

    def __init__(self, name: str, position: Position):
        super().__init__()
        self.SetName(name)
        self.SetOccupationStatus(False)
        self.location: Location = None
        self.SetPosition(position)
        self.container_inventory: Dict[int, "Container"] = {}

    def SetName(self, name: str) -> None:
        """
        Sets holding area name.

        Args:
            name (str): Holding area name.
        """
        self.name: str = name

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
        if location.GetFacility() is None:
            raise KeyError("Facility must not be NoneType.")
        elif location.GetRoom() is None:
            raise KeyError("Room must not be NoneType.")
        elif location.GetHoldingArea() is not None:
            raise KeyError("Holding area must be NoneType.")
        else:
            self.location: Location = location

    def GetLocation(self) -> "Location":
        """
        Gets location of holding area.

        Return:
            location (Location): Location of holding area.
        """
        return self.location

    def SetPosition(self, position: Position) -> None:
        """
        Sets cartesian position of holding area instance.

        Args:
            position (Position):
                Position assigned to holding area instance.
        """
        self.position: Position = position

    def GetPosition(self) -> Position:
        """
        Gets position of holding area instance.

        Returns:
            Position: Position assigned to holding area instance.
        """
        return self.position

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
        self.location: Location = None

    def SetType(self, type: str) -> None:
        """
        Sets container type.

        Args:
            type (str): Container type.
        """
        self.type: str = type

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
        self.name: str = name

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
        self.dimensions: Dimensions = dimensions

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
        if location.GetFacility() is None:
            raise KeyError("Facility must not be NoneType.")
        elif location.GetRoom() is None:
            raise KeyError("Room must not be NoneType.")
        elif location.GetHoldingArea() is None:
            raise KeyError("Holding area must not be NoneType.")
        else:
            self.location: Location = location

    def GetLocation(self) -> "Location":
        """
        Gets current location of container.

        Return:
            location (Location): Current location of container.
        """
        return self.location

    def _activation(self, cmd: "Command") -> None:
        """
        Registers a command passed to this instance and
        activates certain functions based on the command type.

        Args:
            cmd (Command): Instance of command to be processed.
        """
        if type(cmd) is TransportCmd:
            # Update own location to destination
            self.SetLocation(cmd.destination)

        # Update own history
        super().UpdateHistory(cmd)


class Location:
    """
    A class that specifies the location of an instance
    based on facility, room and holding area.

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
        self.facility: Facility = facility

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
        self.room: Room = room

    def GetRoom(self) -> Room:
        """
        Gets room.

        Returns:
                Room: Room instance.
        """
        return self.room

    def SetHoldingArea(self, holdingArea: HoldingArea) -> None:
        """
        Sets holding area.

        Args:
                holdingArea (HoldingArea): Holding area instance.
        """
        self.holdingArea: HoldingArea = holdingArea

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
    All commands are to be directed to the Commander.

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
        self.type: str = type

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
        self.target: HistoryClass = target

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

    def __init__(
        self, target: HistoryClass, origin: Location, destination: Location
    ):
        super().__init__("transport", target)
        self.SetOrigin(origin)
        self.SetDestination(destination)

    def SetOrigin(self, origin: Location) -> None:
        """
        Sets origin of transport.

        Args:
                origin (Location): Origin of transport.
        """
        self.origin: Location = origin

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
        self.destination: Location = destination

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


class Commander:
    """
    A class that creates commands based on user input.
    """

    _authorized_commander = None

    @contextmanager
    def _authorize(self):
        old_commander = Commander._authorized_commander
        Commander._authorized_commander = self
        try:
            yield
        finally:
            Commander._authorized_commander = old_commander

    def IssueTransportCommand(
        self, target: Container, origin: Location, destination: Location
    ) -> None:
        """
        Creates transport command instance and sends it to target container.

        Args:
            target (Container): Targeted container instance.
            origin (Location): Origin of transport.
            destination (Location): Destination of transport.
        """
        # Check that origin Location matches current position of target
        if origin.GetFacility() is not target.GetLocation().GetFacility():
            raise KeyError(
                "Origin Facility must be same as target's current Facility."
            )
        if origin.GetRoom() is not target.GetLocation().GetRoom():
            raise KeyError(
                "Origin Room must be same as target's current Room."
            )
        if (
            origin.GetHoldingArea()
            is not target.GetLocation().GetHoldingArea()
        ):
            raise KeyError(
                """Origin Holding area must be the same
                as target's current Holding area."""
            )
        # Check that destination Location does not contain NoneTypes
        elif not destination.GetFacility():
            raise KeyError("Destination Facility must not be NoneType.")
        elif not destination.GetRoom():
            raise KeyError("Destination Room must not be NoneType.")
        elif not destination.GetHoldingArea():
            raise KeyError("Destination Holding area must not be NoneType.")
        else:
            # Create Command
            cmd = TransportCmd(target, origin, destination)

            with self._authorize():
                # Activate components at origin of transport
                current_holdingArea = target.GetLocation().GetHoldingArea()
                current_holdingArea.Activation(cmd, self)
                current_room = target.GetLocation().GetRoom()
                current_room.Activation(cmd, self)
                current_facility = target.GetLocation().GetFacility()
                current_facility.Activation(cmd, self)

                # Activate components at destination of transport
                destination_facility = destination.GetFacility()
                destination_facility.Activation(cmd, self)
                destination_room = destination.GetRoom()
                destination_room.Activation(cmd, self)
                destination_holdingArea = destination.GetHoldingArea()
                destination_holdingArea.Activation(cmd, self)

                # Activate target
                target.Activation(cmd, self)


class Builder:
    """
    A class that creates instances of physical components and
    uses them to construct a model based on user input.
    """

    def BuildModel(self, model: Dict[str, Dict]) -> None:
        """
        Builds a model based on a dictionary-based
        input and an adjacency matrix.

        Args:
            model (Dict[str, Dict]):
                Dictionary containing names and structure of
                facilities, rooms and holding areas.
            adjacency ():
                Matrix specifying adjacency for rooms
                through entries and exits.
        """

        # Initialize facility with data from dictionary
        #       Model MUST contain at least one facility.
        if not model:
            raise KeyError("Model must contain at least one facility.")

        for _facility, stats in model.items():
            facilityInstance = Facility(
                type=stats["type"],
                name=stats["name"],
                dimensions=Dimensions(
                    stats["dimensions"]["dx"],
                    stats["dimensions"]["dy"],
                    stats["dimensions"]["dx"],
                ),
                position=Position(
                    stats["position"]["x"],
                    stats["position"]["y"],
                    stats["position"]["z"],
                ),
            )

            # Initialize room with data from dictionary
            #       Facility MUST contain at least one room.
            if not stats["rooms"]:
                raise KeyError("Facility must contain at least one room.")

            model_2: Dict[str, Dict] = stats["rooms"]
            for _room, stats_2 in model_2.items():
                roomInstance = Room(
                    type=stats_2["type"],
                    name=stats_2["name"],
                    dimensions=Dimensions(
                        stats_2["dimensions"]["dx"],
                        stats_2["dimensions"]["dy"],
                        stats_2["dimensions"]["dx"],
                    ),
                    position=Position(
                        stats_2["position"]["x"],
                        stats_2["position"]["y"],
                        stats_2["position"]["z"],
                    ),
                )

                # Add room to facility
                facilityInstance.AddRoom(roomInstance)

                if len(stats_2) > 4:
                    # Initialize holding area with data from dictionary
                    #       Room MAY contain holding areas.
                    model_3: Dict[str, Dict] = stats_2["holdingAreas"]
                    for _holdingArea, stats_3 in model_3.items():
                        holdingAreaInstance = HoldingArea(
                            name=stats_3["name"],
                            position=Position(
                                stats_3["position"]["x"],
                                stats_3["position"]["y"],
                                stats_3["position"]["z"],
                            ),
                        )

                        # Add holding area to room
                        roomInstance.AddHoldingArea(holdingAreaInstance)

                        # Initialize container with data from dictionary
                        #       Holding area MAY contain a container.
                        if len(stats_3) > 2:
                            model_4: Dict = stats_3["container"]
                            containerInstance = Container(
                                type=model_4["type"],
                                name=model_4["name"],
                                dimensions=Dimensions(
                                    model_4["dimensions"]["dx"],
                                    model_4["dimensions"]["dy"],
                                    model_4["dimensions"]["dx"],
                                ),
                            )

                            # Add container to holding area
                            holdingAreaInstance.AddContainer(containerInstance)

        print("\nComplete registry:")
        MonitoringSystem.display_registry()

    def CreateDummyModel(self) -> Dict[str, Dict]:
        """
        Creates a dictionary with dummy model data.

        Returns:
            Dict[str, Dict]: Dictionary with dummy model data.
        """
        dummy_model = {
            "facility 1": {
                "type": "Interim storage",
                "name": "Facility 1",
                "dimensions": {"dx": 1.0, "dy": 1.0, "dz": 1.0},
                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                "rooms": {
                    "room 1": {
                        "type": "Storage",
                        "name": "Room 1",
                        "dimensions": {"dx": 1.0, "dy": 1.0, "dz": 1.0},
                        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                        "holdingAreas": {
                            "holdingArea 1": {
                                "name": "HoldingArea 1",
                                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                                "container": {
                                    "type": "Castor",
                                    "name": "Container 1",
                                    "dimensions": {
                                        "dx": 1.0,
                                        "dy": 1.0,
                                        "dz": 1.0,
                                    },
                                },
                            },
                            "holdingArea 2": {
                                "name": "HoldingArea 2",
                                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                            },
                        },
                    },
                    "room 2": {
                        "type": "Storage",
                        "name": "Room 1",
                        "dimensions": {"dx": 1.0, "dy": 1.0, "dz": 1.0},
                        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                        "holdingAreas": {
                            "holdingArea 1": {
                                "name": "HoldingArea 1",
                                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                            }
                        },
                    },
                },
            },
            "facility 2": {
                "type": "Geological repository",
                "name": "Facility 2",
                "dimensions": {"dx": 1.0, "dy": 1.0, "dz": 1.0},
                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                "rooms": {
                    "room 1": {
                        "type": "Shaft",
                        "name": "Room 1",
                        "dimensions": {"dx": 1.0, "dy": 1.0, "dz": 1.0},
                        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                    },
                    "room 2": {
                        "type": "Drift",
                        "name": "Room 2",
                        "dimensions": {"dx": 1.0, "dy": 1.0, "dz": 1.0},
                        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                        "holdingAreas": {
                            "holdingArea 1": {
                                "name": "HoldingArea 1",
                                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                            }
                        },
                    },
                },
            },
        }
        return dummy_model
    
    def CreateModelManually(self) -> Dict[str, Dict]:
        """
        Creates a model manually based on user prompts.

        Returns:
            Dict[str, Dict]: Dictionary with model data.
        """
        pass
    
    def CreateModelFromFile(self, path: str) -> Dict[str, Dict]:
        """
        Creates a model based on a json file.
        See dummy model for syntax. 

        Args:
            parth (str): Absolute path to file with model data.

        Returns:
            Dict[str, Dict]: Dictionary with model data.
        """
        pass

    def CreateDummyAdjacencyMatrix(self):
        """
        Creates dummy adjaceny matrix for dummy model data.
        """
        pass
