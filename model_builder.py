import meep as mp
import numpy as np
from matplotlib import pyplot as plt
import os
from glob import glob
import h5py
import subprocess
import random
import string

# cell = mp.Vector3(16, 8, 0)
# geometry = []
# sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
#             component=mp.Ez,
#             center=mp.Vector3(-7,0))]
# pml_layers = [mp.PML(1.0)]
# resolution = 10
# sim = mp.Simulation(cell_size=cell,
#                     boundary_layers=pml_layers,
#                     geometry=geometry,
#                     sources=sources,
#                     resolution=resolution)
# sim.run(mp.at_beginning(mp.output_epsilon),
#         mp.at_end(mp.output_efield_z),
#         until=200)

class Model:
    def __init__(self, cell_x, cell_y, cell_z=0,output_directory='temp'):
        self.cell = mp.Vector3(cell_x,cell_y,cell_z)
        self.geometry = []
        self.sources = []
        self.pml_layers = [mp.PML(1.0)]
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
                     until=until)

def main():
    M = Model(64, 32)
    M.addGeometry(mp.Block(mp.Vector3(1e20, 1e20, 1e20),center=mp.Vector3(0, 0),material=mp.Medium(epsilon=12)))
    M.addGeometry(mp.Block(mp.Vector3(1e20, 20, 1e20),center=mp.Vector3(0, 0),material=mp.Medium(epsilon=1)))
    M.addGeometry(mp.Block(mp.Vector3(1e20, 10, 1e20),center=mp.Vector3(0, 0),material=mp.Medium(epsilon=12)))
    #M.viewGeometry()
    M.addSource(mp.Source(mp.ContinuousSource(frequency=0.2,width=20),component=mp.Ez,center=mp.Vector3(-31,0),size=mp.Vector3(0,10)))
    M.simulate(until=600)

if (__name__ == '__main__'):
    main()
