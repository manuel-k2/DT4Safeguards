from dataclasses import dataclass, field
from typing import ClassVar, Dict
from contextlib import contextmanager
from copy import copy
import json

from model.units import Dimensions, Position


class InstanceNotFoundError(Exception):
    """
    Exception raised when an instance with a
    given ID or given class name is not found.
    """

    pass


class MonitoringSystem:
    """
    A class to monitor all instances listed in a registry indexed by their IDs.

    Attributes:
        _registry (Dict[int, IDClass]):
            Class-level dictionary to store instances
            of IDClass, indexed by integer IDs.
        _id_counter (int): Class-level counter to generate unique IDs.
        _verbosity (int): Class-level verbosity setting.
    """

    _registry: ClassVar[Dict[int, "IDClass"]] = {}
    _id_counter: ClassVar[int] = 0
    _verbosity: ClassVar[int] = 0  # 0: Silent, 1: Verbose

    @classmethod
    def set_verbosity(cls, level: int) -> None:
        """
        Sets the verbosity level.

        Args:
            level (int): Verbosity level (0: Silent, 1: Verbose).
        """
        cls._verbosity = level
    
    @classmethod
    def get_verbosity(cls) -> int:
        """
        Gets the verbosity level.

        Returns:
            int: Verbosity level (0: Silent, 1: Verbose).
        """
        return int(cls._verbosity)

    @classmethod
    def register(cls, instance: "IDClass") -> int:
        """
        Registers an instance in the registry and assigns a unique ID.

        Args:
            instance (IDClass): The instance to be registered.

        Returns:
            int: The unique ID assigned to the instance.
        """
        instance_id = cls._id_counter
        cls._registry[instance_id] = instance
        cls._id_counter += 1
        return instance_id

    @classmethod
    def get_instance(cls, id: int) -> "IDClass":
        """
        Retrieves an instance from the registry by its ID.

        Args:
            id (int): The ID of the instance to retrieve.

        Returns:
            Instance of IDClass if found.

        Raises:
            InstanceNotFoundError: If the instance with the
                given ID is not found.
        """
        if id not in cls._registry:
            if cls.get_verbosity() > 0:
                print(f"Instance with ID '{id}' not found.")
            raise InstanceNotFoundError()
        instance = cls._registry[id]
        if cls.get_verbosity() > 0:
            print(f"Retrieved instance with ID {id}: {instance}")
        return instance

    @classmethod
    def get_instace_by_type(cls, class_type: type) -> Dict[int, 'IDClass']:
        """
        Retrieves a list of all instances from the registry
        that match the given class type.

        Args:
            class_type (type):
                Class type for which instances are retrieved.

        Returns:
            Dict[int, Facility]:
                Dictionary of all registered instances matching class type.
        """
        instance_inventory = {
            id: instance
            for id, instance in cls._registry.items()
            if isinstance(instance, class_type)
        }

        if not instance_inventory:
            print(f"No instances of type '{class_type}' found.")
            raise InstanceNotFoundError()

        if cls.get_verbosity() > 0:
            print(f"Instances of type {class_type.__name__}: ")
            for id, instance in instance_inventory.items():
                print(f"ID: {id}, Instance: {instance}")

        return instance_inventory

    @classmethod
    def display_registry(cls) -> None:
        """
        Displays all instances in the registry.
        """
        if not cls._registry:
            print("Registry is empty.")
        else:
            for id, instance in cls._registry.items():
                print(f"ID: {id}, Instance: {instance}")


@dataclass
class IDClass:
    """
    The base class for all registrable instances
    that get assigned a unique identifier.

    Attributes:
        _id (int): The unique identifier for the instance.
        _verbosity (int): Class-level verbosity setting.
    """

    _id: int = field(init=False)
    _verbosity: ClassVar[int] = 0  # 0: Silent, 1: Verbose

    @classmethod
    def set_verbosity(cls, level: int) -> None:
        """
        Sets the verbosity level.

        Args:
            level (int): Verbosity level (0: Silent, 1: Verbose).
        """
        cls._verbosity = level

    @classmethod
    def get_verbosity(cls) -> int:
        """
        Gets the verbosity level.

        Returns:
            int: Verbosity level (0: Silent, 1: Verbose).
        """
        return int(cls._verbosity)

    def __post_init__(self) -> None:
        """
        Registers the instance in the registry after initialization
        and assigns a unique ID.
        """
        self._id = MonitoringSystem.register(self)
    
    def GetID(self) -> int:
        """
        Gets unique ID of instance.

        Returns:
            id (int): Unique ID of instance.
        """
        return int(self._id)


