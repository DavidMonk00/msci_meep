from __future__ import division
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import meep as mp
import numpy as np
warnings.simplefilter(action='ignore', category=np.ComplexWarning)
from matplotlib import pyplot as plt
import sys
from model.Model import Model
from model.Model import vals
from model.materials_library import *

def waveguide3D(length=12.44,impedence_width=1.969,sweep=True):
    width = 0.5
    fcen = 0.1
    df = 0.075
    dims = (16,4,4)
    M = Model(dims[0],dims[1],cell_z=dims[2],dpml=0.2,output_directory='waveguide3D')
    M.addGeometry(mp.Block(mp.Vector3(1e20, 1e20, 1e20),center=mp.Vector3(0, 0, 0),material=mp.Medium(epsilon=1)))
    M.addGeometry(mp.Block(mp.Vector3(1e20, width, width),center=mp.Vector3(0, 0, 0),material=mp.Medium(epsilon=100)))
    # M.addGeometry(mp.Block(mp.Vector3(impedence_width, width, width),center=mp.Vector3(-length/2 - impedence_width/2, 0, 0),material=mp.Medium(epsilon=1)))
    # M.addGeometry(mp.Block(mp.Vector3(impedence_width, width, width),center=mp.Vector3(length/2 + impedence_width/2, 0, 0),material=mp.Medium(epsilon=1)))
    # M.addGeometry(mp.Block(mp.Vector3(length, width, width),center=mp.Vector3(0, 0, 0),material=mp.Medium(epsilon=50)))
    #M.viewGeometry()
    if (sweep):
        M.addSource(mp.Source(src=mp.GaussianSource(fcen, fwidth=df),
                              component=mp.Ez,
                              center=mp.Vector3(-dims[0]/2 + 0.5,0,0)))
        M.simulateSweep(fcen,df,resolution=10,until=100/fcen,output_directory='waveguide3D')
    else:
        freq = 0.02
        M.addSource(mp.Source(mp.ContinuousSource(frequency=freq,width=5,end_time=2.5/freq),
                              component=mp.Ez,
                              center=mp.Vector3(-dims[0]/2 + 1,0,0),
                              size=mp.Vector3(width,width,width)))
        M.simulate(resolution=20,until=5/freq,output_directory='waveguide3D')
        # plt.plot(vals[1])
        # plt.plot(vals[0])
        # plt.plot(vals[2])
        # plt.show()
        # # n = "img/l_%.3f.png"%(length)
        # # plt.savefig(n)
        # # with open("Q.txt", 'a') as f:
        # #     f.write("%f,"%(impedence_width)+str(max(np.real(np.array(vals3[-100:])))/max(np.real(np.array(vals2[-100:]))))+"\n")
        # plt.figure(dpi=100)
        # plt.imshow(vals[3], interpolation='spline36', cmap='RdBu')
        # plt.axis('off')
        # plt.show()

def waveguide2D(length=8,impedence_width=1.969,sweep=True):
    width = 1
    fcen = 0.1
    df = 0.075
    dims = (16,4)
    M = Model(dims[0],dims[1],dpml=0.2,output_directory='waveguide2D')
    M.addGeometry(mp.Block(mp.Vector3(1e20, 1e20, 1e20),center=mp.Vector3(0, 0),material=mp.Medium(epsilon=1)))
    M.addGeometry(mp.Block(mp.Vector3(1e20, width),center=mp.Vector3(0, 0),material=mp.Medium(epsilon=100)))
    M.addGeometry(mp.Block(mp.Vector3(impedence_width, width),center=mp.Vector3(-length/2 - impedence_width/2, 0),material=mp.Medium(epsilon=1)))
    M.addGeometry(mp.Block(mp.Vector3(impedence_width, width),center=mp.Vector3(length/2 + impedence_width/2, 0),material=mp.Medium(epsilon=1)))
    M.addGeometry(mp.Block(mp.Vector3(length, width),center=mp.Vector3(0, 0),material=mp.Medium(epsilon=50)))
    #M.viewGeometry()
    if (sweep):
        M.addSource(mp.Source(src=mp.GaussianSource(fcen, fwidth=df),
                              component=mp.Ez,
                              center=mp.Vector3(0,0)))
        M.simulateSweep(fcen,df,resolution=10,until=100/fcen,output_directory='waveguide2D')
    else:
        freq = 0.0717422431795
        M.addSource(mp.Source(mp.ContinuousSource(frequency=freq,width=1,end_time=50/freq),
                              component=mp.Ez,
                              center=mp.Vector3(-dims[0]/2 + 1),
                              size=mp.Vector3(width,width)))
        M.simulate(resolution=20,until=100/freq,output_directory='waveguide2D')
        # plt.plot(vals[1])
        # plt.plot(vals[0])
        # plt.plot(vals[2])
        # plt.show()
        # # n = "img/l_%.3f.png"%(length)
        # # plt.savefig(n)
        # # with open("Q.txt", 'a') as f:
        # #     f.write("%f,"%(impedence_width)+str(max(np.real(np.array(vals3[-100:])))/max(np.real(np.array(vals2[-100:]))))+"\n")
        # plt.figure(dpi=100)
        # plt.imshow(vals[3], interpolation='spline36', cmap='RdBu')
        # plt.axis('off')
        # plt.show()

