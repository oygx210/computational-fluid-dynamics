__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "turbulence calculator"

from math import *

def turbulenceCalculator(L, U, viscosity=1.8e-5, turbulentIntensity=None, turbulentLengthScale=None):
#   TURBULENCE CALCULATOR
#   inputs:
#       1) L ==> a reference length, could be the rocket length or the rocket diameter [m]
#       2) U ==> a reference velocity, usually the freestream velocity magnitude
#       3) kinematic viscosity ==> viscosity of the fluid, default is air, [m^2/s]
#       4) turbulentIntensity of the flow, if None will be calculated based of Re, otherwise specify in %
#       5) turbulentLengthScale ==> characteristic dimension of turbulent eddies. If None will be calculated
#   outputs:
#       1) Reynolds number
#       2) Turbulent length scale
#       3) Turbulence Intensity
#       4) Turbulent Kinetic energy, k
#       5) Specific dissipation rate, w
#       6) Turbulence dissipation rate, epsilon
#       7) Turbulent viscosity, nut
#       8) Modified turbulent viscosity, nutilda

    Cmu = 0.09
    Re = U*L/viscosity

    if turbulentLengthScale is None:
        turbulentLengthScale=0.07*L

    if turbulentIntensity is None:
        turbulentIntensity = 0.16 * Re**(-1./8)

    nut = sqrt(3./2)*U*turbulentIntensity*turbulentLengthScale
    k = 1.5*(U*turbulentIntensity)**2
    epsilon = (Cmu**(3./4.)) * k**(1.5) / turbulentLengthScale
    w = (Cmu ** (-0.25)) * sqrt(k) / turbulentLengthScale
    nuTilda = nut/5
    return Re, turbulentLengthScale, turbulentIntensity, k, w, epsilon, nut, nuTilda
