__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "aerodynamic routine"

from pythonCode.turbulenceModel import turbulenceCalculator
import pythonCode.settings.openFoamConventions as hermes
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
----------------------------------------------------
TORQUES (with respect to (0,0,0))

TX:
    total: {:10.4f} [Nm]
    viscous: {:10.4f} [Nm]
    pressure: {:10.4f} [Nm]
TY:
    total: {:10.4f} [Nm]
    viscous: {:10.4f} [Nm]
    pressure: {:10.4f} [Nm]
TZ:
    total: {:10.4f} [Nm]
    viscous: {:10.4f} [Nm]
    pressure: {:10.4f} [Nm]
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

    uinf = mach*speedOfSound
    Re, turbulentLengthScale, turbulentIntensity, k, w, epsilon, nut, nuTilda = turbulenceCalculator(hermes.LENGTH,uinf)

    returnInitialConditionString = initialConditionString.format(mach,alt, alfa,beta, uinf, temperature, pressure,
                                                                 speedOfSound, Re, turbulentLengthScale,
                                                                 turbulentIntensity,k,w,epsilon,nut, nuTilda)

    t, fxp, fyp, fzp, fxv, fyv, fzv, fxpp, fypp, fzpp, txp, typ, tzp, txv, tyv, tzv, txpp, typp, tzpp = forcesAndTorques[-1]

    returnAerodynamicString = aerodynamicString.format(fxv+fxp, fxv, fxp, fyp+fyv,fyp, fyv, fzp+fzv, fzv, fzp,
                                                       txp+txv, txv, txp, tyv+typ, tyv, typ, tzv+tzp, tzv, tzp)

    return  returnInitialConditionString, returnAerodynamicString
