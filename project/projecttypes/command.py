from model.monitoringsystem import IDClass

class Command(IDClass):
	"""
	The base class for all instances that specify commands.

	Attributes:
		type (str): Type of command.
		targetID (int): ID of instance that is targeted by command.
	"""
	type: str
	targetID: int
	
	def __init__(self, cmdType: str, targetID: int):
		super().__init__()
		self.type = cmdType
		self.targetID = targetID

