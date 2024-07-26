from model.monitoringsystem import IDClass

from project.projecttypes.location import Location


class Command(IDClass):
    """
    The base class for all instances that specify commands.

    Attributes:
        type (str): Type of command.
        targetID (int): ID of instance that is targeted by command.
    """

    type: str
    targetID: int

    def __init__(self, cmdType: str, targetID: int):
        super().__init__()
        self.type = cmdType
        self.targetID = targetID


class TransportCmd(Command):
    """
    A class that specifies a transport command from an origin to a destination.

    Attributes:
        origin (Location): Origin of transport.
        destination (Location): Destination of transport.
    """

    origin: Location
    destination: Location

    def __init__(self, origin: Location, destination: Location):
        super().__init__()
        self.type = "transport"
        self.origin = origin
        self.destination = destination

    def GetOrigin(self):
        """
        Get origin of transport.

        Returns:
                origin (Location): Origin of transport.
        """
        return self.origin

    def GetDestintaion(self):
        """
        Get destination of transport.

        Returns:
                destination (Location): Destination of transport.
        """
        return self.destination
