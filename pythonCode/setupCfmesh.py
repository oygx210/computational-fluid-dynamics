__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu, omar.kahol@mail.polimi.it"
__description__ = "setup loop for cfmesh"
__version__ = "4.0"

import pythonCode.settings.cfmeshPaths as settings
import os

def setupCfmesh(workingPath, config):

	#create the paths that have to be accessed
	cfmeshTemplatePath = os.path.join(workingPath, settings.cfmeshTemplatePath) #locate template folder
	meshdictPath = os.path.join(workingPath, settings.meshdictPath) #locate meshdict file

	#open the template 
	with open(cfmeshTemplatePath, 'r') as f:
		configString = f.read()

	#replace each entry with the config file value
	#----------------------------------------------------------------------------------
	# TODO ==> perform input validations
	#----------------------------------------------------------------------------------
	
	configString = configString.replace("$maxCellSize$", str(config.domainCellSize))
	configString = configString.replace("$rocketCellSize$", str(config.rocketCellSize))
	configString = configString.replace("$numLayers$", str(config.boundaryLayers))
	configString = configString.replace("$tcRatio$", str(config.thicknessRatio))
	configString = configString.replace("$maxFirstLayerThickness$", str(config.maxFirstlayerThickness))

	# refinement zones addition
	refinementString = ""
	for refZone in config.refinementZones:
		refinementString = refinementString + str(refZone)

	# replace the refinement zones template with the correct values
	configString = configString.replace("$customRefinementZones$",refinementString)

	# save results in the correct system file
	with open(meshdictPath, 'w') as f:
		f.write(configString)

	return True
	