class HistoryClass(IDClass):
    """
    The base class for all instances that come with a history that
    tracks all changes made to the instance.

    Attributes:
        _history (Dict[int, dict]): Dictionary to store command
            specifications.
    """

    _history: Dict[int, dict] = {}

    def __init__(self):
        super().__init__()

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
                """Activation can only be called
                within Commander.CreateTransportCommand."""
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
        self._history[cmd.GetID()] = {"cmdType": cmd.GetType(), "target": cmd.GetTarget()}

    def GetHistory(self) -> Dict[int, dict]:
        """
        Gets history of instance.

        Returns:
            Dict[int, dict]: History of instance.
        """
        return copy(self._history)

    def ShowHistory(self) -> None:
        """
        Shows history of instance.
        """
        if not self._history:
            print("Registry is empty.")
        else:
            for id, instance in self._history.items():
                print(f"Command with ID: {id}, {instance}")


@dataclass
class Facility(HistoryClass):
    """
    A class that describes a facility.

    Attributes:
        _type (str): Type of facility.
        _name (str): Name of facility.
        _dimensions (Dimensions): Dimensions of facility.
        _position (Position): Position of faility.
        _room_inventory (Dict[int, Room]): Dictionary of rooms that are
            contained in facility.
    """

    _type: str = None
    _name: str = None
    _dimensions: Dimensions = None
    _position: Position = None
    _room_inventory: Dict[int, "Room"] = field(default_factory=dict)

    def __init__(
        self, type: str, name: str, dimensions: Dimensions, position: Position
    ):
        super().__init__()
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)
        self.SetPosition(position)
        self._room_inventory = {}

    def SetType(self, type: str) -> None:
        """
        Sets facility type.

        Args:
            type (str): Facility type.
        """
        self._type: str = type

    def GetType(self) -> str:
        """
        Gets facility type.

        Returns:
            str: Facility type.
        """
        return str(self._type)

    def SetName(self, name: str) -> None:
        """
        Sets facility name.

        Args:
            name (str): Facility name.
        """
        self._name: str = name

    def GetName(self) -> str:
        """
        Gets facility name.

        Returns:
            str: Facility name.
        """
        return str(self._name)

    def SetDimensions(self, dimensions: Dimensions) -> None:
        """
        Sets dimensions of the facility instance.

        Args:
            dimensions (Dimensions):
                Dimensions assigned to the facility instance.
        """
        self._dimensions: Dimensions = dimensions

    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the facility instance.

        Returns:
            Dimensions: Dimensions assigned to the facility instance.
        """
        return copy(self._dimensions)

    def SetPosition(self, position: Position) -> None:
        """
        Sets cartesian position of facility instance.

        Args:
            position (Position):
                Position assigned to facility instance.
        """
        self._position: Position = position

    def GetPosition(self) -> Position:
        """
        Gets position of facility instance.

        Returns:
            Position: Position assigned to facility instance.
        """
        return copy(self._position)

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
        self._room_inventory[room.GetID()] = room

    def RemoveRoom(self, roomID: int) -> None:
        """
        Removes a room from the facility's room inventory.

        Args:
            roomID (int): ID of room to be removed from inventory.
        """
        if roomID not in self._room_inventory:
            raise KeyError(f"Room with ID {roomID} not found.")
        if len(self._room_inventory) == 1 and roomID in self._room_inventory:
            self._room_inventory.clear()
        else:
            del self._room_inventory[roomID]

    def GetRoomInventory(self) -> Dict[int, "Room"]:
        """
        Gets the facility's room inventory.

        Returns:
            Dict[int, Room]: Dictionary of rooms that are contained
                in facility.
        """
        if IDClass.get_verbosity() > 0:
            if not self._room_inventory:
                print("Inventory is empty.")
            else:
                for id, room in self._room_inventory.items():
                    print(f"ID: {id}, Room: {room.GetName()}")
        return copy(self._room_inventory)

    def PresentEntryInventory(self):
        pass


@dataclass
class Room(HistoryClass):
    """
    A class that describes a room.

    Attributes:
        _type (str): Type of room.
        _name (str): Name of room.
        _dimensions (Dimensions): Dimensions of room.
        _position (Position): Position of room.
        _location (Location): Location of room.
        _holdingarea_inventory (Dict[int, HoldingArea]): Dictionary of
            holding areas that are contained in room.
    """

    _type: str = None
    _name: str = None
    _dimensions: Dimensions = None
    _position: Position = None
    _location: 'Location' = None
    _holdingArea_inventory: Dict[int, "HoldingArea"] = field(
        default_factory=dict
    )

    def __init__(
        self, type: str, name: str, dimensions: Dimensions, position: Position
    ):
        super().__init__()
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)
        self.SetPosition(position)
        self._holdingArea_inventory = {}

    def SetType(self, type: str) -> None:
        """
        Sets room type.

        Args:
            type (str): Room type.
        """
        self._type: str = type

    def GetType(self) -> str:
        """
        Gets room type.

        Returns:
            str: Room type.
        """
        return str(self._type)

    def SetName(self, name: str) -> None:
        """
        Sets room name.

        Args:
            name (str): Room name.
        """
        self._name: str = name

    def GetName(self) -> str:
        """
        Gets room name.

        Returns:
            str: Room name.
        """
        return str(self._name)

    def SetDimensions(self, dimensions: Dimensions) -> None:
        """
        Sets dimensions of the room instance.

        Args:
            dimensions (Dimensions): Dimensions assigned to the room instance.
        """
        self._dimensions: Dimensions = dimensions

    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the room instance.

        Returns:
            Dimensions: Dimensions assigned to the room instance.
        """
        return copy(self._dimensions)

    def SetLocation(self, location: 'Location') -> None:
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
            self._location: Location = location

    def GetLocation(self) -> 'Location':
        """
        Gets location of room instance.

        Return:
            location (Location): Location of room.
        """
        return copy(self._location)

    def SetPosition(self, position: Position) -> None:
        """
        Sets cartesian position of room instance.

        Args:
            position (Position):
                Position assigned to room instance.
        """
        self._position: Position = position

    def GetPosition(self) -> Position:
        """
        Gets position of room instance.

        Returns:
            Position: Position assigned to room instance.
        """
        return copy(self._position)

    def AddHoldingArea(self, holdingArea: "HoldingArea") -> None:
        """
        Adds a holding area to the rooms's holding area inventory.

        Args:
            holdingArea (HoldingArea):
                Holding area to be added to inventory.
        """
        # Set new location to added holding area
        holdingArea_location = Location(self._location.GetFacility(), self)
        holdingArea.SetLocation(holdingArea_location)

        # Add holding area to inventory
        self._holdingArea_inventory[holdingArea.GetID()] = holdingArea

    def RemoveHoldingArea(self, holdingAreaID: int) -> None:
        """
        Removes a holding area from the rooms's holding area inventory.

        Args:
            holdingAreaID (int):
                ID of holding area to be removed from inventory.
        """
        if holdingAreaID not in self._holdingArea_inventory:
            raise KeyError(f"Holding area with ID {holdingAreaID} not found.")
        if (
            len(self._holdingArea_inventory) == 1
            and holdingAreaID in self._holdingArea_inventory
        ):
            self._holdingArea_inventory.clear()
        else:
            del self._holdingArea_inventory[holdingAreaID]

    def GetHoldingAreaInventory(self) -> Dict[int, "HoldingArea"]:
        """
        Gets the room's holding area inventory.

        Returns:
            Dict[int, HoldingArea]:
                Dictionary of holding areas that are contained in room.
        """
        if IDClass.get_verbosity() > 0:
            if not self._holdingArea_inventory:
                print("Inventory is empty.")
            else:
                for id, holdingArea in self._holdingArea_inventory.items():
                    print(f"Holding area: {holdingArea.GetName()}, ID: {id}")
        return copy(self._holdingArea_inventory)

    def CheckForEquipment(self):
        pass

    def PresentExitInventory(self):
        pass


