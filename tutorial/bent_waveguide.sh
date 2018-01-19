#!/bin/bash
mkdir ./bent_waveguide
cd ./bent_waveguide
echo "Running MEEP..."
python ../bent_waveguide.py
echo "Extracting images..."
rm *.png
read frames <<<$( h5ls bent_waveguide-ez.h5 | awk '{split($5,a,"/");print a[1]}')
frames=$(($frames-1))
h5topng -t 0:$frames -R -Zc dkbluered -a yarg -A bent_waveguide-eps-000000.00.h5 bent_waveguide-ez.h5
echo "Converting to gif..."
convert -loop 0 *.png out.gif
echo "Done"
