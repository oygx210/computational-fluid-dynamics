__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "cfmesh classes"

class cfmeshRefinement:
	def __init__(self, name, cellSize, point0, point1, radius0, radius1):
		self.name = name
		self.cellSize = str(cellSize)
		self.point0 = str(point0)
		self.point1 = str(point1)
		self.radius0 = str(radius0)
		self.radius1 = str(radius1)

	def __str__(self):
		returnStr = baseStr
		returnStr = returnStr.replace("$name$", self.name)
		returnStr = returnStr.replace("$cellSize$", self.cellSize)
		returnStr = returnStr.replace("$point0$", self.point0)
		returnStr = returnStr.replace("$point1$", self.point1)
		returnStr = returnStr.replace("$r0$", self.radius0)
		returnStr = returnStr.replace("$r1$", self.radius1)
		return returnStr

class cfmeshConfiguration:
	def __init__(self):
		self.domainCellSize = None
		self.rocketCellSize = None
		self.boundaryLayers = None
		self.thicknessRatio = None
		self.maxFirstlayerThickness = None
		self.refinementZones = None
		

baseStr = '''
$name$
    {
    type		       cone;
    cellSize		   $cellSize$;
    p0                 ($point0$);
    p1                 ($point1$);
    radius0            $r0$;
    radius1            $r1$;
    }
'''