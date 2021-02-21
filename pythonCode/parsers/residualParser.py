__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "residuals parser"

import numpy as np

def parser(filePath):
    with open(filePath, 'r') as f:

        f.readline()
        varNames = (','.join(f.readline().replace('#','').split())).split(',')
        rawStr = f.read()

    rawStr = rawStr.replace("\n", ";")

    rawStr = ','.join(rawStr.split())
    data = [line.split(',') for line in rawStr.split(';')]
    return varNames, np.array(data[0:-1], dtype=float)