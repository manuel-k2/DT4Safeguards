class Command:
	"""
	The base class for all instances that specify 

	Attributes:
		cmdType (str): A .
	"""

	cmdType: str
	cmdID: int
	targetID: int
	
	def __init__(self, cmdID: int, cmdType: str, targetID: int):
		self.cmdID = cmdID
		self.cmdType = cmdType
		self.targetID = targetID

