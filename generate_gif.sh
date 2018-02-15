#!/bin/bash
cd $1
echo "Extracting images..."
rm *.png
for i in *-ez.h5;
do
  read frames <<<$( h5ls $i | awk '{split($6,a,"/");print a[1]}')
  frames=$(($frames-1))
  PROG=$(echo $i| cut -d'-' -f 1)
  time h5topng -y 40 -t 0:$frames -R -Zc dkbluered -a yarg -A $PROG-eps-000000.00.h5 $i
  echo "Converting to gif..."
  rm test.mp4
  time ffmpeg -y -r 30 -f image2 -i $PROG-ez.t%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p out_y_40.mp4
done
echo "Done"
