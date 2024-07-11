from model.historyclass import HistoryClass

from projecttypes.dimensions import Dimensions

class Room(HistoryClass):

	name: str
	dimensions: Dimensions

	def __init__(self, name, dimensions):
		self.name = name
		self.dimensions = dimensions

	def CheckForEquipment(self):
		pass

	def PresentExitInventory(self):
		pass

