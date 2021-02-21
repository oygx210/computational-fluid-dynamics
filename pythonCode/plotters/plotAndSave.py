__author__ = "Omar Kahol"
__email__ = "omar.kahol@skywarder.eu"
__description__ = "plot a variable and save it"

import matplotlib.pyplot as plt

def plot(x,y, xlabel, ylabel, title, dumpFile, style='ko-', lw=2):

    plt.plot(x,y,style,lw=lw)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.savefig(dumpFile)
    plt.close()
