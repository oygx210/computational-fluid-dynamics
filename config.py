__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "simulation setup"

#imports
import pythonCode.meshClasses.cfmesh as cfmesh
import pythonCode.meshClasses.snappyhexmesh as snappy
from pythonCode.meshClasses.point import point
import pythonCode.meshClasses.dynamicMesh as dynamicMesh

#simulation batch name
simulationName = "simulazione0.7"

# --------------------------------------------------------------------------------------------
# MESHING PART
# This utility will "automatically" create the mesh
# Note, not all meshing can be done automatically. Please setup the template files properly
# --------------------------------------------------------------------------------------------
meshToUse = "snappy" #set it to cfmesh or snappy

#-------------------------------------------------CFMESH CONFIGURATION-------------------------------------------------------------------------------------------------------------
cfmeshConfiguration = cfmesh.cfmeshConfiguration()
cfmeshConfiguration.domainCellSize = 0.3 #cellSize of the domain
cfmeshConfiguration.rocketCellSize = 0.01 #cellSize near the rocket

cfmeshConfiguration.boundaryLayers = 1 #add boundaryLayers
cfmeshConfiguration.thicknessRatio = 1.3 #thickness ratio
cfmeshConfiguration.maxFirstlayerThickness = 0.00001 #maximum allowable thickness of the first layer

cfmeshConfiguration.refinementZones = [
	# cfmeshRefinement(NAME, CELLSIZE, POINT1, POINT2, RADIUS1, RADIUS2) ==> create a refinement zone shaped like a cone
	cfmesh.cfmeshRefinement("wake_superfine", 0.002, point(0.98, 0, 0), point(1.2, 0, 0), 0.05, 0.0692),
	cfmesh.cfmeshRefinement("wake_fine", 0.03, point(-1.4, 0, 0), point(2.5, 0, 0), 0.02, 0.541),
	cfmesh.cfmeshRefinement("wake_medium", 0.06, point(2.5, 0, 0), point(5, 0, 0), 0.76, 1.02),
	cfmesh.cfmeshRefinement("wake_coarse", 0.09, point(5, 0, 0), point(8, 0, 0), 0.76, 1.02),
	cfmesh.cfmeshRefinement("ogive_far", 0.06, point(-1.5, 0, 0), point(0.2, 0, 0), 0.7, 0.848),
	cfmesh.cfmeshRefinement("ogive_area", 0.01, point(-0.6, 0, 0), point(-1.5, 0, 0), 0.15, 0.15),
	cfmesh.cfmeshRefinement("ogive_narrow", 0.005, point(-1.02, 0, 0), point(-0.6, 0, 0), 0.03, 0.07),
	cfmesh.cfmeshRefinement("winglet_zone", 0.01, point(0.8, 0, 0), point(1.5, 0, 0), 0.15, 0.21)
]

#-------------------------------------------------SNAPPY HEX MESH CONFIGURATION-----------------------------------------------------------------------------------------------------
snappyConfiguration = snappy.snappyConfiguration()
snappyConfiguration.featureExtractLevel = 8  #refinement precision for feature extraction
snappyConfiguration.rocketRefineLevel = snappy.refinementLevel(7,7) #rocket feature refinement level, specify min and max level
snappyConfiguration.boundaryLayers = 10  #define number of boundary layers

snappyConfiguration.boundaryControl = snappy.boundaryControl() #add a boundary control
snappyConfiguration.boundaryControl.setFirstLayerThickness(2.0e-5)
snappyConfiguration.boundaryControl.setTotalThickness(1.5e-3)

snappyConfiguration.refinementZones = [
	snappy.snappyRefinement("wake_coarse", snappy.refinementLevel(2,3), point(-1.4, 0, 0), point(8,0,0), 0.4),
	snappy.snappyRefinement("ogive", snappy.refinementLevel(4,5), point(-1.1, 0, 0), point(-0.55,0,0), 0.15),

	snappy.snappyRefinement("winglet",     snappy.refinementLevel(6,7), point(0.85, 0, 0), point(1.05,0,0), 0.15),

	snappy.snappyRefinement("wake_near_1", snappy.refinementLevel(6,7), point(1.0, 0, 0), point(1.2,0,0), 0.075),
	snappy.snappyRefinement("wake_near_2", snappy.refinementLevel(5,6), point(0.95, 0, 0), point(1.5,0,0), 0.1),
	snappy.snappyRefinement("wake_near_3", snappy.refinementLevel(4,5), point(0.8, 0, 0), point(2.5,0,0), 0.15)
]
# -------------------------------------------------------------------------------

#-------------------------------------------------DYNAMIC MESH CONFIGURATION-----------------------------------------------------------------------------------------------------
activateDynamicMesh = False

dynamicMeshConfiguration = dynamicMesh.dynamicMeshConfiguration()
dynamicMeshConfiguration.refineInterval = 100
dynamicMeshConfiguration.refineField = "nut"
dynamicMeshConfiguration.lowerRefineLevel = 0.00001
dynamicMeshConfiguration.upperRefineLevel = 0.5
dynamicMeshConfiguration.unrefineLevel = 0.000001
dynamicMeshConfiguration.maxRefinement = 4
dynamicMeshConfiguration.maxCells = 4000000
# -------------------------------------------------------------------------------

#-------------------------------------------------SIMULATIONS--------------------------------------------------------------------------------------------
numberOfProcessors = 8
renumberMesh = True

type = "steady" #set to steady or transient

alfa = 0
beta = 0
mach = 0.30
alt = 0.0
