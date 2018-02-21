import os
from glob import glob
import math

output_folders = glob("./*/")
output_folder = ""
for i in output_folders:
    if "-out" in i:
        output_folder = i
images = glob(output_folder+"*.png")
images.sort()
for i in range(len(images)):
    parts = images[i].split("ez")
    fname_new = parts[0] + 'ez-{:06d}.png'.format(i)
    os.rename(images[i], fname_new)