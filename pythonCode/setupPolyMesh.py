__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu, omar.kahol@mail.polimi.it"
__description__ = "setup loop for polymesh folder"
__version__ = "4.0"

import pythonCode.settings.polyMeshPaths as settings
import os
import shutil

def copytree(source,dest):
    os.mkdir(dest)
    dest_dir = os.path.join(dest,os.path.basename(source))
    shutil.copytree(source,dest_dir)

def setupMesh(workingPath, mesh): # mesh: 0 for cfmesh, 1 for snappyhexmesh
    targetPath = os.path.join(workingPath, settings.transientPolyMeshPath)
    originalPath = None
    if mesh == 0:
        originalPath = os.path.join(workingPath, settings.cfmeshPath)
    elif mesh == 1:
        originalPath = os.path.join(workingPath, settings.snappyhexmeshPath)
    else:
        raise "unknown mesh"

    try:
        shutil.rmtree(targetPath)
    except:
        pass

    shutil.copytree(originalPath, targetPath, symlinks=False, ignore=None)
    return True


