NPROC=$(nproc)
mpirun -np $NPROC meep-openmpi stripline.ctl # &> out.log
cd stripline-out
read frames <<<$( h5ls ez.h5 | awk '{split($6,a,"/");print a[1]}' )
read y_len <<<$( h5ls ez.h5 | awk '{split($4,a,",");print a[1]}' )
y_len=$(($y_len - 1))
y_len=$(($y_len*4/5))
frames=$(($frames-1))
h5topng -y $y_len -t 0:$frames -R -Zc dkbluered -a yarg ez.h5 -m -0.0025 -M 0.0025
rm -rf img
mkdir img
mv *.png ./img/
for i in ./img/*.png; do
  read x <<<$( identify $i | awk '{split($3,a,"x");print a[1]}' )
  read y <<<$( identify $i | awk '{split($3,a,"x");print a[2]}' )
  convert $i -crop $((x-4))x$((y-4))+2+2 $i
done
python ../rename_images.py
cat ./img/*.png | ffmpeg -y -f image2pipe -i - output.mp4 &> /dev/null
