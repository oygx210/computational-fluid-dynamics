# OPENFOAM ROCKET SIMULATION 
Automatic compressible flow simulation setup and run for HERMES V1 rocket, developed by Skyward Experimental Rocketry.

# REQUIREMENTS
To run this simulation openfoam, cfmesh and python are required. 
You can compile cfmesh by following this link https://openfoamwiki.net/index.php/Extend-bazaar/utilities/cfMesh 

To install the python requirements you have to run the following command

`python3 -m pip  install -r requirements.txt`

# SETUP
In order to be able to use this code you must create the geometry domain file. 

To do this, go the meshSnappy/geo folder and execute the following command

`surfaceFeatureEdges geometry.stl geometry.fms`

This command will translate the domain .stl domain file into an .fms 
file that can be read by cfmesh.

# DOCUMENTATION
This repository provides the user with a python environment 
that will facilitate the correct setup of an openfoam simulation. 
This is by no means a replacement of openfoam setup files, rather 
a collection of routine that will automate part of the workload required
to correctly setup and run a parallel simulation. 

The parameters of the simulation can be modified in the **config.py** file. 

The python programm consits of two preprocessors, one processor and a postprocessor.
The preprocessors are used to compute the domain mesh and setup the simulation files, 
the processor will run the simulation and the 
postprocessor will read the solution files and produce relevant data.

Each module can be accessed running the **run.py** file. The correct 
workflow consists of 
1) Modifying the openfoam parameters that cannot be accessed by the **config.py** 
file. These files can be found inside the solver folder or in the templates folder.

2) Setting up the **config.py** with the desired parameters

3) running the executable with the following command `python3 run.py ARGS`

Each submodule can be accessed by calling **run.py** with the correct argument.
More modules can be run in the same call by adding more than one argument

#### MESH PREPROCESSOR
This module can be accessed by `python3 run.py -m`

It will compute the mesh and copy the mesh data in the solver folder 

#### SIMULATION PREPROCESSOR
This module can be accessed by `python3 run.py -s`

This submodule will setup the correct initial conditions, bash script files 
and decomposePar dictionaries.

#### RUN
This module can be accessed by `python3 run.py -r`

This command will run the simulation by calling the correct openfoam solver.

This command is equivalent to `./transientSolver/Allrun` or 
`./steadySolver/Allrun`

#### POSTPROCESSING
This module can be accessed by `python3 run.py -p`

This command will call the postProcessor and create a folder (simulation name)
with the relevant post-processing data.