def ringResonator():
    n = 3.4  # index of waveguide
    w = 5  # width of waveguide
    r = 5  # inner radius of ring
    pad = 4  # padding between waveguide and edge of PML
    dpml = 2  # thickness of PML
    sxy = 2 * (r + w + pad + dpml)  # cell size

    M = Model(sxy, sxy, dpml=2.0)
    M.addGeometry(mp.Cylinder(radius=r + w, material=Ag))
    M.addGeometry(mp.Cylinder(radius=r))
    M.addSource(mp.Source(mp.GaussianSource(0.02, fwidth=0.01), mp.Ez, mp.Vector3(0,0)))
    M.simulate(until=1500,output_directory='temp')
    # M.sim.run(mp.at_beginning(mp.output_epsilon),
    #           mp.after_sources(mp.Harminv(mp.Ez, mp.Vector3(r + 0.1), 0.15, 0.1)),
    #           until_after_sources=300)

def rectangularCavity():
    r = 1.25
    l = 16
    s = l*r
    w = 4
    d = l/16
    dpml = s/16
    sx = s
    sy = s
    fcen = 0.2
    df = 0.3
    res = 16
    M = Model(sx,sy,dpml=dpml)
    M.addGeometry(mp.Block(mp.Vector3(l,d,mp.inf),
                           center=mp.Vector3(0,(w+d)/2,0),
                           material=Cu))
    M.addGeometry(mp.Block(mp.Vector3(l,d,mp.inf),
                           center=mp.Vector3(0,-(w+d)/2,0),
                           material=Cu))
    M.addGeometry(mp.Block(mp.Vector3(d,w,mp.inf),
                           center=mp.Vector3((l+d)/2,0,0),
                           material=Cu))
    M.addGeometry(mp.Block(mp.Vector3(d,w,mp.inf),
                           center=mp.Vector3(-(l+d)/2,0,0),
                           material=Cu))
    M.addSource(mp.Source(mp.GaussianSource(fcen,fwidth=df),
                          component=mp.Ez,
                          center=mp.Vector3(0,0,0),
                          size=mp.Vector3(0,0,0)))
    M.simulate(resolution=res,until=1/fcen,output_directory='rectangularCavity')
    # for i in vals[2]:
    #     print imshow(vals[3], interpolation='spline36', cmap='RdBu')
    plt.axis('off')
    plt.show()
    # x = [20,40,60,80,100,110,120,130,140,150]
    # for i in x:
    #     plt.plot(vals[2][:i])
    #     plt.show()
    plt.figure(dpi=100)
    plt.imshow(vals[3][:80], interpolation='spline36', cmap='RdBu')
    plt.axis('off')
    plt.show()

def main():
    # length = 10.0
    # if (len(sys.argv) > 1):
    #     length = float(sys.argv[1])
    #     i_w = float(sys.argv[2])
    waveguide2D(sweep=False)
    # ringResonator()
    # rectangularCavity()

if (__name__ == '__main__'):
    main()