@dataclass
class HoldingArea(HistoryClass):
    """
    A class that describes a holding area for containers.
    Each holding area may contain one container.

    Attributes:
        _name (str): Name of holding area.
        _position (Position): Position of holding area.
        _location (Location): Location of holding area.
        _occupationStatus (bool):
            True if holding area is occupied by container, False if not.
        _container_inventory (Dict[int, Container]):
            Dictionary of container in holding area.
    """

    _name: str = None
    _position: Position = None
    _location: 'Location' = None
    _container_inventory: Dict[int, 'Container'] = field(default_factory=dict)

    def __init__(self, name: str, position: Position):
        super().__init__()
        self.SetName(name)
        self.SetOccupationStatus(False)
        self.SetPosition(position)
        self._container_inventory = {}

    def SetName(self, name: str) -> None:
        """
        Sets holding area name.

        Args:
            name (str): Holding area name.
        """
        self._name: str = name

    def GetName(self) -> str:
        """
        Gets holding area name.

        Returns:
            str: Holding area name.
        """
        return str(self._name)

    def SetLocation(self, location: 'Location') -> None:
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
            self._location: Location = location

    def GetLocation(self) -> 'Location':
        """
        Gets location of holding area.

        Return:
            location (Location): Location of holding area.
        """
        return copy(self._location)

    def SetPosition(self, position: Position) -> None:
        """
        Sets cartesian position of holding area instance.

        Args:
            position (Position):
                Position assigned to holding area instance.
        """
        self._position: Position = position

    def GetPosition(self) -> Position:
        """
        Gets position of holding area instance.

        Returns:
            Position: Position assigned to holding area instance.
        """
        return copy(self._position)

    def SetOccupationStatus(self, occupationStatus: bool) -> None:
        """
        Sets occupation status to true or false.

        Args:
            occupationStatus (bool): New occupation status.
        """
        self._occupationStatus = occupationStatus

    def GetOccupationStatus(self) -> bool:
        """
        Gets current occupation status.

        Returns:
            bool: Current occupation status.
        """
        return bool(self._occupationStatus)

    def AddContainer(self, container: 'Container') -> None:
        """
        Adds container to holding area.

        Args:
            container (Container): Container to be added to holding area.
        """
        if self.GetOccupationStatus() is True:
            if IDClass.get_verbosity() > 0:
                print("Holding Area is already occupied.")
        else:
            # Set new location to added container
            container_location = Location(
                self.GetLocation().GetFacility(),
                self.GetLocation().GetRoom(),
                self
            )
            container.SetLocation(container_location)

            # Add container to inventory
            self._container_inventory[container.GetID()] = container
            self.SetOccupationStatus(True)

    def RemoveContainer(self) -> None:
        """
        Removes container from holding area.
        """
        if IDClass.get_verbosity() > 0:
            for id, container in self._container_inventory.items():
                print(
                    f"""ID: {id}, Container: {container}
                    removed from holding area."""
                )
        self._container_inventory.clear()
        self.SetOccupationStatus(False)

    def GetContainer(self) -> 'Container':
        """
        Gets the container contained in holding area.

        Returns:
            Container:
                Container that is contained in holding area.
        """
        if self._occupationStatus is False:
            if IDClass.get_verbosity() > 0:
                print("No container in holding area.")
        else:
            for id, container in self._container_inventory.items():
                if IDClass.get_verbosity() > 0:
                    print(f"Container: {container.GetName()}, ID: {id}")
                return container

    def _activation(self, cmd: "Command") -> None:
        """
        Registers a command passed to this instance and
        activates certain functions based on the command type.

        Args:
            cmd (Command): Instance of command to be processed.
        """
        if type(cmd) is TransportCmd:
            # If holding area is at origin of transport
            if self is cmd.GetOrigin().GetHoldingArea():
                self.RemoveContainer()
            # If holding area is at destination of transport
            if self is cmd.GetDestination().GetHoldingArea():
                self.AddContainer(cmd.GetTarget())

        # Update own history
        super().UpdateHistory(cmd)


