from dataclasses import dataclass, field
from typing import ClassVar, Dict
from datetime import datetime, timedelta
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


class InvalidStartTimeError(Exception):
    """
    Exception raised when the start time
    is before the current global time.
    """

    pass


class MonitoringSystem:
    """
    A class to monitor all instances listed in a registry indexed by their IDs.

    Attributes:
        _registry (Dict[int, IDObject]):
            Class-level dictionary to store instances
            of IDObject, indexed by integer IDs.
        _id_counter (int): Class-level counter to generate unique IDs.
        _verbosity (int): Class-level verbosity setting.
    """

    _registry: ClassVar[Dict[int, "IDObject"]] = (
        {}
    )  # Class-level dictionary to store indexed instances of IDObject.
    _id_counter: ClassVar[int] = (
        0  # Class-level counter to generate unique IDs.
    )
    _global_time: ClassVar[datetime] = datetime(
        2024, 1, 1, 0, 0
    )  # Initialize global time to a specific start date and time.
    _verbosity: ClassVar[int] = 1  # 0: Silent, 1: Verbose

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
    def register(cls, instance: "IDObject") -> int:
        """
        Registers an instance in the registry and assigns a unique ID.

        Args:
            instance (IDObject): The instance to be registered.

        Returns:
            int: The unique ID assigned to the instance.
        """
        instance_id = cls._id_counter
        cls._registry[instance_id] = instance
        cls._id_counter += 1
        return instance_id

    @classmethod
    def get_instance(cls, id: int) -> "IDObject":
        """
        Retrieves an instance from the registry by its ID.

        Args:
            id (int): The ID of the instance to retrieve.

        Returns:
            Instance of IDObject if found.

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
            print(f"Retrieved instance with ID: {id}, Type: {type(instance).__name__}")
        return instance

    @classmethod
    def get_instance_by_type(cls, class_type: type) -> Dict[int, "IDObject"]:
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
            print(f"Retrieved instances of type {class_type.__name__}: ")
            for id, instance in instance_inventory.items():
                print(f"ID: {id}, Type: {type(instance).__name__}")

        return instance_inventory

    @classmethod
    def display_registry(cls) -> None:
        """
        Displays all instances in the registry.
        """
        if not cls._registry:
            print("None.")
        else:
            for id, instance in cls._registry.items():
                print(f"ID: {id}, Type: {type(instance).__name__}")

    @classmethod
    def get_time(cls) -> str:
        """
        Gets current global time in the format YYYY:MM:DD.hh:mm.

        Returns:
            str: Current global time.
        """
        if cls.get_verbosity() > 0:
            print("Global time: ", cls._global_time.strftime("%Y:%m:%d.%H:%M"))

        return cls._global_time.strftime("%Y:%m:%d.%H:%M")

    @classmethod
    def set_time(cls, new_time: datetime) -> None:
        """
        Sets global time to a new value.

        Args:
            new_time (datetime): New global time.
        """
        cls._global_time = new_time

    @classmethod
    def process_time(cls, start_time: str, end_time: str) -> None:
        """
        Processes start and end times, updates global time if necessary,
        calculates the duration.

        Args:
            start_time (str): Start time in the format YYYY:MM:DD.hh:mm.
            end_time (str): End time in the format YYYY:MM:DD.hh:mm.

        Returns:
            int: Duration between the start and end times in minutes.
        """
        # Parse start and end times
        start_dt = datetime.strptime(start_time, "%Y:%m:%d.%H:%M")
        end_dt = datetime.strptime(end_time, "%Y:%m:%d.%H:%M")

        current_dt = cls._global_time

        # Update global time if start time is later than current global time
        if start_dt > current_dt:
            cls.set_time(end_dt)

            if cls.get_verbosity() > 0:
                print(f"New global time is: {end_time}")

            return

        # Check if start time is before current global time
        if start_dt < current_dt:
            duration_before_current_time = int(
                (current_dt - start_dt).total_seconds() / 60
            )  # Duration in minutes

            if cls.get_verbosity() > 0:
                print(
                    f"""Warning: Start time is {duration_before_current_time}
                    min before current global time."""
                )

        # Calculate duration
        duration_total = int(
            (end_dt - start_dt).total_seconds() / 60
        )  # Duration in minutes

        if start_dt < current_dt:
            duration = duration_total - duration_before_current_time
        else:
            duration = duration_total

        # Increment global time by duration
        cls.increment_time(duration)

        if cls.get_verbosity() > 0:
            print(
                f"Process duration: {duration} minutes."
                f"\nNew global time is: {cls.get_time()}"
            )

    @classmethod
    def increment_time(cls, amount: int = 1) -> None:
        """
        Increments the global time by a specified amount.

        Args:
            amount (int):
                Amount of time to increment by in minutes.
                Default is 1 minute.
        """
        cls._global_time += timedelta(minutes=amount)


@dataclass
class IDObject:
    """
    The base class for all registrable instances
    that get assigned a unique identifier.

    Attributes:
        _id (int): The unique identifier for the instance.
        _init_time (str):
            Global time at the moment of instance initialization.
        _verbosity (int): Class-level verbosity setting.
    """

    _id: int = field(init=False)  # ID of IDObject instance
    _init_time: str = field(
        init=False
    )  # Initialization time of IDObject instance
    _verbosity: ClassVar[int] = 1  # 0: Silent, 1: Verbose

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
        self._init_time = MonitoringSystem.get_time()

    def get_id(self) -> int:
        """
        Gets unique ID of instance.

        Returns:
            id (int): Unique ID of instance.
        """
        return int(self._id)


@dataclass
class HistoryObject(IDObject):
    """
    The base class for all instances that come with a history that
    tracks all changes made to the instance.

    Attributes:
        _history (History): History instance.
    """

    _history: "History"

    def __init__(self) -> None:
        super().__init__()

    def __post_init__(self) -> None:
        super().__post_init__()
        self._history = History()

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
        self._history.update_history(cmd)

    def get_history(self) -> "History":
        """
        Gets history instance of HistoryObject instance.

        Returns:
            History: History instance of HistoryObject instance.
        """
        return self._history
    
    def get_history_at_time(self, time: str) -> "History":
        """
        Gets history instance of HistoryObject instance
        at a specific time.

        Args:
            time (str): Time in the format YYYY:MM:DD.hh:mm.

        Returns:
            History:
                History instance of HistoryObject instance
                at a specific time.
        """
        _history_at_time = History()
        _history_at_time._entries = {
            id: value
            for id, value in self.get_history().get_entries().items()
            if datetime.strptime(value["end_time"], "%Y:%m:%d.%H:%M")
            < datetime.strptime(time, "%Y:%m:%d.%H:%M")
        }

        return _history_at_time


@dataclass
class History:
    """
    History class that tracks all changes made to
    an associated instance.

    Attributes:
        _entries (Dict[int, dict]): Dictionary to store
            command specifications.
    """

    _entries: Dict[int, dict] = field(default_factory=dict)

    def __repr__(self) -> str:
        """
        Provides a string representation of the History instance.

        Returns:
            str: String representation of the History instance.
        """
        if not self._entries:
            return "History is empty."
        else:
            return_str = ""
            for id, command in self._entries.items():
                return_str += (
                    f"""Command ID: {id}, """
                    f"""Type: {command["cmd_type"]}, """
                    f"""Target: {command["target"].get_name()}, """
                    f"""Start: {command["start_time"]}, """
                    f"""End: {command["end_time"]}.\n"""
                )
            return return_str
    
    def get_entries(self) -> Dict[int, dict]:
        """
        Get entries of History instance's dictionary.

        Returns:
            Dict[int, dict]: Dictionary with command specifications.
        
        """
        return copy(self._entries)


    def update_history(self, cmd: "Command") -> None:
        """
        Stores command specifications in a dictionary.

        Args:
            cmd (Command): Instance of command to be processed.
        """
        self._entries[cmd.get_id()] = {
            "cmd_type": cmd.get_type(),
            "target": cmd.get_target(),
            "start_time": cmd.get_start_time(),
            "end_time": cmd.get_end_time(),
        }


@dataclass
class Facility(HistoryObject):
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
        """
        Initializes Facility instance.

        Args:
            type (str): Type of facility.
            name (str): Name of facility.
            dimensions (Dimensions): Dimensions of facility.
            position (Position): Position of faility.
        """
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

    def remove_room(self, room_id: int) -> None:
        """
        Removes a room from the facility's room inventory.

        Args:
            room_id (int): ID of room to be removed from inventory.
        """
        if room_id not in self._room_inventory:
            raise KeyError(f"Room with ID {room_id} not found.")
        if len(self._room_inventory) == 1 and room_id in self._room_inventory:
            self._room_inventory.clear()
        else:
            del self._room_inventory[room_id]

    def get_room_inventory(self) -> Dict[int, "Room"]:
        """
        Gets the facility's room inventory.

        Returns:
            Dict[int, Room]: Dictionary of rooms that are contained
                in facility.
        """
        if IDObject.get_verbosity() > 0:
            if not self._room_inventory:
                print("Room inventory is empty.")
            else:
                for id, room in self._room_inventory.items():
                    print(f"ID: {id}, Type: Room, Name: {room.get_name()}")
        return copy(self._room_inventory)


@dataclass
class Room(HistoryObject):
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
        """ "
        Initializes Room instance.

        Args:
            type (str): Type of room.
            name (str): Name of room.
            dimensions (Dimensions): Dimensions of room.
            position (Position): Position of room.
        """
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

    def remove_holding_area(self, holding_area_id: int) -> None:
        """
        Removes a holding area from the rooms's holding area inventory.

        Args:
            holding_area_id (int):
                ID of holding area to be removed from inventory.
        """
        if holding_area_id not in self._holding_area_inventory:
            raise KeyError(
                f"Holding area with ID {holding_area_id} not found."
            )
        if (
            len(self._holding_area_inventory) == 1
            and holding_area_id in self._holding_area_inventory
        ):
            self._holding_area_inventory.clear()
        else:
            del self._holding_area_inventory[holding_area_id]

    def get_holding_area_inventory(self) -> Dict[int, "HoldingArea"]:
        """
        Gets the room's holding area inventory.

        Returns:
            Dict[int, HoldingArea]:
                Dictionary of holding areas that are contained in room.
        """
        if IDObject.get_verbosity() > 0:
            if not self._holding_area_inventory:
                print("Holdingg area inventory is empty.")
            else:
                for id, holding_area in self._holding_area_inventory.items():
                    print(f"ID: {id}, Type: Holding area, Name: {holding_area.get_name()}")
        return copy(self._holding_area_inventory)


@dataclass
class HoldingArea(HistoryObject):
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
        """ "
        Initializes HoldingArea instance.

        Args:
            name (str): Name of holding area.
            position (Position): Position of holding area.
        """
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
            if IDObject.get_verbosity() > 0:
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
        if IDObject.get_verbosity() > 0:
            for id, container in self._container_inventory.items():
                print(
                    f"ID: {id}, Container: {container} "
                    "removed from holding area."
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
            if IDObject.get_verbosity() > 0:
                print("No container in holding area.")
        else:
            for id, container in self._container_inventory.items():
                if IDObject.get_verbosity() > 0:
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
        super()._activation(cmd)


@dataclass
class Container(HistoryObject):
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
        """ "
        Initializes Container instance.

        Args:
            type (str): Type of container.
            name (str): Name of container.
            dimensions (Dimensions): Dimensions of container.
        """
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
        super()._activation(cmd)


@dataclass
class Location:
    """
    A class that specifies the location of an instance
    based on facility, room and holding area.

    Attributes:
        _facility (Facility): Corresponding facility instance.
        _room (Room): Corresponding room instance.
        _holding_area (HoldingArea): Corresponding holding area instance.
    """

    _facility: Facility
    _room: Room
    _holding_area: HoldingArea

    def __init__(self, *args):
        """ "
        Initializes Location instance.

        Args:
            facility (Facility): Corresponding facility instance.
            room (Room): Corresponding room instance (optional).
            holding_area (HoldingArea):
                Corresponding holding area instance (optional).
        """
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
        return_str = f"({self.get_facility().get_name()}, "
        if self._room is not None:
            return_str += f"{self.get_room().get_name()}, "
        else:
            return_str += "None, "
        if self._holding_area is not None:
            return_str += f"{self.get_holding_area().get_name()})"
        else:
            return_str += "None, "

        return return_str

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
            h_a_n = self.get_holding_area().get_name()
            h_a_id = self.get_holding_area().get_id()
            print(f"Holding Area: {h_a_n}, ID: {h_a_id}")


@dataclass
class Command(IDObject):
    """
    The base class for all instances that specify commands.
    All commands are to be directed to the Commander.

    Attributes:
        _type (str): Type of command.
        _target (HistoryObject): Instance that is targeted by command.
        _start_time (str): Start time in the format YYYY:MM:DD.hh:mm.
        _end_time (str): End time in the format YYYY:MM:DD.hh:mm.
    """

    _type: str
    _target: HistoryObject
    _start_time: str
    _end_time: str

    def __init__(
        self, type: str, target: HistoryObject, start_time: str, end_time: str
    ):
        """ "
        Initializes Command instance.

        Args:
            type (str): Type of command.
            target (HistoryObject): Instance that is targeted by command.
            start_time (str): Start time in the format YYYY:MM:DD.hh:mm.
            end_time (str): End time in the format YYYY:MM:DD.hh:mm.
        """
        super().__init__()
        self.set_type(type)
        self.set_target(target)
        self.set_start_time(start_time)
        self.set_end_time(end_time)
        MonitoringSystem.process_time(start_time, end_time)

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

    def set_target(self, target: HistoryObject) -> None:
        """
        Set instance targeted with a command.

        Args:
                target (HistoryObject): Targeted instance.
        """
        self._target: HistoryObject = target

    def get_target(self) -> HistoryObject:
        """
        Gets instance targeted with a command.

        Returns:
                HistoryObject: Targeted instance.
        """
        return self._target

    def set_start_time(self, start_time: str) -> None:
        """
        Sets the start time.

        Args:
            _start_time (str):
                Start time in the format YYYY:MM:DD.hh:mm.
        """
        self._start_time = start_time

    def get_start_time(self) -> str:
        """
        Gets the start time.

        Returns:
            str: Start time in the format YYYY:MM:DD.hh:mm.
        """
        return str(self._start_time)

    def set_end_time(self, end_time: str) -> None:
        """
        Sets the end time.

        Args:
            _end_time (str):
                End time in the format YYYY:MM:DD.hh:mm.
        """
        self._end_time = end_time

    def get_end_time(self) -> str:
        """
        Gets the end time.

        Returns:
            str: End time in the format YYYY:MM:DD.hh:mm.
        """
        return str(self._end_time)


@dataclass
class TransportCmd(Command):
    """
    A class that specifies a transport command from an origin to a destination.

    Attributes:
        _origin (Location): Origin of transport.
        _destination (Location): Destination of transport.
    """

    _origin: Location
    _destination: Location

    def __init__(
        self,
        target: HistoryObject,
        origin: Location,
        destination: Location,
        start_time: str,
        end_time: str,
    ):
        """ "
        Initializes TransportCmd instance.

        Args:
            type (str): Type of command.
            target (HistoryObject): Instance that is targeted by command.
            origin (Location): Origin of transport.
            destination (Location): Destination of transport.
            start_time (str): Start time in the format YYYY:MM:DD.hh:mm.
            end_time (str): End time in the format YYYY:MM:DD.hh:mm.
        """
        super().__init__("transport", target, start_time, end_time)
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
        return self._origin

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
        return self._destination

    def print_command(self) -> None:
        """
        Prints details of transport command.
        """
        print(f"Transport command with target: {self.get_target()}")
        print("Origin:")
        self.get_origin().print_location()
        print("Destination:")
        self.get_destination().print_location()
        print("Start time:", self.get_start_time())
        print("End time:", self.get_end_time())


class Commander:
    """
    A class that creates commands based on user input.
    """

    _authorized_commander = None

    @contextmanager
    def _authorize(self):
        """
        Authorizes Commander instance ro activate other instances.
        """
        old_commander = Commander._authorized_commander
        Commander._authorized_commander = self
        try:
            yield
        finally:
            Commander._authorized_commander = old_commander

    def issue_transport_command(
        self,
        target: Container,
        origin: Location,
        destination: Location,
        start_time: str,
        end_time: str,
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
            cmd = TransportCmd(
                target, origin, destination, start_time, end_time
            )

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
            MonitoringSystem.get_instance_by_type(Facility)
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
