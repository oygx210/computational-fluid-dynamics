__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "forces parser"

import numpy as np

def parser(filePath):
    with open(filePath, 'r') as f:

        for i in range(1,4):
            f.readline()

        rawStr = f.read()

    rawStr = rawStr.replace("\n", ";")
    rawStr = rawStr.replace("(","")
    rawStr = rawStr.replace(")","")

    rawStr = ','.join(rawStr.split())
    data = [line.split(',') for line in rawStr.split(';')]
    return np.array(data[0:-1], dtype=float)




