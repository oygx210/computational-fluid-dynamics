__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu, omar.kahol@mail.polimi.it"
__description__ = "setup loop for the useable cores"
__version__ = "4.0"

import pythonCode.settings.simulationCoresPath as settings
import os

def setupDecomposePar(workingPath, procs):
    templatePath = os.path.join(workingPath, settings.decomposeParTemplate)
    filePath = os.path.join(workingPath, settings.decomposeParFile)

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

def setupAllRun(workingPath, procs, renumber):
    templatePath = os.path.join(workingPath, settings.allrunTemplate)
    filePath = os.path.join(workingPath, settings.allrunFile)

    with open(templatePath, 'r') as f:
        dumpStr = f.read()

    parallelRun = "mpirun -np {0} --oversubscribe {1} -parallel"

    dumpStr = dumpStr.replace("$decomposePar$", "decomposePar -force" if procs>1 else "")
    dumpStr = dumpStr.replace("$renumberMesh$", parallelRun.format(procs,"renumberMesh") if procs > 1 and renumber else "")
    dumpStr = dumpStr.replace("$run$", parallelRun.format(procs, "rhoPimpleFoam") if procs > 1 else "rhoPimpleFoam")
    dumpStr = dumpStr.replace("$reconstruct$", "reconstructPar" if procs > 1 else "")


    with open(filePath, 'w') as f:
        f.write(dumpStr)