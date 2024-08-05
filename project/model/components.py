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
    def get_instace_by_type(cls, class_type: type) -> Dict[int, "IDClass"]:
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

    def get_id(self) -> int:
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

    def activation(self, cmd: "Command", caller: "Commander") -> None:
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
        self.update_history(cmd)

    def update_history(self, cmd: "Command") -> None:
        """
        Stores command specifications in a dictionary.

        Args:
            cmd (Command): Instance of command to be processed.
        """
        self._history[cmd.get_id()] = {
            "cmdType": cmd.get_type(),
            "target": cmd.get_target(),
        }

    def get_history(self) -> Dict[int, dict]:
        """
        Gets history of instance.

        Returns:
            Dict[int, dict]: History of instance.
        """
        return copy(self._history)

    def print_history(self) -> None:
        """
        Prints history of instance.
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
        self.set_type(type)
        self.set_name(name)
        self.set_dimensions(dimensions)
        self.set_position(position)
        self._room_inventory = {}

    def set_type(self, type: str) -> None:
        """
        Sets facility type.

        Args:
            type (str): Facility type.
        """
        self._type: str = type

    def get_type(self) -> str:
        """
        Gets facility type.

        Returns:
            str: Facility type.
        """
        return str(self._type)

    def set_name(self, name: str) -> None:
        """
        Sets facility name.

        Args:
            name (str): Facility name.
        """
        self._name: str = name

    def get_name(self) -> str:
        """
        Gets facility name.

        Returns:
            str: Facility name.
        """
        return str(self._name)

    def set_dimensions(self, dimensions: Dimensions) -> None:
        """
        Sets dimensions of the facility instance.

        Args:
            dimensions (Dimensions):
                Dimensions assigned to the facility instance.
        """
        self._dimensions: Dimensions = dimensions

    def get_dimensions(self) -> Dimensions:
        """
        Gets dimensions of the facility instance.

        Returns:
            Dimensions: Dimensions assigned to the facility instance.
        """
        return copy(self._dimensions)

    def set_position(self, position: Position) -> None:
        """
        Sets cartesian position of facility instance.

        Args:
            position (Position):
                Position assigned to facility instance.
        """
        self._position: Position = position

    def get_position(self) -> Position:
        """
        Gets position of facility instance.

        Returns:
            Position: Position assigned to facility instance.
        """
        return copy(self._position)

    def add_room(self, room: "Room") -> None:
        """
        Adds a room to the facility's room inventory.

        Args:
            room (Room): Room to be added to inventory.
        """
        # Set new location to added room
        room_location = Location(self)
        room.set_location(room_location)

        # Add room to inventory
        self._room_inventory[room.get_id()] = room

    def remove_room(self, roomID: int) -> None:
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

    def get_room_inventory(self) -> Dict[int, "Room"]:
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
                    print(f"ID: {id}, Room: {room.get_name()}")
        return copy(self._room_inventory)


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
    _location: "Location" = None
    _holding_area_inventory: Dict[int, "HoldingArea"] = field(
        default_factory=dict
    )

    def __init__(
        self, type: str, name: str, dimensions: Dimensions, position: Position
    ):
        super().__init__()
        self.set_type(type)
        self.set_name(name)
        self.set_dimensions(dimensions)
        self.set_position(position)
        self._holding_area_inventory = {}

    def set_type(self, type: str) -> None:
        """
        Sets room type.

        Args:
            type (str): Room type.
        """
        self._type: str = type

    def get_type(self) -> str:
        """
        Gets room type.

        Returns:
            str: Room type.
        """
        return str(self._type)

    def set_name(self, name: str) -> None:
        """
        Sets room name.

        Args:
            name (str): Room name.
        """
        self._name: str = name

    def get_name(self) -> str:
        """
        Gets room name.

        Returns:
            str: Room name.
        """
        return str(self._name)

    def set_dimensions(self, dimensions: Dimensions) -> None:
        """
        Sets dimensions of the room instance.

        Args:
            dimensions (Dimensions): Dimensions assigned to the room instance.
        """
        self._dimensions: Dimensions = dimensions

    def get_dimensions(self) -> Dimensions:
        """
        Gets dimensions of the room instance.

        Returns:
            Dimensions: Dimensions assigned to the room instance.
        """
        return copy(self._dimensions)

    def set_location(self, location: "Location") -> None:
        """
        Sets room location room.
        Called when added to a facility.

        Args:
            location (Location): Location of room.
        """
        if location.get_facility() is None:
            raise KeyError("Facility must not be NoneType.")
        elif location.get_room() is not None:
            raise KeyError("Room must be NoneType.")
        elif location.get_holding_area() is not None:
            raise KeyError("Holding area must be NoneType.")
        else:
            self._location: Location = location

    def get_location(self) -> "Location":
        """
        Gets location of room instance.

        Return:
            location (Location): Location of room.
        """
        return copy(self._location)

    def set_position(self, position: Position) -> None:
        """
        Sets cartesian position of room instance.

        Args:
            position (Position):
                Position assigned to room instance.
        """
        self._position: Position = position

    def get_position(self) -> Position:
        """
        Gets position of room instance.

        Returns:
            Position: Position assigned to room instance.
        """
        return copy(self._position)

    def add_holding_area(self, holding_area: "HoldingArea") -> None:
        """
        Adds a holding area to the rooms's holding area inventory.

        Args:
            holding_area (HoldingArea):
                Holding area to be added to inventory.
        """
        # Set new location to added holding area
        holding_area_location = Location(self._location.get_facility(), self)
        holding_area.set_location(holding_area_location)

        # Add holding area to inventory
        self._holding_area_inventory[holding_area.get_id()] = holding_area

    def remove_holding_area(self, holding_areaID: int) -> None:
        """
        Removes a holding area from the rooms's holding area inventory.

        Args:
            holding_areaID (int):
                ID of holding area to be removed from inventory.
        """
        if holding_areaID not in self._holding_area_inventory:
            raise KeyError(f"Holding area with ID {holding_areaID} not found.")
        if (
            len(self._holding_area_inventory) == 1
            and holding_areaID in self._holding_area_inventory
        ):
            self._holding_area_inventory.clear()
        else:
            del self._holding_area_inventory[holding_areaID]

    def get_holding_area_inventory(self) -> Dict[int, "HoldingArea"]:
        """
        Gets the room's holding area inventory.

        Returns:
            Dict[int, HoldingArea]:
                Dictionary of holding areas that are contained in room.
        """
        if IDClass.get_verbosity() > 0:
            if not self._holding_area_inventory:
                print("Inventory is empty.")
            else:
                for id, holding_area in self._holding_area_inventory.items():
                    print(f"Holding area: {holding_area.get_name()}, ID: {id}")
        return copy(self._holding_area_inventory)


@dataclass
class HoldingArea(HistoryClass):
    """
    A class that describes a holding area for containers.
    Each holding area may contain one container.

    Attributes:
        _name (str): Name of holding area.
        _position (Position): Position of holding area.
        _location (Location): Location of holding area.
        _occupation_status (bool):
            True if holding area is occupied by container, False if not.
        _container_inventory (Dict[int, Container]):
            Dictionary of container in holding area.
    """

    _name: str = None
    _position: Position = None
    _location: "Location" = None
    _container_inventory: Dict[int, "Container"] = field(default_factory=dict)

    def __init__(self, name: str, position: Position):
        super().__init__()
        self.set_name(name)
        self.set_occupation_status(False)
        self.set_position(position)
        self._container_inventory = {}

    def set_name(self, name: str) -> None:
        """
        Sets holding area name.

        Args:
            name (str): Holding area name.
        """
        self._name: str = name

    def get_name(self) -> str:
        """
        Gets holding area name.

        Returns:
            str: Holding area name.
        """
        return str(self._name)

    def set_location(self, location: "Location") -> None:
        """
        Sets holding area location. Called when added to room.

        Args:
            location (Location): Location of holding area.
        """
        if location.get_facility() is None:
            raise KeyError("Facility must not be NoneType.")
        elif location.get_room() is None:
            raise KeyError("Room must not be NoneType.")
        elif location.get_holding_area() is not None:
            raise KeyError("Holding area must be NoneType.")
        else:
            self._location: Location = location

    def get_location(self) -> "Location":
        """
        Gets location of holding area.

        Return:
            location (Location): Location of holding area.
        """
        return copy(self._location)

    def set_position(self, position: Position) -> None:
        """
        Sets cartesian position of holding area instance.

        Args:
            position (Position):
                Position assigned to holding area instance.
        """
        self._position: Position = position

    def get_position(self) -> Position:
        """
        Gets position of holding area instance.

        Returns:
            Position: Position assigned to holding area instance.
        """
        return copy(self._position)

    def set_occupation_status(self, occupation_status: bool) -> None:
        """
        Sets occupation status to true or false.

        Args:
            occupation_status (bool): New occupation status.
        """
        self._occupation_status = occupation_status

    def get_occupation_status(self) -> bool:
        """
        Gets current occupation status.

        Returns:
            bool: Current occupation status.
        """
        return bool(self._occupation_status)

    def add_container(self, container: "Container") -> None:
        """
        Adds container to holding area.

        Args:
            container (Container): Container to be added to holding area.
        """
        if self.get_occupation_status() is True:
            if IDClass.get_verbosity() > 0:
                print("Holding Area is already occupied.")
        else:
            # Set new location to added container
            container_location = Location(
                self.get_location().get_facility(),
                self.get_location().get_room(),
                self,
            )
            container.set_location(container_location)

            # Add container to inventory
            self._container_inventory[container.get_id()] = container
            self.set_occupation_status(True)

    def remove_container(self) -> None:
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
        self.set_occupation_status(False)

    def get_container(self) -> "Container":
        """
        Gets the container contained in holding area.

        Returns:
            Container:
                Container that is contained in holding area.
        """
        if self._occupation_status is False:
            if IDClass.get_verbosity() > 0:
                print("No container in holding area.")
        else:
            for id, container in self._container_inventory.items():
                if IDClass.get_verbosity() > 0:
                    print(f"Container: {container.get_name()}, ID: {id}")
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
            if self is cmd.get_origin().get_holding_area():
                self.remove_container()
            # If holding area is at destination of transport
            if self is cmd.get_destination().get_holding_area():
                self.add_container(cmd.get_target())

        # Update own history
        super().update_history(cmd)


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
    _location: "Location" = None

    def __init__(self, type: str, name: str, dimensions: Dimensions):
        super().__init__()
        self.set_type(type)
        self.set_name(name)
        self.set_dimensions(dimensions)

    def set_type(self, type: str) -> None:
        """
        Sets container type.

        Args:
            type (str): Container type.
        """
        self._type: str = type

    def get_type(self) -> str:
        """
        Gets container type.

        Returns:
            str: Container type.
        """
        return str(self._type)

    def set_name(self, name: str) -> None:
        """
        Sets container name.

        Args:
            name (str): Container name.
        """
        self._name: str = name

    def get_name(self) -> str:
        """
        Gets container name.

        Returns:
            str: Container name.
        """
        return str(self._name)

    def set_dimensions(self, dimensions: Dimensions) -> None:
        """
        Sets dimensions of the container instance.

        Args:
            dimensions (Dimensions):
                Dimensions assigned to the container instance.
        """
        self._dimensions: Dimensions = dimensions

    def get_dimensions(self) -> Dimensions:
        """
        Gets dimensions of the container instance.

        Returns:
            Dimensions: Dimensions assigned to the container instance.
        """
        return copy(self._dimensions)

    def set_location(self, location: "Location") -> None:
        """
        Sets container location.

        Args:
            location (Location): New location of container.
        """
        if location.get_facility() is None:
            raise KeyError("Facility must not be NoneType.")
        elif location.get_room() is None:
            raise KeyError("Room must not be NoneType.")
        elif location.get_holding_area() is None:
            raise KeyError("Holding area must not be NoneType.")
        else:
            self._location: Location = location

    def get_location(self) -> "Location":
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
            self.set_location(cmd.get_destination())

        # Update own history
        super().update_history(cmd)


@dataclass
class Location:
    """
    A class that specifies the location of an instance
    based on facility, room and holding area.

    Attributes:
        _facility (Facility): Corresponding   facility instance.
        _room (Room): Corresponding room instance.
        _holding_area (HoldingArea): Corresponding holding area instance.
    """

    _facility: Facility
    _room: Room
    _holding_area: HoldingArea

    def __init__(self, *args):
        if len(args) > 0:
            self.set_facility(args[0])
        else:
            self.set_facility(None)
        if len(args) > 1:
            self.set_room(args[1])
        else:
            self.set_room(None)
        if len(args) > 2:
            self.set_holding_area(args[2])
        else:
            self.set_holding_area(None)

    def __repr__(self) -> str:
        """
        Provides a string representation of the Location instance.

        Returns:
            str: String representation of the Location instance.
        """
        return (
            f"({self.get_facility().get_name()}, "
            f"{self.get_room().get_name()}, "
            f"{self.get_holding_area().get_name()})"
        )

    def set_facility(self, facility: Facility) -> None:
        """
        Sets facility.

        Args:
                facility (Facility): Facility instance.
        """
        self._facility: Facility = facility

    def get_facility(self) -> Facility:
        """
        Gets facility.

        Returns:
                facility: Facility instance.
        """
        return self._facility

    def set_room(self, room: Room) -> None:
        """
        Sets room.

        Args:
                room (Room): Room instance.
        """
        self._room: Room = room

    def get_room(self) -> Room:
        """
        Gets room.

        Returns:
                Room: Room instance.
        """
        return self._room

    def set_holding_area(self, holding_area: HoldingArea) -> None:
        """
        Sets holding area.

        Args:
                holding_area (HoldingArea): Holding area instance.
        """
        self._holding_area: HoldingArea = holding_area

    def get_holding_area(self) -> HoldingArea:
        """
        Gets holding area.

        Returns:
                HodingArea: Holding area instance.
        """
        return self._holding_area

    def print_location(self) -> None:
        """
        Prints facility and room IDs of location.
        """
        if self.get_facility / () is not None:
            print(
                f"Facility: {self.get_facility().get_name()}, "
                f"ID: {self.get_facility().get_id()}"
            )
        if self.get_room() is not None:
            print(
                f"Room: {self.get_room().get_name()}, "
                f"ID: {self.get_room().get_id()}"
            )
        if self.get_holding_area() is not None:
            hAN = self.get_holding_area().get_name()
            hAID = self.get_holding_area().get_id()
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
        self.set_type(type)
        self.set_target(target)

    def set_type(self, type: str) -> None:
        """
        Sets command type.

        Args:
                type (str): Command type.
        """
        self._type: str = type

    def get_type(self) -> str:
        """
        Gets command type.

        Returns:
                str: Command type.
        """
        return str(self._type)

    def set_target(self, target: HistoryClass) -> None:
        """
        Set instance targeted with a command.

        Args:
                target (HistoryClass): Targeted instance.
        """
        self._target: HistoryClass = target

    def get_target(self) -> HistoryClass:
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
        self.set_origin(origin)
        self.set_destination(destination)

    def set_origin(self, origin: Location) -> None:
        """
        Sets origin of transport.

        Args:
                origin (Location): Origin of transport.
        """
        self._origin: Location = origin

    def get_origin(self) -> Location:
        """
        Gets origin of transport.

        Returns:
                Location: Origin of transport.
        """
        return copy(self._origin)

    def set_destination(self, destination: Location) -> None:
        """
        Sets destination of transport.

        Args:
                destination (Location): Destination of transport.
        """
        self._destination: Location = destination

    def get_destination(self) -> Location:
        """
        Gets destination of transport.

        Returns:
                Location: Destination of transport.
        """
        return copy(self._destination)

    def print_command(self) -> None:
        """
        Prints details of transport command.
        """
        print(f"Transport command with target: {self.get_target()}")
        print("Origin:")
        self.get_origin().print_location()
        print("Destination:")
        self.get_destination().print_location()


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

    def issue_transport_command(
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
        if origin.get_facility() is not target.get_location().get_facility():
            raise KeyError(
                "Origin Facility must be same as target's current Facility."
            )
        if origin.get_room() is not target.get_location().get_room():
            raise KeyError(
                "Origin Room must be same as target's current Room."
            )
        if (
            origin.get_holding_area()
            is not target.get_location().get_holding_area()
        ):
            raise KeyError(
                """Origin Holding area must be the same
                as target's current Holding area."""
            )
        # Check that destination Location does not contain NoneTypes
        elif not destination.get_facility():
            raise KeyError("Destination Facility must not be NoneType.")
        elif not destination.get_room():
            raise KeyError("Destination Room must not be NoneType.")
        elif not destination.get_holding_area():
            raise KeyError("Destination Holding area must not be NoneType.")
        else:
            # Create Command
            cmd = TransportCmd(target, origin, destination)

            with self._authorize():
                # Activate components at origin of transport
                current_holding_area = target.get_location().get_holding_area()
                current_holding_area.activation(cmd, self)
                current_room = target.get_location().get_room()
                current_room.activation(cmd, self)
                current_facility = target.get_location().get_facility()
                current_facility.activation(cmd, self)

                # Activate components at destination of transport
                destination_facility = destination.get_facility()
                destination_facility.activation(cmd, self)
                destination_room = destination.get_room()
                destination_room.activation(cmd, self)
                destination_holding_area = destination.get_holding_area()
                destination_holding_area.activation(cmd, self)

                # Activate target
                target.activation(cmd, self)


