import numpy as np
from matplotlib import pyplot as plt

def main():
    data = np.loadtxt("Q.txt", delimiter=",")
    plt.scatter(data[:,0], data[:,1])
    plt.show()

if (__name__ == '__main__'):
    main()
