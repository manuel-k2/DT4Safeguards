from dataclasses import dataclass, field
from typing import ClassVar, Dict


class InstanceNotFoundError(Exception):
    """Exception raised when an instance with a given ID is not found."""

    pass


class MonitoringSystem:
    """
    A class to monitor all instances listed in a registry indexed by their IDs.

    Attributes:
        _registry (Dict[int, IDClass]): Class-level dictionary to store
        instances of IDClass, indexed by integer IDs.
        _id_counter (int): Class-level counter to generate unique IDs.
    """

    _registry: ClassVar[Dict[int, "IDClass"]] = {}
    _id_counter: ClassVar[int] = 0

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
            print(f"Instance with ID '{id}' not found.")
            raise InstanceNotFoundError()
        return cls._registry[id]

    @classmethod
    def display_registry(cls):
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
        id (int): The unique identifier for the instance.
    """

    id: int = field(init=False)

    def __post_init__(self):
        """
        Registers the instance in the registry after initialization
        and assigns a unique ID.
        """
        self.id = MonitoringSystem.register(self)
