__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "simulation run"

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
from pythonCode.setupSimulationCores import setupAllRun, setupDecomposePar
from pythonCode.setupPostProcessing import setupPostProcessing

# CREATE SIMULATION FOLDER
path = os.getcwd()
directoryName = config.simulationName
folder = os.path.join(path, directoryName)

try:
    os.mkdir(folder)
    os.mkdir(os.path.join(folder,"PLOTS"))
    os.mkdir(os.path.join(folder, "PLOTS/FORCES"))
    os.mkdir(os.path.join(folder, "PLOTS/RESIDUALS"))
    os.mkdir(os.path.join(folder,"CSV"))
except Exception as e:
    pass

# ------------------------------------------------------------------------------------------------------
# MESH SETUP
# -----------------------------------------------------------------------------------------------------+
transient = config.type[0].upper() == 'T'

if config.recomputeMesh:

    if config.meshToUse[0].upper() == 'C':
        os.system('./meshCfmesh/Allclean')

        # try to setup the cfmesh dict file
        if not setupCfmesh(path, config.cfmeshConfiguration):
            raise "Unable to write the cfmesh dict"
        else:
            print("mesh files written")
        os.system('./meshCfmesh/Allrun')
        setupMesh(path, False, transient)
    else:
        if not setupSnappyhexmesh(path, config.snappyConfiguration):
            raise "Unable to write snappyHexMesh dict"
        else:
            print("mesh files written")
        os.system('./meshSnappy/Allclean')
        os.system('./meshSnappy/Allrun')
        setupMesh(path, True, transient)

else:
    pass

print("SUCCESFULLY SETUP MESH")

# ------------------------------------------------------------------------------------------------------
# DYNAMIC MESHING
# -----------------------------------------------------------------------------------------------------+
if config.activateDynamicMesh:
    if not setupDynamicMesh(path, config.dynamicMeshConfiguration):
        raise "Unable to setup dynamic mesh"
    else:
        print("dynamic dictionary written")
else:
    removeDynamicMesh(path)

# -------------------------------------------------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------------------------------------------------
setupAllRun(path, config.numberOfProcessors, config.renumberMesh,transient)
setupDecomposePar(path, config.numberOfProcessors,transient)
setupInitialConditions(path, config.alfa, config.beta, config.mach, config.alt, transient)

if config.automaticRun:
    if transient:
        os.system('./transientSolver/Allrun')
    else:
        os.system('./steadySolver/Allrun')

if config.doPostProcessing:
    setupPostProcessing(path,config.simulationName,transient, config.mach, config.alt, config.alfa, config.beta)