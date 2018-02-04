import meep as mp
import numpy as np
from matplotlib import pyplot as plt
import os
from glob import glob
import h5py
import subprocess
import random
import string
from materials_library import *

vals = []
def get_slice(sim):
    center = mp.Vector3(15,0)
    size = mp.Vector3(0, 0)
    vals.append(sim.get_field_point(mp.Ez,center))

vals2 = []
def get_slice_start(sim):
    center = mp.Vector3(-15,0)
    size = mp.Vector3(0, 0)
    vals2.append(sim.get_field_point(mp.Ez,center))

w_vals = []
def get_waveguide_slice(sim):
    center = mp.Vector3(0,0)
    size = mp.Vector3(32, 0)
    w_vals.append(sim.get_array(center=center, size=size, component=mp.Ez))

class Model:
    def __init__(self, cell_x, cell_y, cell_z=0,dpml=1.0,output_directory='temp'):
        self.cell = mp.Vector3(cell_x,cell_y,cell_z)
        self.geometry = []
        self.sources = []
        self.pml_layers = [mp.PML(dpml)]
        self.output_directory = output_directory
    def addGeometry(self, geometry):
        self.geometry.append(geometry)
    def viewGeometry(self,resolution=10):
        tmp = ''.join(random.choice(string.ascii_lowercase) for _ in range(20))
        os.mkdir(tmp)
        sim = mp.Simulation(cell_size = self.cell,
                            boundary_layers = self.pml_layers,
                            geometry = self.geometry,
                            sources = self.sources,
                            resolution = resolution
                            )
        sim.use_output_directory(tmp)
        sim.run(mp.at_beginning(mp.output_epsilon),until=1)
        files = glob(tmp+"/*-eps-*.h5")
        for i in files:
            eps_h5file = h5py.File(i,'r')
            eps_data = np.array(eps_h5file['eps'])
            plt.figure(dpi=100)
            plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
            plt.axis('off')
            plt.show()
        for i in files:
            os.remove(i)
        os.removedirs(tmp)
    def addSource(self,source):
        self.sources.append(source)
    def simulate(self, resolution=10, until=200, output_directory='temp'):
        self.vals = []
        self.output_directory = output_directory
        self.sim = mp.Simulation(cell_size = self.cell,
                                 boundary_layers = self.pml_layers,
                                 geometry = self.geometry,
                                 sources = self.sources,
                                 resolution = resolution)
        try:
            os.mkdir(self.output_directory)
        except OSError:
            pass
        self.sim.use_output_directory(self.output_directory)
        self.sim.run(mp.at_beginning(mp.output_epsilon),
                     mp.to_appended("ez", mp.at_every(2, mp.output_efield_z)),
                     mp.at_every(2,get_slice),
                     mp.at_every(2,get_slice_start),
                     mp.at_every(2,get_waveguide_slice),
                     until=until)

def waveguide2D():
    width = 4
    length = 10.0
    period = 50
    M = Model(32, 16,dpml=0.2,output_directory='waveguide2D')
    M.addGeometry(mp.Block(mp.Vector3(1e20, 1e20, 1e20),center=mp.Vector3(0, 0),material=mp.Medium(epsilon=1)))
    M.addGeometry(mp.Block(mp.Vector3(1e20, width, 1e20),center=mp.Vector3(0, 0),material=mp.Medium(epsilon=100)))
    M.addGeometry(mp.Block(mp.Vector3(2, width, 1e20),center=mp.Vector3(-length/2 - 1, 0),material=mp.Medium(epsilon=1)))
    M.addGeometry(mp.Block(mp.Vector3(2, width, 1e20),center=mp.Vector3(length/2 + 1, 0),material=mp.Medium(epsilon=1)))
    # M.viewGeometry()
    M.addSource(mp.Source(mp.ContinuousSource(wavelength=period,width=10,end_time=20*period),
                          component=mp.Ez,
                          center=mp.Vector3(-15,0),
                          size=mp.Vector3(0,width)))
    M.simulate(resolution=20,until=20*period,output_directory='waveguide2D')
    plt.plot(vals)
    plt.plot(vals2)
    plt.show()
    plt.figure(dpi=100)
    plt.imshow(w_vals, interpolation='spline36', cmap='RdBu')
    plt.axis('off')
    plt.show()

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
    M.addSource(mp.Source(mp.GaussianSource(0.02, fwidth=0.01), mp.Ez, mp.Vector3(0.1)))
    M.simulate(until=1500,output_directory='temp')
    # M.sim.run(mp.at_beginning(mp.output_epsilon),
    #           mp.after_sources(mp.Harminv(mp.Ez, mp.Vector3(r + 0.1), 0.15, 0.1)),
    #           until_after_sources=300)

def main():
    waveguide2D()
    # ringResonator()

if (__name__ == '__main__'):
    main()