@dataclass
class Container(HistoryClass):
    """
    A class that describes a container for nuclear material.

    Attributes:
            _type (str): Type of container.
            _name (str): Name of container.
            _dimensions (Dimensions): Dimensions of container.
            _location (Location): Location of container.

    """

    _type: str = None
    _name: str = None
    _dimensions: Dimensions = None
    _location: 'Location' = None

    def __init__(self, type: str, name: str, dimensions: Dimensions):
        super().__init__()
        self.SetType(type)
        self.SetName(name)
        self.SetDimensions(dimensions)

    def SetType(self, type: str) -> None:
        """
        Sets container type.

        Args:
            type (str): Container type.
        """
        self._type: str = type

    def GetType(self) -> str:
        """
        Gets container type.

        Returns:
            str: Container type.
        """
        return str(self._type)

    def SetName(self, name: str) -> None:
        """
        Sets container name.

        Args:
            name (str): Container name.
        """
        self._name: str = name

    def GetName(self) -> str:
        """
        Gets container name.

        Returns:
            str: Container name.
        """
        return str(self._name)

    def SetDimensions(self, dimensions: Dimensions) -> None:
        """
        Sets dimensions of the container instance.

        Args:
            dimensions (Dimensions):
                Dimensions assigned to the container instance.
        """
        self._dimensions: Dimensions = dimensions

    def GetDimensions(self) -> Dimensions:
        """
        Gets dimensions of the container instance.

        Returns:
            Dimensions: Dimensions assigned to the container instance.
        """
        return copy(self._dimensions)

    def SetLocation(self, location: 'Location') -> None:
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
            self._location: Location = location

    def GetLocation(self) -> 'Location':
        """
        Gets current location of container.

        Return:
            location (Location): Current location of container.
        """
        return copy(self._location)

    def _activation(self, cmd: "Command") -> None:
        """
        Registers a command passed to this instance and
        activates certain functions based on the command type.

        Args:
            cmd (Command): Instance of command to be processed.
        """
        if type(cmd) is TransportCmd:
            # Update own location to destination
            self.SetLocation(cmd.GetDestination())

        # Update own history
        super().UpdateHistory(cmd)


