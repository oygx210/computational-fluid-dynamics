__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "setup loop for snappyhexmesh"

import pythonCode.settings.snappyhexmeshPaths as settings
import os

def setupSnappyhexmesh(workingPath, config):

	#create the paths that have to be accessed
	snappyTemplatePath = os.path.join(workingPath, settings.snappyhexmeshTemplatePath) #locate template folder
	meshdictPath = os.path.join(workingPath, settings.meshdictPath) #locate meshdict file

	#open the template 
	with open(snappyTemplatePath, 'r') as f:
		configString = f.read()

	#replace each entry with the config file value
	#----------------------------------------------------------------------------------
	# TODO ==> perform input validations
	#----------------------------------------------------------------------------------
	
	configString = configString.replace("$featureExtractLevel$", str(config.featureExtractLevel))
	configString = configString.replace("$rocketLevel$", str(config.rocketRefineLevel))
	configString = configString.replace("$numLayers$", str(config.boundaryLayers))
	configString = configString.replace("$boundaryControls$", str(config.boundaryControl))

	# refinement zones addition
	refinementZoneString = ""
	refinementLevelString = ""
	for refZone in config.refinementZones:
		refinementZoneString = refinementZoneString + refZone.getGeometryDescription()
		refinementLevelString = refinementLevelString + refZone.getRefinementDescription()


	# replace the refinement zones template with the correct values
	configString = configString.replace("$refinementZones$",refinementZoneString)
	configString = configString.replace("$refinementLevels$",refinementLevelString)

	# save results in the correct system file
	with open(meshdictPath, 'w') as f:
		f.write(configString)

	return True
	
