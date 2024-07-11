from dataclasses import dataclass

from model.monitoringsystem import IDClass


@dataclass
class HistoryClass(IDClass):
    """
    The base class for all instances that come with a history that
        tracks all changes made to the instance,

    Attributes:
    param (str): An additional parameter specific to HistoryClass.
    """

    # param: str
