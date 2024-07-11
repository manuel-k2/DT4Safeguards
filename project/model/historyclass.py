from dataclasses import dataclass

from model.monitoringsystem import IDClass


@dataclass
class HistoryClass(IDClass):
	"""
	The base class for all instances that come with a history that
		tracks all changes made to the instance,

	"""
	
	def Activation(self, cmd):
		"""
		"""
		pass
	
	def UpdateHistory(self, cmdType, cmdId, targetId):
		"""
		"""
		pass
