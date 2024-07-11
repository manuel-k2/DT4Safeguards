from project.projecttypes.command import Command
from project.projecttypes.location import Location

class TransportCmd(Command):

	origin: Location
	destination: Location

	def __init__(self):
		super().__init__(self)
		self.origin 
		self.destination