@dataclass
class Location:
    """
    A class that specifies the location of an instance
    based on facility, room and holding area.

    Attributes:
        _facility (Facility): Corresponding   facility instance.
        _room (Room): Corresponding room instance.
        _holdingArea (HoldingArea): Corresponding holding area instance.
    """

    _facility: Facility
    _room: Room
    _holdingArea: HoldingArea

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

    def __repr__(self) -> str:
        """
        Provides a string representation of the Location instance.
        
        Returns:
            str: String representation of the Location instance.
        """
        return (
            f"({self.GetFacility().GetName()}, "
            f"{self.GetRoom().GetName()}, "
            f"{self.GetHoldingArea().GetName()})"
        )

    def SetFacility(self, facility: Facility) -> None:
        """
        Sets facility.

        Args:
                facility (Facility): Facility instance.
        """
        self._facility: Facility = facility

    def GetFacility(self) -> Facility:
        """
        Gets facility.

        Returns:
                facility: Facility instance.
        """
        return self._facility

    def SetRoom(self, room: Room) -> None:
        """
        Sets room.

        Args:
                room (Room): Room instance.
        """
        self._room: Room = room

    def GetRoom(self) -> Room:
        """
        Gets room.

        Returns:
                Room: Room instance.
        """
        return self._room

    def SetHoldingArea(self, holdingArea: HoldingArea) -> None:
        """
        Sets holding area.

        Args:
                holdingArea (HoldingArea): Holding area instance.
        """
        self._holdingArea: HoldingArea = holdingArea

    def GetHoldingArea(self) -> HoldingArea:
        """
        Gets holding area.

        Returns:
                HodingArea: Holding area instance.
        """
        return self._holdingArea

    def PrintLocation(self) -> None:
        """
        Prints facility and room IDs of location.
        """
        if self.GetFacility/() is not None:
            print(f"Facility: {self.GetFacility().GetName()}, ID: {self.GetFacility().GetID()}")
        if self.GetRoom() is not None:
            print(f"Room: {self.GetRoom().GetName()}, ID: {self.GetRoom().GetID()}")
        if self.GetHoldingArea() is not None:
            hAN = self.GetHoldingArea().GetName()
            hAID = self.GetHoldingArea().GetID()
            print(f"Holding Area: {hAN}, ID: {hAID}")


@dataclass
class Command(IDClass):
    """
    The base class for all instances that specify commands.
    All commands are to be directed to the Commander.

    Attributes:
        _type (str): Type of command.
        _target (HistoryClass): Instance that is targeted by command.
    """

    _type: str
    _target: HistoryClass

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
        self._type: str = type

    def GetType(self) -> str:
        """
        Gets command type.

        Returns:
                str: Command type.
        """
        return str(self._type)

    def SetTarget(self, target: HistoryClass) -> None:
        """
        Set instance targeted with a command.

        Args:
                target (HistoryClass): Targeted instance.
        """
        self._target: HistoryClass = target

    def GetTarget(self) -> HistoryClass:
        """
        Gets instance targeted with a command.

        Returns:
                HistoryClass: Targeted instance.
        """
        return self._target


