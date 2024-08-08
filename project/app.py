from model.components import MonitoringSystem, Facility, HoldingArea, Container
from model.components import Builder, Commander


# Create model with Builder by loading data from a JSON file
builder = Builder()
# model = builder.load_dummy_model()
model = builder.load_model_from_file("../data/dummy_model.json")

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
start_time = "2024:04:04.09:42"
end_time = "2024:04:04.11:08"

commander = Commander()
commander.issue_transport_command(
    target, origin, destination, start_time, end_time
)

# Move container back to origin afterwards
start_time2 = "2024:08:06.13:12"
end_time2 = "2024:08:06.14:19"
commander.issue_transport_command(
    target, destination, origin, start_time2, end_time2
)

# Print Holding area instance histories
print("Current Instance History - Holding area origin")
print(holding_area_origin.get_instance_history())

print("Initial Instance History - Holding area origin")
print(holding_area_origin.get_instance_history().at_time("2024:05:01.00:00"))

print("Intermediate Instance History - Holding area origin")
print(holding_area_origin.get_instance_history().at_time("2024:01:01.00:00"))


print("Current Instance History - Holding area destination")
print(holding_area_destination.get_instance_history())

print("Intermediate Instance History - Holding area destination")
print(
    holding_area_destination.get_instance_history().at_time("2024:05:01.00:00")
)
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

# Export current state of model to a JSON file
builder.export_model_state("../data/dummy_model_export.json")

# Print History with ongoing commands at specific time
time = "2024:08:06.13:13"
print(f"Ongoing commands at time {time}")
print(MonitoringSystem.get_ongoing_commands_at_time(time))

# Export state of model at specific time to a JSON file
time2 = "2024:05:01.00:00"
builder.export_model_state(
    "../data/dummy_model_at_time_export.json", time2
)
