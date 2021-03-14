__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "snappy hex mesh classes"

class refinementLevel:
	def __init__(self, minLevel, maxLevel):
		self.minLevel = minLevel
		self.maxLevel = maxLevel
	def __str__(self):
		return str(self.minLevel) + " " + str(self.maxLevel)

class boundaryControl:
	def __init__(self):
		self.control = []
		self.value = []

	def setTotalThickness(self,totalThickness):
		self.control.append("thickness")
		self.value.append(str(totalThickness))
	
	def setThicknessRatio(self,tcRatio):
		self.control.append("expansionRatio")
		self.value.append(str(tcRatio))

	def setFirstLayerThickness(self, tc):
		self.control.append("firstLayerThickness")
		self.value.append(str(tc))

	def setLastLayerThickness(self, tc):
		self.control.append("finalLayerThickness")
		self.value.append(str(tc))

	def __str__(self):
		return self.control[0] + "    " + self.value[0] + ";\n"+self.control[1] + "    " + self.value[1] + ";\n"

class snappyRefinement:
	def __init__(self, name, reflevel, point1, point2, radius):
		self.name = str(name)
		self.refinementLevel = str(reflevel)
		self.point1 = str(point1)
		self.point2 = str(point2)
		self.radius = str(radius)

	def getGeometryDescription(self):
		returnStr = geometryDescriptionStr
		returnStr = returnStr.replace("$name$", self.name)
		returnStr = returnStr.replace("$point1$", self.point1)
		returnStr = returnStr.replace("$point2$", self.point2)
		returnStr = returnStr.replace("$radius$", self.radius)
		return returnStr

	def getRefinementDescription(self):
		returnStr = refinementDescriptionStr
		returnStr = returnStr.replace("$name$", self.name)
		returnStr = returnStr.replace("$level$", self.refinementLevel)
		return returnStr 

class snappyConfiguration:
	def __init__(self):
		self.featureExtractLevel = None
		self.rocketRefineLevel = None
		self.boundaryLayers = None
		self.boundaryControl = None
		self.refinementZones = None
		self.domainCellSize = None



geometryDescriptionStr='''
$name$
    {
    type		    searchableCylinder;
    point1          ($point1$);
    point2          ($point2$);
    radius          $radius$;
    }
'''
refinementDescriptionStr = '''
$name$
	    {
		    mode inside;
		    levels (($level$));
	    }
'''
