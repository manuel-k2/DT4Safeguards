from model.monitoringsystem import MonitoringSystem
from model.components import Facility
from model.components import Room
from model.components import HoldingArea
from model.components import Container

from projecttypes.dimensions import Dimensions


# Create instances
first_facility = Facility(
    type="Interim storage", name="Jülich", dimensions=Dimensions(1, 1, 1)
)

first_room = Room(
    type="Storage", name="Room 1", dimensions=Dimensions(1, 1, 1)
)

first_holdingArea = HoldingArea(name="Bay 1")

second_room = Room(
    type="Storage", name="Room 2", dimensions=Dimensions(1, 1, 1)
)

second_holdingArea = HoldingArea(name="Bay 1")

first_container = Container(
    type="Castor", name="Container 1", dimensions=Dimensions(1, 1, 1)
)

# Construct model
first_facility.AddRoom(first_room)
first_facility.AddRoom(second_room)
print("Room inventory: ")
first_facility.GetRoomInventory()

print("Room locations: ")
first_room.GetLocation().PrintLocation()
second_room.GetLocation().PrintLocation()

print("\n")

first_room.AddHoldingArea(first_holdingArea)
print("Holding area inventory - Room 1: ")
first_room.GetHoldingAreaInventory()

second_room.AddHoldingArea(second_holdingArea)
print("Holding area inventory - Room 2: ")
second_room.GetHoldingAreaInventory()

print("Holding area locations: ")
first_holdingArea.GetLocation().PrintLocation()
second_holdingArea.GetLocation().PrintLocation()

print("\n")

first_holdingArea.AddContainer(first_container)
print("Container inventory: ")
first_holdingArea.GetContainer()

print("Container location: ")
first_container.GetLocation().PrintLocation()

# Print complete registry
print("\nComplete registry:")
MonitoringSystem.display_registry()

# Move container