@dataclass
class Builder:
    """
    A class that creates instances of physical components and
    uses them to construct a model based on user input.
    """

    def build_model(self, model: Dict[str, Dict]) -> None:
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
                facilityInstance.add_room(roomInstance)

                if len(room_stats) > 4:
                    # Initialize holding area with data from dictionary
                    #       Room MAY contain holding areas.
                    model_3: Dict[str, Dict] = room_stats["holding_areas"]
                    for _holding_area, holding_area_stats in model_3.items():
                        holding_areaInstance = HoldingArea(
                            name=holding_area_stats["name"],
                            position=Position(
                                holding_area_stats["position"]["x"],
                                holding_area_stats["position"]["y"],
                                holding_area_stats["position"]["z"],
                            ),
                        )

                        # Add holding area to room
                        roomInstance.add_holding_area(holding_areaInstance)

                        # Initialize container with data from dictionary
                        #       Holding area MAY contain a container.
                        if len(holding_area_stats) > 2:
                            model_4: Dict = holding_area_stats["container"]
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
                            holding_areaInstance.add_container(
                                containerInstance
                            )

        if MonitoringSystem.get_verbosity() > 0:
            print("\nAll registered instances:")
            MonitoringSystem.display_registry()

    def get_model(self) -> Dict[str, Dict]:
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
                "type": facility.get_type(),
                "name": facility.get_name(),
                "dimensions": {
                    "dx": facility.get_dimensions().get_x(),
                    "dy": facility.get_dimensions().get_y(),
                    "dz": facility.get_dimensions().get_z(),
                },
                "position": {
                    "x": facility.get_position().get_x(),
                    "y": facility.get_position().get_y(),
                    "z": facility.get_position().get_z(),
                },
            }

            # Get Rooms
            room_inventory: Dict[int, Room] = facility.get_room_inventory()
            model["facility " + str(i)]["rooms"] = {}
            j: int = 1
            for _id, room in room_inventory.items():
                model["facility " + str(i)]["rooms"]["room " + str(j)] = {
                    "type": room.get_type(),
                    "name": room.get_name(),
                    "dimensions": {
                        "dx": room.get_dimensions().get_x(),
                        "dy": room.get_dimensions().get_y(),
                        "dz": room.get_dimensions().get_z(),
                    },
                    "position": {
                        "x": room.get_position().get_x(),
                        "y": room.get_position().get_y(),
                        "z": room.get_position().get_z(),
                    },
                }

                # Get Holding areas (if any)
                holding_area_inventory: Dict[int, HoldingArea] = (
                    room.get_holding_area_inventory()
                )
                if holding_area_inventory:
                    model["facility " + str(i)]["rooms"]["room " + str(j)][
                        "holding_areas"
                    ] = {}
                    k: int = 1
                    for _id, holding_area in holding_area_inventory.items():
                        model["facility " + str(i)]["rooms"]["room " + str(j)][
                            "holding_areas"
                        ]["holding_area " + str(k)] = {
                            "name": holding_area.get_name(),
                            "position": {
                                "x": holding_area.get_position().get_x(),
                                "y": holding_area.get_position().get_y(),
                                "z": holding_area.get_position().get_z(),
                            },
                        }

                        # Get Container (if any)
                        container: Container = holding_area.get_container()
                        if container:
                            model["facility " + str(i)]["rooms"][
                                "room " + str(j)
                            ]["holding_areas"]["holding_area " + str(k)][
                                "container"
                            ] = {
                                "type": container.get_type(),
                                "name": container.get_name(),
                                "dimensions": {
                                    "dx": container.get_dimensions().get_x(),
                                    "dy": container.get_dimensions().get_y(),
                                    "dz": container.get_dimensions().get_z(),
                                },
                            }
                        k += 1
                    k = 1
                j += 1
            j = 1
            i += 1
        return model

    def load_dummy_model(self) -> Dict[str, Dict]:
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
                        "holding_areas": {
                            "holding_area 1": {
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
                            "holding_area 2": {
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
                        "holding_areas": {
                            "holding_area 1": {
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
                        "holding_areas": {
                            "holding_area 1": {
                                "name": "HoldingArea 1",
                                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                            }
                        },
                    },
                },
            },
        }

        return dummy_model

    def load_model_from_file(self, file_path: str) -> Dict[str, Dict]:
        """
        Creates a model based on a file in JSON format.
        See data/dummy_model.json for syntax.

        Args:
            file_path (str):
                Relative or absolute path to json file with model data.

        Returns:
            Dict[str, Dict]: Dictionary with model data.
        """
        try:
            with open(file_path) as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            if MonitoringSystem.get_verbosity() > 0:
                print(f"Error: The file '{file_path}' was not found.")
            return None
        except json.JSONDecodeError:
            if MonitoringSystem.get_verbosity() > 0:
                print(f"Error: The file '{file_path}' is not a valid JSON.")
            return None

    def export_model_to_file(
        self, model: Dict[str, Dict], file_path: str
    ) -> None:
        """
        Creates a JSON file with model information.

        Args:
            model (Dict[str, Dict]):
                Dictionary that is to be exported to JSON file.
            file_path (str):
                Relative or absolute path to json file with model data.
        """
        try:
            with open(file_path, "w") as file:
                json.dump(model, file, indent=4)
            if MonitoringSystem.get_verbosity() > 0:
                print(f"Model successfully saved to {file_path}.")
        except OSError as e:
            if MonitoringSystem.get_verbosity() > 0:
                print(
                    f"""An error occurred while
                    saving the model to {file_path}: {e}"""
                )

    def create_model_manually(self) -> Dict[str, Dict]:
        """
        Creates a model manually based on user prompts.

        Returns:
            Dict[str, Dict]: Dictionary with model data.
        """
        pass

    def load_dummy_adjacency_matrix(self):
        """
        Creates dummy adjaceny matrix for dummy model data.
        """
        pass
