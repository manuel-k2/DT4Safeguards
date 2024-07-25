from project.projecttypes.command import Command
from project.projecttypes.location import Location

class TransportCmd(Command):
	"""
	A class that specifies a transport command from an origin to a destination.

	Attributes:
		origin (Location): Origin of transport.
		destination (Location): Destination of transport.
	"""
	origin: Location
	destination: Location

	def __init__(self, origin: Location, destination: Location):
		super().__init__()
		self.origin = origin
		self.destination = destination

	def GetOrigin(self):
		"""
		Get origin of transport.

		Returns:
			origin (Location): Origin of transport.
		"""
		return self.origin
	
	def GetDestintaion(self):
		"""
		Get destination of transport.

		Returns:
			destination (Location): Destination of transport.
		"""
		return self.destination
