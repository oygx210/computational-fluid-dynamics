__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "setup loop for the usable cores"

import pythonCode.settings.simulationCoresPath as settings
import os

def setupDecomposePar(workingPath, procs, transient):
    templatePath = os.path.join(workingPath, settings.decomposeParTemplate)
    filePath = os.path.join(workingPath, settings.decomposeParFileTransient if transient else settings.decomposeParFileSteady)

    if procs > 1:
        with open(templatePath, 'r') as f:
            dumpStr = f.read()

        dumpStr = dumpStr.replace("$numProcessors$",str(procs))

        with open(filePath, 'w') as f:
            f.write(dumpStr)

    else:
        try:
            os.remove(filePath)
        except:
            pass
    return True

def setupAllRun(workingPath, procs, renumber, transient):
    templatePath = os.path.join(workingPath, settings.allrunTemplate)
    filePath = os.path.join(workingPath, settings.allrunFileTransient if transient else settings.allrunFileSteady)

    with open(templatePath, 'r') as f:
        dumpStr = f.read()

    solver = "rhoPimpleFoam" if transient else "rhoSimpleFoam"
    runCommand = "mpirun -np {0} --oversubscribe {1} -parallel".format(procs, solver) if procs > 1 else solver

    renumberCommand = "mpirun -np {0} --oversubscribe renumberMesh -parallel".format(procs) if procs>1 and renumber else ""

    dumpStr = dumpStr.replace("$decomposePar$", "decomposePar -force" if procs>1 else "")
    dumpStr = dumpStr.replace("$renumberMesh$", renumberCommand)
    dumpStr = dumpStr.replace("$run$", runCommand)


    with open(filePath, 'w') as f:
        f.write(dumpStr)