__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "copy setupPostProcessingFolder"

import shutil
from pythonCode.computePostprocessingData import getString
from pythonCode.parsers.forceParser import parser
import pythonCode.settings.postProcessingPaths as settings
import os

def setupPostProcessing(path, targetFolder, transient, mach, alt, alfa, beta):

    sourceFolder = "transientSolver" if transient else "steadySolver"
    destinationFolder = path

    try:
        shutil.copytree(sourceFolder,destinationFolder)

    except Exception as e:
        pass

    forcesFile = os.path.join(path, settings.forcesTransient if transient else settings.forcesSteady)
    targetFolder = os.path.join(path, targetFolder)
    forcesAndTorques = parser(forcesFile)

    str1, str2 = getString(alt,mach, alfa, beta, forcesAndTorques)
    with open(os.path.join(targetFolder,"SIMULATION DATA"), 'w') as f:
        f.write(str1+str2)





