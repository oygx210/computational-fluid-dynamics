__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "post processing routine"

import shutil
import numpy as np
from pythonCode.computePostprocessingData import getString
import pythonCode.parsers.forceParser as forceParser
import pythonCode.parsers.residualParser as residualParser
import pythonCode.settings.postProcessingPaths as settings
import pythonCode.plotters.plotAndSave as plt
import os

def returnFolderName(path,transient):
    searchPath = os.path.join(path,"{0}/postProcessing/computeForces".format(
        "transientSolver" if transient else "steadySolver"
    ))
    return os.listdir(searchPath)[0]


def setupPostProcessing(path, targetFolder, transient, mach, alt, alfa, beta):

#---------------------------------------------------------------------------------------
# COPY FOLDER
#---------------------------------------------------------------------------------------

    # sourceFolder = "transientSolver" if transient else "steadySolver"
    # destinationFolder = path
    #
    # try:
    #     shutil.copytree(sourceFolder,destinationFolder)
    #
    # except Exception as e:
    #     pass
#---------------------------------------------------------------------------------------
# MAIN FILE
#---------------------------------------------------------------------------------------
    dirName = returnFolderName(path,transient)
    forcesFile = os.path.join(path, settings.forcesTransient.format(dirName) if transient else settings.forcesSteady.format(dirName))
    targetFolder = os.path.join(path, targetFolder)
    forcesAndTorques = forceParser.parser(forcesFile)

    str1, str2 = getString(alt,mach, alfa, beta, forcesAndTorques)
    with open(os.path.join(targetFolder,"SIMULATION DATA"), 'w') as f:
        f.write(str1+str2)

#---------------------------------------------------------------------------------------
# FORCES
#---------------------------------------------------------------------------------------

    t, fxp, fyp, fzp, fxv, fyv, fzv, fxpp, fypp, fzpp, txp, typ, tzp, txv, tyv, tzv, txpp, typp, tzpp = \
        np.array([forcesAndTorques[:,i] for i in range(19)])

    variables = [fxp+fxv, fxp, fxv, fyp+fyv, fyp, fyv, fzp+fzv, fzp, fzv, txp+txv, txp, txv, typ+tyv, typ, tyv, tzp+tzv,
                 tzp,tzv]

    labels = ['FX', 'FXP','FXV','FY', 'FYP','FYV','FZ', 'FZP','FZV','TX', 'TXP','TXV','TY',
              'TYP','TYV','TZ', 'TZP','TZV']

    titleStr = "TREND FOR {0}"
    ylabelStr = "{0} [N]"
    saveStr = "plot_{0}.png"
    graphFolder = os.path.join(targetFolder,"PLOTS/FORCES")
    for var, label in zip(variables, labels):
        plt.plot(t,var,"t [s]" if transient else "",ylabelStr.format(label),
                 titleStr.format(label),os.path.join(graphFolder,saveStr.format(label)))

#---------------------------------------------------------------------------------------
# RESIDUALS
#---------------------------------------------------------------------------------------


    varNames, residuals = \
    residualParser.parser(os.path.join(path,settings.residualsTransient.format(dirName) if transient else settings.residualsSteady.format(dirName)))

    titleStr = "RESIDUAL OF {0}"
    saveStr = "plot_{0}_residual.png"
    ylabelStr = "{0} [-]"
    graphFolder = os.path.join(targetFolder,"PLOTS/RESIDUALS")
    time = residuals[:,0]
    for var, label in zip(residuals.T[1:],varNames[1:]):
        plt.plot(time[1:], var[1:], "t [s]" if transient else "", ylabelStr.format(label),
             titleStr.format(label), os.path.join(graphFolder, saveStr.format(label)),style='k-',lw=1)

#---------------------------------------------------------------------------------------
# DUMP CSV
#---------------------------------------------------------------------------------------

    np.savetxt(os.path.join(targetFolder,"CSV/forcesAndTorques.csv"),
               forcesAndTorques, header="Time, forces(pressure viscous porous), moments(pressure viscous porous)")
    np.savetxt(os.path.join(targetFolder,"CSV/residuals.csv"),residuals,header=', '.join(varNames))

