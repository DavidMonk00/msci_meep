import meep as mp
import numpy as np
from matplotlib import pyplot as plt
import h5py
import argparse

def main():
    cell = mp.Vector3(32, 32, 0)
    geometry = [
        mp.Block(mp.Vector3(26, 4, 1e20),
                 center=mp.Vector3(-5, -7),
                 material=mp.Medium(epsilon=1.5)),
        mp.Block(mp.Vector3(4, 26, 1e20),
                 center=mp.Vector3(7, 4),
                 material=mp.Medium(epsilon=1.5))
    ]
    pml_layers = [mp.PML(1.0)]
    resolution = 10
    sources = [
        mp.Source(mp.ContinuousSource(  wavelength=50,
                                        width=20),
                                        component=mp.Ez,
                                        center=mp.Vector3(-14,-7),
                                        size=mp.Vector3(0,4))
    ]
    sim = mp.Simulation(cell_size=cell,
                        boundary_layers=pml_layers,
                        geometry=geometry,
                        sources=sources,
                        resolution=resolution)
    sim.run(mp.at_beginning(mp.output_epsilon),
            mp.to_appended("ez", mp.at_every(1, mp.output_efield_z)),
            until=400)

if (__name__ == '__main__'):
    main()
