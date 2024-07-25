from model.facility import Facility
from model.room import Room


class Location:
    """
    A class that specifies the location of an instance.

    Attirbutes:
            facility (Facility): Corresponding facility instance.
            room (Room): Corresponding room instance.
    """

    facility: Facility
    room: Room

    def __init__(self, facility: Facility, room: Room):
        self.facility = facility
        self.room = room

    def PrintLocation(self):
        """
        Print facility and room IDs of location.
        """
        print(self.facility.id, self.room.id)

    def GetFacility(self):
        """
        Get facility.

        Returns:
                facility (Facility): Facility instance.
        """
        return self.facility

    def GetRoom(self):
        """
        Get room.

        Returns:
                room (Room): Room instance.
        """
        return self.room
