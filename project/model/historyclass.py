from dataclasses import dataclass, field
from typing import Dict

from model.monitoringsystem import IDClass
from projecttypes.command import Command


@dataclass
class HistoryClass(IDClass):
    """
    The base class for all instances that come with a history that
    tracks all changes made to the instance.

    Attributes:
        registry (Dict[int, dict]): Dictionary to store command
        specifications.
    """

    registry: Dict[int, dict] = field(default_factory=dict)

    def Activation(self, cmd: Command):
        """
        Registers a command and activates certain functions based on
        the command type.

        Args:
            cmd (Command): Instance of command to be processed.
        """
        self.UpdateHistory(cmd.type, cmd.id, cmd.target_id)

    def UpdateHistory(self, cmd_id: int, cmd_type: str, target_id: int):
        """
        Stores command specifications in a dictionary.

        Args:
            cmd_id (int): Unique ID of processed command.
            cmd_type (str): Type of processed command.
            target_id (int): Unique ID of instance targeted by
            processed command.
        """
        self.registry[cmd_id] = {"cmd_type": cmd_type, "target_id": target_id}