@dataclass
class TransportCmd(Command):
    """
    A class that specifies a transport command from an origin to a destination.

    Attributes:
        target (HistoryClass): Instance that is targeted by command.
        origin (Location): Origin of transport.
        destination (Location): Destination of transport.
    """

    _target: HistoryClass
    _origin: Location
    _destination: Location

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
        self._origin: Location = origin

    def GetOrigin(self) -> Location:
        """
        Gets origin of transport.

        Returns:
                Location: Origin of transport.
        """
        return copy(self._origin)

    def SetDestination(self, destination: Location) -> None:
        """
        Sets destination of transport.

        Args:
                destination (Location): Destination of transport.
        """
        self._destination: Location = destination

    def GetDestination(self) -> Location:
        """
        Gets destination of transport.

        Returns:
                Location: Destination of transport.
        """
        return copy(self._destination)

    def PrintCommand(self) -> None:
        """
        Prints details of transport command.
        """
        print(f"Transport command with target: {self.GetTarget()}")
        print("Origin:")
        self.GetOrigin().PrintLocation()
        print("Destination:")
        self.GetDestination().PrintLocation()


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


@dataclass
class Builder:
    """
    A class that creates instances of physical components and
    uses them to construct a model based on user input.
    """

    def BuildModel(self, model: Dict[str, Dict]) -> None:
        """
        Builds a model on a dictionary-based
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

        for _facility, facility_stats in model.items():
            facilityInstance = Facility(
                type=facility_stats["type"],
                name=facility_stats["name"],
                dimensions=Dimensions(
                    facility_stats["dimensions"]["dx"],
                    facility_stats["dimensions"]["dy"],
                    facility_stats["dimensions"]["dx"],
                ),
                position=Position(
                    facility_stats["position"]["x"],
                    facility_stats["position"]["y"],
                    facility_stats["position"]["z"],
                ),
            )

            # Initialize room with data from dictionary
            #       Facility MUST contain at least one room.
            if not facility_stats["rooms"]:
                raise KeyError("Facility must contain at least one room.")

            model_2: Dict[str, Dict] = facility_stats["rooms"]
            for _room, room_stats in model_2.items():
                roomInstance = Room(
                    type=room_stats["type"],
                    name=room_stats["name"],
                    dimensions=Dimensions(
                        room_stats["dimensions"]["dx"],
                        room_stats["dimensions"]["dy"],
                        room_stats["dimensions"]["dx"],
                    ),
                    position=Position(
                        room_stats["position"]["x"],
                        room_stats["position"]["y"],
                        room_stats["position"]["z"],
                    ),
                )

                # Add room to facility
                facilityInstance.AddRoom(roomInstance)

                if len(room_stats) > 4:
                    # Initialize holding area with data from dictionary
                    #       Room MAY contain holding areas.
                    model_3: Dict[str, Dict] = room_stats["holdingAreas"]
                    for _holdingArea, holdingArea_stats in model_3.items():
                        holdingAreaInstance = HoldingArea(
                            name=holdingArea_stats["name"],
                            position=Position(
                                holdingArea_stats["position"]["x"],
                                holdingArea_stats["position"]["y"],
                                holdingArea_stats["position"]["z"],
                            ),
                        )

                        # Add holding area to room
                        roomInstance.AddHoldingArea(holdingAreaInstance)

                        # Initialize container with data from dictionary
                        #       Holding area MAY contain a container.
                        if len(holdingArea_stats) > 2:
                            model_4: Dict = holdingArea_stats["container"]
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

        if MonitoringSystem.get_verbosity() > 0:
            print("\nAll registered instances:")
            MonitoringSystem.display_registry()

    def GetModel(self) -> Dict[str, Dict]:
        """
        Gets current state of model as
        model dictionary and adjacency matrix.

        Returns:
            Dict[str, Dict]:
                Dictionary containing names and structure of
                facilities, rooms and holding areas.
            :
                Matrix specifying adjacency for rooms
                through entries and exits.
        """
        model: Dict[str, Dict] = {}

        # Get facilities from registry and write stats into dictionary
        faciliy_inventory: Dict[int, Facility] = (
            MonitoringSystem.get_instace_by_type(Facility)
        )
        i: int = 1
        for _id, facility in faciliy_inventory.items():
            model["facility " + str(i)] = {
                "type": facility.GetType(),
                "name": facility.GetName(),
                "dimensions": {
                    "dx": facility.GetDimensions().GetX(),
                    "dy": facility.GetDimensions().GetY(),
                    "dz": facility.GetDimensions().GetZ(),
                },
                "position": {
                    "x": facility.GetPosition().GetX(),
                    "y": facility.GetPosition().GetY(),
                    "z": facility.GetPosition().GetZ(),
                },
            }

            # Get Rooms
            room_inventory: Dict[int, Room] = facility.GetRoomInventory()
            model["facility " + str(i)]["rooms"] = {}
            j: int = 1
            for _id, room in room_inventory.items():
                model["facility " + str(i)]["rooms"]["room " + str(j)] = {
                    "type": room.GetType(),
                    "name": room.GetName(),
                    "dimensions": {
                        "dx": room.GetDimensions().GetX(),
                        "dy": room.GetDimensions().GetY(),
                        "dz": room.GetDimensions().GetZ(),
                    },
                    "position": {
                        "x": room.GetPosition().GetX(),
                        "y": room.GetPosition().GetY(),
                        "z": room.GetPosition().GetZ(),
                    },
                }

                # Get Holding areas (if any)
                holdingArea_inventory: Dict[int, HoldingArea] = (
                    room.GetHoldingAreaInventory()
                )
                if holdingArea_inventory:
                    model["facility " + str(i)]["rooms"]["room " + str(j)][
                        "holdingAreas"
                    ] = {}
                    k: int = 1
                    for _id, holdingArea in holdingArea_inventory.items():
                        model["facility " + str(i)]["rooms"]["room " + str(j)][
                            "holdingAreas"
                        ]["holdingArea " + str(k)] = {
                            "name": holdingArea.GetName(),
                            "position": {
                                "x": holdingArea.GetPosition().GetX(),
                                "y": holdingArea.GetPosition().GetY(),
                                "z": holdingArea.GetPosition().GetZ(),
                            },
                        }

                        # Get Container (if any)
                        container: Container = holdingArea.GetContainer()
                        if container:
                            model["facility " + str(i)]["rooms"][
                                "room " + str(j)
                            ]["holdingAreas"]["holdingArea " + str(k)][
                                "container"
                            ] = {
                                "type": container.GetType(),
                                "name": container.GetName(),
                                "dimensions": {
                                    "dx": container.GetDimensions().GetX(),
                                    "dy": container.GetDimensions().GetY(),
                                    "dz": container.GetDimensions().GetZ(),
                                },
                            }
                        k += 1
                    k = 1
                j += 1
            j = 1
            i += 1
        return model

    def LoadDummyModel(self) -> Dict[str, Dict]:
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

    def LoadModelFromFile(self, filePath: str) -> Dict[str, Dict]:
        """
        Creates a model based on a file in JSON format.
        See data/dummy_model.json for syntax.

        Args:
            filePath (str):
                Relative or absolute path to json file with model data.

        Returns:
            Dict[str, Dict]: Dictionary with model data.
        """
        try:
            with open(filePath) as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            if MonitoringSystem.get_verbosity() > 0:
                print(f"Error: The file '{filePath}' was not found.")
            return None
        except json.JSONDecodeError:
            if MonitoringSystem.get_verbosity() > 0:
                print(f"Error: The file '{filePath}' is not a valid JSON.")
            return None

    def ExportModelToFile(self, model: Dict[str, Dict], filePath: str) -> None:
        """
        Creates a JSON file with model information.

        Args:
            model (Dict[str, Dict]):
                Dictionary that is to be exported to JSON file.
            filePath (str):
                Relative or absolute path to json file with model data.
        """
        try:
            with open(filePath, "w") as file:
                json.dump(model, file, indent=4)
            if MonitoringSystem.get_verbosity() > 0:
                print(f"Model successfully saved to {filePath}.")
        except OSError as e:
            if MonitoringSystem.get_verbosity() > 0:
                print(
                    f"""An error occurred while
                    saving the model to {filePath}: {e}"""
                )

    def CreateModelManually(self) -> Dict[str, Dict]:
        """
        Creates a model manually based on user prompts.

        Returns:
            Dict[str, Dict]: Dictionary with model data.
        """
        pass

    def LoadDummyAdjacencyMatrix(self):
        """
        Creates dummy adjaceny matrix for dummy model data.
        """
        pass
