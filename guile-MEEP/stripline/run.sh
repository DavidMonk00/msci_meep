meep stripline.ctl &> out.log
cd stripline-out
read frames <<<$( h5ls ez.h5 | awk '{split($6,a,"/");print a[1]}' )
frames=$(($frames-1))
h5topng -y 150 -t 0:$frames -R -Zc dkbluered -a yarg -A eps-000000.00.h5 ez.h5
rm -rf img
mkdir img
mv *.png ./img/
python ../rename_images.py
cat ./img/*.png | ffmpeg -y -f image2pipe -i - output.mp4
