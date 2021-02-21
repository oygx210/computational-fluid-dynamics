__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "representation of a point"

class point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	def __str__(self):
		return "{0} {1} {2}".format(self.x, self.y, self.z)