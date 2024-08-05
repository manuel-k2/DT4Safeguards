from model.components import MonitoringSystem, Facility, HoldingArea, Container
from model.components import Builder, Commander


# Create model with Builder by loading data from a JSON file
builder = Builder()
# model = builder.LoadDummyModel()
model = builder.LoadModelFromFile("../data/dummy_model.json")
builder.BuildModel(model)

# Get container and holding area from registry
container_1: Container = MonitoringSystem.get_instance(id=3)
holdingArea_destination: HoldingArea = MonitoringSystem.get_instance(id=10)

# print("\nLocation - Container 1 (PreTransport): ")
# container_1.GetLocation().PrintLocation()

# Move container by sending Transport sepecifications to Commander
target = container_1
origin = container_1.GetLocation()
destination = holdingArea_destination.GetLocation()
destination.SetHoldingArea(holdingArea_destination)

commander = Commander()
commander.IssueTransportCommand(target, origin, destination)

# Print new container location and history
# print("\nLocation - Container 1 (PostTransport)")
# container_1.GetLocation().PrintLocation()
# print("\nHistory - Container 1")
# container_1.ShowHistory()

# Print facility histories
facility_1: Facility = MonitoringSystem.get_instance(id=0)
print("History - Facility 1")
facility_1.ShowHistory()

# facility_2: Facility = MonitoringSystem.get_instance(id=7)
# print("History - Facility 2")
# facility_2.ShowHistory()

# Display current state of model and export it to JSON file
model_update = builder.GetModel()
builder.ExportModelToFile(model_update, "../data/dummy_model_export.json")
