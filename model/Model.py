from __future__ import division
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import meep as mp
import h5py
import numpy as np
warnings.simplefilter(action='ignore', category=np.ComplexWarning)
import os
from glob import glob
from matplotlib import pyplot as plt
import random
import string

vals = [[],[],[],[]]
def get_slice(sim):
    center = mp.Vector3(7.5,0,0)
    size = mp.Vector3(0, 0, 0)
    vals[0].append(sim.get_field_point(mp.Ez,center))

def get_slice_start(sim):
    center = mp.Vector3(-7.5,0,0)
    size = mp.Vector3(0, 0 ,0)
    vals[1].append(sim.get_field_point(mp.Ez,center))

def get_slice_middle(sim):
    center = mp.Vector3(0,0,0)
    size = mp.Vector3(0, 0, 0)
    vals[2].append(sim.get_field_point(mp.Ez,center))

def get_waveguide_slice(sim):
    center = mp.Vector3(0,0,0)
    size = mp.Vector3(16, 0, 0)
    vals[3].append(sim.get_array(center=center, size=size, component=mp.Ez))

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
                            dimensions=3,
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
            if (len(eps_data.transpose().shape) == 2):
                plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
            else:
                plt.imshow(eps_data.transpose()[:,40,:], interpolation='spline36', cmap='binary')
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
                                 dimensions = 2 if self.cell[2] == 0 else 3,
                                 boundary_layers = self.pml_layers,
                                 geometry = self.geometry,
                                 sources = self.sources,
                                 resolution = resolution)
                                 # symmetries=[mp.Mirror(mp.Y)])
        try:
            os.mkdir(self.output_directory)
        except OSError:
            pass
        self.sim.use_output_directory(self.output_directory)
        self.sim.run(mp.at_beginning(mp.output_epsilon),
                     mp.to_appended("ez", mp.at_every(1/(20), mp.output_efield_z)),
                     mp.at_every(2,get_slice),
                     mp.at_every(2,get_slice_start),
                     mp.at_every(0.01,get_slice_middle),
                     mp.at_every(0.01,get_waveguide_slice),
                     until=until)
    def simulateSweep(self, fcen, df, resolution=10, until=200, output_directory='temp'):
        self.sim = mp.Simulation(cell_size = self.cell,
                                 boundary_layers = self.pml_layers,
                                 dimensions = 2 if self.cell[2] == 0 else 3,
                                 geometry = self.geometry,
                                 sources = self.sources,
                                 resolution = resolution)
                                 # symmetries=[mp.Mirror(mp.Y),mp.Mirror(mp.X)])
        self.sim.run(mp.after_sources(mp.Harminv(mp.Ez, mp.Vector3(1.0,0.0), fcen, df)),
                     until_after_sources=200)
