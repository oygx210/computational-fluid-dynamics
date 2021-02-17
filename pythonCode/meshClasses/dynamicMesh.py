__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu, omar.kahol@mail.polimi.it"
__description__ = "dynamic mesh parameters"
__version__ = "4.0"


class dynamicMeshConfiguration:
	def __init__(self):
		self.refineInterval = None 
		self.refineField = None
		self.lowerRefineLevel = None
		self.upperRefineLevel = None
		self.unrefineLevel = None
		self.maxRefinement = None
		self.maxCells = None
	