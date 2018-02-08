#!/bin/bash
source activate mp
#declare -a array=(5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0)
declare -a array=(12.431 12.432 12.433 12.434 12.435 12.436 12.437 12.438 12.439 12.441 12.442 12.443 12.444 12.445 12.446 12.447 12.448 12.449)
arraylength=${#array[@]}
for (( i=1; i<${arraylength}+1; i++ ));
do
  echo $i " / " ${arraylength} " : " ${array[$i-1]}
  python model_builder.py ${array[$i-1]} &> out.log
done
source deactivate
sort Q.txt | uniq > temp.txt
mv temp.txt Q.txt
