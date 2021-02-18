__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu, omar.kahol@mail.polimi.it"
__description__ = "simulation run"
__version__ = "4.0"

try: 
	import config as config
except Exception as e:
	raise "The configuration file was not setup properly..."
import os
from pythonCode.setupCfmesh import setupCfmesh
from pythonCode.setupDynamicMesh import setupDynamicMesh, removeDynamicMesh
from pythonCode.setupSnappyhexmesh import setupSnappyhexmesh
from pythonCode.setupPolyMesh import setupMesh
from pythonCode.setupInitialConditions import setupInitialConditions
from pythonCode.setupSimulationCores import setupAllRun,setupDecomposePar
os.system('rm -r debug')

#CREATE SIMULATION FOLDER
path = os.getcwd()
directoryName = config.simulationName
folder = os.path.join(path, directoryName)

try:
	os.mkdir(folder)
	print("successfully created simulation folder")
except Exception as e:
	raise "Error: cannot create the simulation folder requested, maybe it already exists (?)."

#------------------------------------------------------------------------------------------------------
# MESH SETUP
# -----------------------------------------------------------------------------------------------------+
if config.recomputeMesh:
	
	if config.meshToUse[0].upper() == 'C':
		os.system('./meshCfmesh/Allclean')

		# try to setup the cfmesh dict file
		if not setupCfmesh(path, config.cfmeshConfiguration):
			raise "Unable to write the cfmesh dict"
		else:
			print("mesh files written")
		os.system('./meshCfmesh/Allrun')
		setupMesh(path, 0)
	else:
		if not setupSnappyhexmesh(path, config.snappyConfiguration):
			raise "Unable to write snappyHexMesh dict"
		else:
			print("mesh files written")
		os.system('./meshSnappy/Allclean')
		os.system('./meshSnappy/Allrun')
		setupMesh(path, 1)

else:
	pass

print("SUCCESFULLY SETUP MESH")

#------------------------------------------------------------------------------------------------------
# DYNAMIC MESHING
# -----------------------------------------------------------------------------------------------------+
if config.activateDynamicMesh:
	if not setupDynamicMesh(path, config.dynamicMeshConfiguration):
		raise "Unable to setup dynamic mesh"
	else:
		print("dynamic dictionary written")
else:
	removeDynamicMesh(path)

#-------------------------------------------------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------------------------------------------------
setupAllRun(path,config.numberOfProcessors,config.renumberMesh)
setupDecomposePar(path,config.numberOfProcessors)

if config.numberOfSimulations > 0:
	setupInitialConditions(path,config.alfa,config.beta,config.mach,config.alt)
