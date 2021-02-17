__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu, omar.kahol@mail.polimi.it"
__description__ = "simple point class implementation"
__version__ = "4.0"

class point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	def __str__(self):
		return "{0} {1} {2}".format(self.x, self.y, self.z)