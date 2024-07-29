from model.monitoringsystem import MonitoringSystem
from model.components import Facility
from model.components import Room
from model.components import HoldingArea
from model.components import Container

from projecttypes.dimensions import Dimensions


# Create instances
facility_1 = Facility(
    type="Interim storage", name="Jülich", dimensions=Dimensions(1, 1, 1)
)

room_1 = Room(
    type="Storage", name="Room 1", dimensions=Dimensions(1, 1, 1)
)

holdingArea_1 = HoldingArea(name="Bay 1")
holdingArea_2 = HoldingArea(name="Bay 2")

room_2 = Room(
    type="Storage", name="Room 2", dimensions=Dimensions(1, 1, 1)
)
holdingArea_3 = HoldingArea(name="Bay 1")

facility_2 = Facility(
    type="Geological repository", name="Onkalo", dimensions=Dimensions(1, 1, 1)
)

room_3 = Room(
    type="Storage", name="Room 1", dimensions=Dimensions(1, 1, 1)
)

holdingArea_4 = HoldingArea(name="Bay 1")

container_1 = Container(
    type="Castor", name="Container 1", dimensions=Dimensions(1, 1, 1)
)

# Construct model
facility_1.AddRoom(room_1)
room_1.AddHoldingArea(holdingArea_1)
room_1.AddHoldingArea(holdingArea_2)

facility_1.AddRoom(room_2)
room_2.AddHoldingArea(holdingArea_3)

facility_2.AddRoom(room_3)
room_3.AddHoldingArea(holdingArea_4)

holdingArea_1.AddContainer(container_1)

# Print inventories and locations
print("Room inventory - Facility 1: ")
facility_1.GetRoomInventory()
print("Room inventory - Facility 2: ")
facility_2.GetRoomInventory()

print("\nLocation - Room 1: ")
room_1.GetLocation().PrintLocation()
print("Location - Room 2: ")
room_2.GetLocation().PrintLocation()
print("Location - Room 3: ")
room_3.GetLocation().PrintLocation()

print("\nHolding area inventory - Room 1: ")
room_1.GetHoldingAreaInventory()
print("Holding area inventory - Room 2: ")
room_2.GetHoldingAreaInventory()
print("Holding area inventory - Room 3: ")
room_3.GetHoldingAreaInventory()

print("\nLocation - Holding Area 1: ")
holdingArea_1.GetLocation().PrintLocation()
print("Location - Holding Area 2: ")
holdingArea_2.GetLocation().PrintLocation()
print("Location - Holding Area 3: ")
holdingArea_3.GetLocation().PrintLocation()
print("Location - Holding Area 4: ")
holdingArea_4.GetLocation().PrintLocation()

print("\nContainer inventory - Holding area 1: ")
holdingArea_1.GetContainer()
print("Location - Container 1: ")
container_1.GetLocation().PrintLocation()

# Print complete registry
print("\nComplete registry:")
MonitoringSystem.display_registry()

# Move container
