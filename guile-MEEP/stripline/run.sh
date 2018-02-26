meep stripline.ctl # &> out.log
cd stripline-out
read frames <<<$( h5ls ez.h5 | awk '{split($6,a,"/");print a[1]}' )
read y_len <<<$( h5ls ez.h5 | awk '{split($4,a,",");print a[1]}' )
y_len=$(($y_len - 1))
y_len=$(($y_len*3/4))
frames=$(($frames-1))
h5topng -y $y_len -t 0:$frames -R -Zc dkbluered -a yarg ez.h5
rm -rf img
mkdir img
mv *.png ./img/
python ../rename_images.py
cat ./img/*.png | ffmpeg -y -f image2pipe -i - output.mp4 &> /dev/null
