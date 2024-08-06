from model.components import MonitoringSystem, Facility, HoldingArea, Container
from model.components import Builder, Commander


# Create model with Builder by loading data from a JSON file
builder = Builder()
# model = builder.load_dummy_model()
model = builder.load_model_from_file("../data/dummy_model.json")
builder.build_model(model)

# Get container and holding area from registry
container_1: Container = MonitoringSystem.get_instance(id=3)
holding_area_destination: HoldingArea = MonitoringSystem.get_instance(id=10)

# print("\nLocation - Container 1 (PreTransport): ")
# print(container_1.get_location())

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

# Print new container location and history
# print("\nLocation - Container 1 (PostTransport)")
# print(container_1.get_location())
# print("\nHistory - Container 1")
# print(container_1.get_history())

# Print facility histories
facility_1: Facility = MonitoringSystem.get_instance(id=0)
print("Current History - Facility 1")
print(facility_1.get_history())

print("Initial History - Facility 1")
print(facility_1.get_history_at_time("2024:01:01.00:00"))

# facility_2: Facility = MonitoringSystem.get_instance(id=7)
# print("History - Facility 2")
# print(facility_2.get_history())

# Display current state of model and export it to JSON file
model_update = builder.get_model()
builder.export_model_to_file(model_update, "../data/dummy_model_export.json")
