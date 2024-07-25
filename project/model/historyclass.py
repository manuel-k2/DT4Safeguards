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
            _registry (Dict[int, {str, int}]):
    """

    registry: Dict[int, {str, int}] = field(default_factory=dict)

    def Activation(self, cmd: Command):
        """
        Registers a command and activates certain
                functions based on the command type.

        Args:
                cmd (Command): Instance of command to be processed.
        """
        self.UpdateHistory(cmd.type, cmd.id, cmd.targetID)

    def UpdateHistory(self, cmdID: int, cmdType: str, targetID: int):
        """
        Stores command specifications in a dictionary.

        Args:
                cmdID (int): Unique ID of processed command.
                cmdType (str): Type of processed command.
                targetID (int):
                        Unique ID of instance targeted by processed command.
        """
        self.registry[cmdID] = {cmdType, targetID}
