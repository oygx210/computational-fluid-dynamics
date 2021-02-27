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
import argparse

# ARGUMENT PARSER
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mesh", action="store_true",
                    help="compute the mesh")
parser.add_argument("-s", "--simulationSetup", action="store_true",
                    help="setup the simulation files")
parser.add_argument("-r", "--run", action="store_true",
                    help="run the simulation")
parser.add_argument("-p", "--postProcessing", action="store_true",
                    help="proceed with postProcessing")
args = parser.parse_args()

# SOME IMPORTANT PARAMETERS MUST BE CALCULATED AT THE BEGINNING
transient = config.type[0].upper() == 'T'
path = os.getcwd()
directoryName = config.simulationName
folder = os.path.join(path, directoryName)

# ------------------------------------------------------------------------------------------------------
# MESH SETUP
# -----------------------------------------------------------------------------------------------------+
if args.mesh:
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

# -------------------------------------------------------------------------------------------------------
# SIMULATION SETUP
# -------------------------------------------------------------------------------------------------------
if args.simulationSetup:
    if config.activateDynamicMesh:
        if not setupDynamicMesh(path, config.dynamicMeshConfiguration):
            raise "Unable to setup dynamic mesh"
        else:
            print("dynamic dictionary written")
    else:
        removeDynamicMesh(path)
    setupAllRun(path, config.numberOfProcessors, config.renumberMesh,transient)
    setupDecomposePar(path, config.numberOfProcessors,transient)
    setupInitialConditions(path, config.alfa, config.beta, config.mach, config.alt, transient)

# -------------------------------------------------------------------------------------------------------
# SIMULATION RUN
# -------------------------------------------------------------------------------------------------------
if args.run:
    if transient:
        os.system('./transientSolver/Allrun')
    else:
        os.system('./steadySolver/Allrun')

# -------------------------------------------------------------------------------------------------------
# POSTPROCESSING
# -------------------------------------------------------------------------------------------------------
if args.postProcessing:
    #CREATE SIMULATION FOLDER
    try:
        os.mkdir(folder)
        os.mkdir(os.path.join(folder, "PLOTS"))
        os.mkdir(os.path.join(folder, "PLOTS/FORCES"))
        os.mkdir(os.path.join(folder, "PLOTS/RESIDUALS"))
        os.mkdir(os.path.join(folder, "CSV"))
    except Exception as e:
        pass
    #FILL IT WITH POST PROCESSING DATA
    setupPostProcessing(path,config.simulationName,transient, config.mach, config.alt, config.alfa, config.beta)