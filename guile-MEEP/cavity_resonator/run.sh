rm -rf cavity_resonator-out/*.png
meep cavity_resonator_sweep.ctl | awk '/harminv/ {print $2, $4}'
meep cavity_resonator.ctl &> out.log
python rename_images.py
cat ./cavity_resonator-out/*.png | ffmpeg -y -f image2pipe -i - output.mp4
