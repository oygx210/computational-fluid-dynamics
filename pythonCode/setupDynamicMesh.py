__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu, omar.kahol@mail.polimi.it"
__description__ = "setup loop for dynamic meshing"
__version__ = "4.0"

import pythonCode.settings.dynamicMeshPaths as settings
import os


def setupDynamicMesh(workingPath, configuration):

	#create paths
	templatePath = os.path.join(workingPath, settings.templatePath)
	filePath = os.path.join(workingPath, settings.filePath)

	#open template string
	with open(templatePath, 'r') as f:
		templateString = f.read()

	#replace templates with configuration values
	templateString = templateString.replace("$refineInterval$", str(configuration.refineInterval))
	templateString = templateString.replace("$refineField$", str(configuration.refineField))
	templateString = templateString.replace("$lowerRefineLevel$", str(configuration.lowerRefineLevel))
	templateString = templateString.replace("$upperRefineLevel$", str(configuration.upperRefineLevel))
	templateString = templateString.replace("$unrefineLevel$", str(configuration.unrefineLevel))
	templateString = templateString.replace("$maxRefinement$", str(configuration.maxRefinement))
	templateString = templateString.replace("$maxCells$", str(configuration.maxCells))

	#dump string in file
	with open(filePath, 'w') as f:
		f.write(templateString)

	return True

def removeDynamicMesh(workingPath):
	filePath = os.path.join(workingPath, settings.filePath)
	try:
		os.remove(filePath)
		return True
	except:
		return False
