import h5py
import numpy as np
from matplotlib import pyplot as plt
from glob import glob

def get1DSlice(data,dim,x1,x2,t):
    if (dim == "x"):
        return data[:,x1,x2,t]
    if (dim == "y"):
        return data[x1,75:,x2,t]
    if (dim == "z"):
        return data[x1,x2,:,t]

def plot1D(s,show=True):
    plt.plot(s)
    if (show):
        plt.show()

def main():
    dirs = glob("*/")
    output_directory = ""
    for i in dirs:
        if ("-out" in i):
            output_directory = i
    f = h5py.File(i + "ez.h5")["ez"]
    print f.shape
    #t = [0,50,100,150,200,250,300,350]
    # for i in t:
    #     plot1D(get1DSlice(f,"y",25,40,i),False)
    # plt.legend()
    # plt.show()
    slices = []
    for i in range(200,300):
        slices.append(get1DSlice(f,"x",280,40,i))
    slices = np.abs(slices)
    print slices
    plt.plot(np.mean(slices,axis=0))
    plt.show()

if (__name__ == "__main__"):
    main()
