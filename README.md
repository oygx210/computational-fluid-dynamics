# HERMES V1 FLOW SIMULATION
Automatic compressible flow simulation setup and run for HERMES V1 rocket, developed by Skyward Experimental Rocketry.

# REQUIREMENTS
To run this simulation openfoam, cfmesh and python are required. You can compile cfmesh by following this link https://openfoamwiki.net/index.php/Extend-bazaar/utilities/cfMesh 
NOTE => CURRENTLY cfmesh does not work with openfoam 8

# PART ONE MESH GENERATION
In the geometry folder you will find the ROCKET.STEP file which constains the geometry of the rocket and for .stl files which define the boundaries of the domain. These file are useful ONLY if you want to use the cfmesh utility to generate a mesh. If you want to use another software, you only need to ROCKET.STEP file. The mesh should then be converted to an OpenFOAM format. If you are planning to use cfmesh just follow the steps

STEP ZERO (already done)

With a CAD software modify the ROCKET.STEP file to create a suitable simulation domain. You will have to save all the boundaries of that domain (like the inlet, outlet, walls and the rocket) into different .stl files. This can be easily achieved using salome https://www.code-aster.org/V2/spip.php?article303

STEP ONE (already done)

From the geo folder, run "./stlCombine" to combine the 4 .stl files into a single geometry.stl file

STEP TWO

From the geo folder, run "surfaceFeatureEdges geometry.stl geometry.fms" to convert the stl file into an fms file

STEP THREE

From the main folder, run "cartesianMesh" to create a mesh. The mesh parameters can be found and changed in the system/meshDict file. You can read this guide for some references http://cfmesh.com/wp-content/uploads/2015/09/User_Guide-cfMesh_v1.1.pdf

STEP FOUR

From the main folder, run "changeDictionary" to update the boundaries. This command will just assign the correct physical type to each boundary in the constant/polyMesh/boundary file

# PART TWO SIMULATION SETUP AND RUN
There are three main ways to run this simulation

1) From the main folder, run "rhoSimpleFoam" to run the simulation once
2) From the main folder, run "./Allrun". 
    NOTE ==> This file will run a simulation in parallel, please modify it properly before running it.
3) Use the run.py script 
    NOTE ==> This file allows you to automate the process. Since it uses the Allrun bash script, modify that file properly. 



