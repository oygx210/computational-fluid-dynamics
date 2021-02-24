__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "aerodynamic routine"

from pythonCode.turbulenceModel import turbulenceCalculator
import pythonCode.settings.openFoamConventions as hermes
from pythonCode.computeAerodynamicCoefficients import computeCoefficients
from ambiance import Atmosphere

aerodynamicString='''----------------------------------------------------
AERODYNAMIC DATA
computed using the last iteration of the solver
----------------------------------------------------
FORCES 

FX:
    total: {:10.4f} [N]
    viscous: {:10.4f} [N]
    pressure: {:10.4f} [N]
FY:
    total: {:10.4f} [N]
    viscous: {:10.4f} [N]
    pressure: {:10.4f} [N]
FZ:
    total: {:10.4f} [N]
    viscous: {:10.4f} [N]
    pressure: {:10.4f} [N]

FORCES IN THE WIND FRAME

D: {:10.4f} [N]
L: {:10.4f} [N]
S: {:10.4f} [N]

COEFFICIENTS (adimensionalized by the frontal surface)

CD: {:10.4f} [-]
CL: {:10.4f} [-]
CS: {:10.4f} [-]
----------------------------------------------------
TORQUES CONVENTION

Rolling Moment:
    A positive rolling moment tends to rotate 
    the rocket in the postive direction 
    identified by the first body axis.
    This axis goes from the end to the tip.

Yawing Moment:
    A positive yawing moment tends to rotate 
    the tip of the rocket towards the
    observer. This is equivalent to a positive
    rotation along the lift axis.

Pitching Moment:
    A positive pitching moment will increase the
    angle of attack.

All torques are adimensionalized by the rocket length.
----------------------------------------------------
TORQUES in (0,0,0)

Rolling Moment:
    total: {:10.4f} [Nm]
    viscous: {:10.4f} [Nm]
    pressure: {:10.4f} [Nm]
Yawing Moment:
    total: {:10.4f} [Nm]
    viscous: {:10.4f} [Nm]
    pressure: {:10.4f} [Nm]
Pitching Moment:
    total: {:10.4f} [Nm]
    viscous: {:10.4f} [Nm]
    pressure: {:10.4f} [Nm]
----------------------------------------------------
TORQUES AT THE ROCKET TIP 

Yawing Moment:
    value: {:10.4f} [Nm]
    coefficient: {:10.4f} [-]
Pitching Moment:
    value: {:10.4f} [Nm]
    coefficient: {:10.4f} [-]
----------------------------------------------------
TORQUES AT THE ROCKET C.G. 

Yawing Moment:
    value: {:10.4f} [Nm]
    coefficient: {:10.4f} [-]
Pitching Moment:
    value: {:10.4f} [Nm]
    coefficient: {:10.4f} [-]
----------------------------------------------------
'''

initialConditionString = '''----------------------------------------------------
INITIAL CONDITIONS
----------------------------------------------------
SIMULATION SETUP

MACH: {:10.4f} [-]
ALTITUDE: {:10.4f} [m]
ANGLE OF ATTACK: {:10.4f} [°]
ANGLE OF SIDESLIP: {:10.4f} [°]
U_INF = {:10.4f} [m/s]
----------------------------------------------------
ATMOSPHERIC DATA

TEMPERATURE: {:10.4f} [K]
PRESSURE: {:10.4f} [m]
DENSITY: {:10.4f} [kg/m^3]
SPEED OF SOUND: {:10.4f} [m/s]
----------------------------------------------------
TURBULENCE PROPERTIES

Reynolds number: {:10.4f} [-]
turbulent length scale: {:10.4f} [m]
turbulent intensity: {:10.4f} [%]
k: {:10.4f} [J]
w: {:10.4f} [J]
epsilon: {:10.4f} [J]
nut: {:10.4f} [m^2/s]
nuTilda: {:10.4f} [m^2/s]
'''

def getString(alt, mach, alfa, beta, forcesAndTorques):
    global initialConditionString, aerodynamicString
    atm = Atmosphere(alt)
    pressure = atm.pressure[0]
    speedOfSound = atm.speed_of_sound[0]
    temperature = atm.temperature[0]
    dens = atm.density[0]

    uinf = mach*speedOfSound
    Re, turbulentLengthScale, turbulentIntensity, k, w, epsilon, nut, nuTilda = turbulenceCalculator(hermes.LENGTH,uinf)

    returnInitialConditionString = initialConditionString.format(mach,alt, alfa,beta, uinf, temperature, pressure, dens,
                                                                 speedOfSound, Re, turbulentLengthScale,
                                                                 turbulentIntensity,k,w,epsilon,nut, nuTilda)

    t, fxp, fyp, fzp, fxv, fyv, fzv, fxpp, fypp, fzpp, txp, typ, tzp, txv, tyv, tzv, txpp, typp, tzpp = forcesAndTorques[-1]
    D, L, S, Cd, Cl, Cs, YawingMomentTip, PitchingMomentTip, YawingMomentCG, PitchingMomentCG, CYT, CYCG, CPT, CPCG = computeCoefficients(fxv+fxp,
                                                                                                                                          fyv+fyp,
                                                                                                                                          fzv+fzp,
                                                                                                                                          txv+txp,
                                                                                                                                          tyv+typ,
                                                                                                                                          tzv+tzp,
                                                                                                                                          0.5*dens*uinf**2,
                                                                                                                                          alfa,
                                                                                                                                          beta)


    returnAerodynamicString = aerodynamicString.format(fxv+fxp, fxv, fxp, fyp+fyv,fyp, fyv, fzp+fzv, fzv, fzp,
                                                       D,L,S,Cd,Cl,Cs,
                                                       -txp-txv, -txv, -txp, tyv+typ, tyv, typ, -tzv-tzp, -tzv, -tzp,
                                                       YawingMomentTip,CYT,-PitchingMomentTip,-CPT,
                                                       YawingMomentCG,CYCG,-PitchingMomentCG,-CPCG)



    return  returnInitialConditionString, returnAerodynamicString
