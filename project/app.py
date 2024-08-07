from model.components import MonitoringSystem, Facility, HoldingArea, Container
from model.components import Builder, Commander


# Create model with Builder by loading data from a JSON file
builder = Builder()
# model = builder.load_dummy_model()
model = builder.load_model_from_file("../data/dummy_model.json")
builder.build_model(model)

# Get container and holding area from registry
container_1: Container = MonitoringSystem.get_instance(id=3)
holding_area_origin: HoldingArea = (
    container_1.get_location().get_holding_area()
)
holding_area_destination: HoldingArea = MonitoringSystem.get_instance(id=10)

# Move container by sending Transport sepecifications to Commander
target = container_1
origin = container_1.get_location()
destination = holding_area_destination.get_location()
destination.set_holding_area(holding_area_destination)
start_time = "2024:08:06.13:12"
end_time = "2024:08:06.14:19"

commander = Commander()
commander.issue_transport_command(
    target, origin, destination, start_time, end_time
)

# Print Holding area instance histories
print("Current Instance History - Holding area origin")
print(holding_area_origin.get_instance_history())

print("Initial Instance History - Holding area origin")
print(holding_area_origin.get_instance_history().at_time("2024:01:01.00:00"))

print("Current Instance History - Holding area destination")
print(holding_area_destination.get_instance_history())

print("Initial Instance History - Holding area destination")
print(
    holding_area_destination.get_instance_history().at_time("2024:01:01.00:00")
)

# Print facility complete histories
facility_origin: Facility = origin.get_facility()
print("Current Complete History - Facility origin")
print(facility_origin.get_complete_history())

facility_destination: Facility = destination.get_facility()
print("Current Complete History - Facility destination")
print(facility_destination.get_complete_history())

# Display current state of model and export it to JSON file
model_update = builder.get_model()
builder.export_model_to_file(model_update, "../data/dummy_model_export.json")
