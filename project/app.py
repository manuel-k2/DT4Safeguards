from model.monitoringsystem import MonitoringSystem
from model.facility import Facility
from model.room import Room

from projecttypes.dimensions import Dimensions

first_facility = Facility(
    type="Interim storage", name="Jülich", dimensions=Dimensions(1, 1, 1)
)

first_room = Room(
    type="Storage", name="Room 1", dimensions=Dimensions(1, 1, 1)
)

first_facility.AddRoom(first_room)
first_facility.GetRoomInventory()

MonitoringSystem.display_registry()
