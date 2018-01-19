#!/bin/bash
cd $1
echo "Extracting images..."
rm *.png
for i in *-ez.h5;
do
  read frames <<<$( h5ls $i | awk '{split($5,a,"/");print a[1]}')
  frames=$(($frames-1))
  PROG=$(echo $i| cut -d'-' -f 1)
  time h5topng -t 0:$frames -R -Zc dkbluered -a yarg -A $PROG-eps-000000.00.h5 $i
  echo "Converting to gif..."
  rm test.mp4
  time ffmpeg -r 10 -f image2 -i $PROG-ez.t%03d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p test.mp4
done
echo "Done"
