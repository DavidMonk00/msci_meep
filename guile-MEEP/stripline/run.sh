NPROC=$(nproc)
echo "Setting variables..."
if [[ $# -eq 0 ]] ; then
    echo 'ERROR: No resolution given, please enter resolution for simulation as argument.'
    exit 0
fi
sed -i "s/param res .*)/param res $1)/g" ./stripline.ctl
echo "Running MEEP..."
mpirun -np $((NPROC/2)) meep-openmpi stripline.ctl # &> out.log

cd stripline-out

# Create y slice video
echo "Creating y-slice..."
read frames <<<$( h5ls ez.h5 | awk '{split($6,a,"/");print a[1]}' )
read y_len <<<$( h5ls ez.h5 | awk '{split($4,a,",");print a[1]}' )
y_len=$((($y_len-1)*4/5))
h5topng -y $y_len -t 0:$((frames-1)) -R -Zc dkbluered -a yarg ez.h5 # -m -0.02 -M 0.02
rm -rf img/y-slice
mkdir -p img/y-slice
mv *.png ./img/y-slice/
for i in ./img/y-slice/*.png; do
  read x <<<$( identify $i | awk '{split($3,a,"x");print a[1]}' )
  read y <<<$( identify $i | awk '{split($3,a,"x");print a[2]}' )
  convert $i -crop $((x-1))x$((y-1))+1+1 $i
done
python ../rename_images.py
cat ./img/y-slice/*.png | ffmpeg -y -f image2pipe -i - output_y_slice.mkv &> /dev/null

# Create z-slice at source
echo "Creating z-slice..."
read frames <<<$( h5ls ez.h5 | awk '{split($6,a,"/");print a[1]}' )
read z_len <<<$( h5ls ez.h5 | awk '{split($5,a,",");print a[1]}' )
z_len=$((($z_len-1)*7/10))
h5topng -z $z_len -t 0:$((frames-1)) -R -Zc dkbluered -a yarg ez.h5 # -m -0.002 -M 0.002
rm -rf img/z-slice
mkdir -p img/z-slice
mv *.png ./img/z-slice/
for i in ./img/z-slice/*.png; do
  read x <<<$( identify $i | awk '{split($3,a,"x");print a[1]}' )
  read y <<<$( identify $i | awk '{split($3,a,"x");print a[2]}' )
  convert $i -crop $((x-1))x$((y-1))+1+1 $i
done
python ../rename_images.py
cat ./img/z-slice/*.png | ffmpeg -y -f image2pipe -i - output_z_slice.mkv &> /dev/null
echo "Done."
