#!/bin/bash
source activate pmp
#declare -a array=(5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0)
declare -a array=(1.96875 2.03125)
arraylength=${#array[@]}
for (( i=1; i<${arraylength}+1; i++ ));
do
  echo $i " / " ${arraylength} " : " ${array[$i-1]}
  mpirun -np 4 python model_builder.py ${array[$i-1]} &> out.log
done
source deactivate
sort Q.txt | uniq > temp.txt
mv temp.txt Q.txt
