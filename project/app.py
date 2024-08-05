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
# container_1.get_location().print_location()

# Move container by sending Transport sepecifications to Commander
target = container_1
origin = container_1.get_location()
destination = holding_area_destination.get_location()
destination.set_holding_area(holding_area_destination)

commander = Commander()
commander.issue_transport_command(target, origin, destination)

# Print new container location and history
# print("\nLocation - Container 1 (PostTransport)")
# container_1.get_location().print_location()
# print("\nHistory - Container 1")
# container_1.print_history()

# Print facility histories
facility_1: Facility = MonitoringSystem.get_instance(id=0)
print("History - Facility 1")
facility_1.print_history()

# facility_2: Facility = MonitoringSystem.get_instance(id=7)
# print("History - Facility 2")
# facility_2.print_history()

# Display current state of model and export it to JSON file
model_update = builder.get_model()
builder.export_model_to_file(model_update, "../data/dummy_model_export.json")
