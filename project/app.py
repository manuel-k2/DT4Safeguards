from model.monitoringsystem import MonitoringSystem
from model.facility import Facility
from model.historyclass import HistoryClass

from projecttypes.dimensions import Dimensions

hist1 = HistoryClass()
hist2 = HistoryClass()
hist3 = HistoryClass()

first_facility = Facility(name="Interim storage", dimensions=Dimensions(1,1,1))

print(first_facility.id)

MonitoringSystem.display_registry()
