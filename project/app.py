# from model.monitoringsystem import MonitoringSystem
from model.components import Facility, Room, HoldingArea, Container
from model.components import Commander

from projecttypes.units import Dimensions, Position

# Create instances
facility_1 = Facility(
    type="Interim storage",
    name="Facility 1",
    dimensions=Dimensions(1, 1, 1),
    position=Position(0, 0, 0),
)

room_1 = Room(
    type="Storage",
    name="Room 1",
    dimensions=Dimensions(1, 1, 1),
    position=Position(0, 0, 0),
)

holdingArea_1 = HoldingArea(name="HoldingArea 1", position=Position(0, 0, 0))
holdingArea_2 = HoldingArea(name="HoldingArea 2", position=Position(0, 0, 0))

room_2 = Room(
    type="Storage",
    name="Room 2",
    dimensions=Dimensions(1, 1, 1),
    position=Position(0, 0, 0),
)
holdingArea_3 = HoldingArea(name="Bay 1", position=Position(0, 0, 0))

facility_2 = Facility(
    type="Geological repository",
    name="Facility 2",
    dimensions=Dimensions(1, 1, 1),
    position=Position(0, 0, 0),
)

room_3 = Room(
    type="Storage",
    name="Room 1",
    dimensions=Dimensions(1, 1, 1),
    position=Position(0, 0, 0),
)

holdingArea_4 = HoldingArea(name="HoldingArea 1", position=Position(0, 0, 0))

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

# # Print inventories and locations
# print("Room inventory - Facility 1: ")
# facility_1.GetRoomInventory()
# print("Room inventory - Facility 2: ")
# facility_2.GetRoomInventory()

# print("\nLocation - Room 1: ")
# room_1.GetLocation().PrintLocation()
# print("Location - Room 2: ")
# room_2.GetLocation().PrintLocation()
# print("Location - Room 3: ")
# room_3.GetLocation().PrintLocation()

# print("\nHolding area inventory - Room 1: ")
# room_1.GetHoldingAreaInventory()
# print("Holding area inventory - Room 2: ")
# room_2.GetHoldingAreaInventory()
# print("Holding area inventory - Room 3: ")
# room_3.GetHoldingAreaInventory()

# print("\nLocation - Holding Area 1: ")
# holdingArea_1.GetLocation().PrintLocation()
# print("Location - Holding Area 2: ")
# holdingArea_2.GetLocation().PrintLocation()
# print("Location - Holding Area 3: ")
# holdingArea_3.GetLocation().PrintLocation()
# print("Location - Holding Area 4: ")
# holdingArea_4.GetLocation().PrintLocation()

# print("\nContainer inventory - Holding area 1: ")
# holdingArea_1.GetContainer()
print("Location - Container 1: ")
container_1.GetLocation().PrintLocation()

# # Print complete registry
# print("\nComplete registry:")
# MonitoringSystem.display_registry()

# Move container by sending Transport sepecifications to Commander
target = container_1
origin = container_1.GetLocation()
destination = holdingArea_4.GetLocation()
destination.SetHoldingArea(holdingArea_4)

commander = Commander()
commander.IssueTransportCommand(target, origin, destination)

# Print new container location and histories
print("\nLocation - Container 1")
container_1.GetLocation().PrintLocation()

print("\nHistory - Container 1")
container_1.ShowHistory()
print("History - Facility 1")
facility_1.ShowHistory()
print("History - Facility 2")
facility_2.ShowHistory()
