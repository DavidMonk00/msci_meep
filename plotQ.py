import numpy as np
from matplotlib import pyplot as plt
import sys

def main():
    if (len(sys.argv) == 1):
        fname = "Q.txt"
    else:
        fname = sys.argv[1]
    data = np.loadtxt(fname,delimiter=",")
    plt.scatter(data[:,0],data[:,1])
    plt.show()

if (__name__ == '__main__'):
    main()
