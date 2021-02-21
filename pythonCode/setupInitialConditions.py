__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu, omar.kahol@mail.polimi.it"
__description__ = "setup loop for the initial conditions"
__version__ = "4.0"

from math import *
import numpy as np
from ambiance import Atmosphere
import pythonCode.settings.initialConditionsPath as settings
from pythonCode.turbulenceModel import turbulenceCalculator
import os

def rotateVelocity(vel, alfa, beta):
    alfa, beta = np.radians([alfa, beta])
    return vel * np.array([cos(alfa) * cos(beta), sin(beta), sin(alfa) * cos(beta)])

def setupInitialConditions(workingPath,alfa, beta, mach, altitude, transient):

    #PATHS
    templatePath = os.path.join(workingPath, settings.templatePath)
    filePath = os.path.join(workingPath, settings.filePathTransient if transient else settings.filePathSteady)

    #ATMOSPHERIC MODEL
    atm = Atmosphere(altitude)
    temp = atm.temperature[0]
    press = atm.pressure[0]
    dens = atm.density[0]
    c = atm.speed_of_sound[0]
    vel = c*mach
    u = rotateVelocity(vel, alfa, beta)

    #TURBULENCE PARAMETERS
    Re, turbulentLengthScale, turbulentIntensity, k, w, epsilon, nut, nuTilda = turbulenceCalculator(0.15, vel)

    #OPEN TEMPLATE
    with open(templatePath, 'r') as f:
        dumpStr = f.read()

    #SUBSTITUTE PARAMETERS IN TEMPLATE
    dumpStr = dumpStr.replace("%ux%", str(round(u[0],3)))
    dumpStr = dumpStr.replace("%uy%", str(round(u[1],3)))
    dumpStr = dumpStr.replace("%uz%", str(round(u[2],3)))
    dumpStr = dumpStr.replace("%pressure%", str(round(press,3)))
    dumpStr = dumpStr.replace("%densityRef%", str(round(dens,3)))
    dumpStr = dumpStr.replace("%temperature%", str(round(temp,3)))
    dumpStr = dumpStr.replace("%nut%", str(round(nut,5)))
    dumpStr = dumpStr.replace("%k%", str(round(k,5)))
    dumpStr = dumpStr.replace("%w%", str(round(w,5)))
    dumpStr = dumpStr.replace("%Uinf%", str(round(vel,3)))
    dumpStr = dumpStr.replace("%nuTilda%", str(round(nuTilda,5)))

    #DUMP FILE
    with open(filePath, 'w') as f:
        f.write(dumpStr)

    return True