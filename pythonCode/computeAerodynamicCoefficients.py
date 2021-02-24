__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "compute aerodynamic coefficients"

import pythonCode.settings.openFoamConventions as rocket
from math import *
import numpy as np

def computeCoefficients(FX,FY,FZ,TX,TY,TZ,qd, alfa, beta):
    Surface = (pi/4)*rocket.DIAMETER**2
#ROTATION TENSOR
    alfa = radians(alfa)
    beta = radians(beta)

    R_body_wind = np.array([[cos(beta)*cos(alfa),-sin(alfa)*cos(beta),-sin(beta)],
                            [sin(alfa),cos(alfa),0],
                            [sin(beta)*cos(alfa), -sin(alfa)*sin(beta),cos(beta)]])
#FORCES IN THE WIND FRAME
    D, L, S = R_body_wind.dot(np.array([FX,FY,FZ]))

#COEFFICIENTS IN THE WIND FRAME
    Cd, Cl, Cs = np.array([FX,FY,FZ]) / (qd*Surface)

#MOMENTS WRT ROCKET TIP
    YawingMomentTip = TY + FZ*rocket.XR
    PitchingMomentTip = TZ + FY*rocket.XR

#MOMENTS WRT ROCKET CG
    YawingMomentCG = TY + FZ * (rocket.XR + rocket.XCG)
    PitchingMomentCG = TZ + FY * (rocket.XR + rocket.XCG)

#MOMENTS COEFFICIENTS
    CYT = YawingMomentTip/(qd*Surface*rocket.LENGTH)
    CYCG = YawingMomentCG / (qd * Surface * rocket.LENGTH)

    CPT = PitchingMomentTip/(qd*Surface*rocket.LENGTH)
    CPCG = PitchingMomentCG / (qd * Surface * rocket.LENGTH)



    return (D,L,S,Cd,Cl,Cs,YawingMomentTip,PitchingMomentTip,YawingMomentCG,PitchingMomentCG,CYT,CYCG,CPT,CPCG)