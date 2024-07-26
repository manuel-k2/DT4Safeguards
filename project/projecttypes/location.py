from model.facility import Facility
from model.room import Room
from model.holdingarea import HoldingArea


class Location:
    """
    A class that specifies the location of an instance.

    Attributes:
        facility (Facility): Corresponding facility instance.
        room (Room): Corresponding room instance.
        holdingArea(HoldingArea): Corresponding holding area instance.
    """

    facility: Facility
    room: Room
    holdingArea: HoldingArea

    def SetFacility(self, facility: Facility):
        """
        Set facility.

        Args:
                facility (Facility): Facility instance.
        """
        self.facility = facility

    def GetFacility(self) -> Facility:
        """
        Get facility.

        Returns:
                facility: Facility instance.
        """
        return self.facility

    def SetRoom(self, room: Room):
        """
        Set room.

        Args:
                room (Room): Room instance.
        """
        self.room = room
    
    def GetRoom(self) -> Room:
        """
        Get room.

        Returns:
                Room: Room instance.
        """
        return self.room
     
    def SetHoldingArea(self, holdingArea: HoldingArea):
        """
        Set holding area.

        Args:
                holdingArea (HoldingArea): Holding area instance.
        """
        self.holdingArea = holdingArea
    
    def GetRoom(self) -> HoldingArea:
        """
        Get holding area.

        Returns:
                HodingArea: Holding area instance.
        """
        return self.holdingArea
    
    def PrintLocation(self):
        """
        Print facility and room IDs of location.
        """
        print(self.facility.id, self.room.id)
