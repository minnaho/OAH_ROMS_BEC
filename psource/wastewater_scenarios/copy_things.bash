#!/bin/bash
#======================================================#
# Cigdem Akan (akanc@ucla.edu)
# REVISION: 30-September-2016
# LAST REVISION: 2-March-2017 (Faycal Kessouri kesf@ucla.edu)
#======================================================#
ns=0;
ne=383;

T1=$(date +%s)

for (( n=ns; n<=ne; n+=1 ))
do
 if (( n<10 )); then
     echo $n
     cp roms_psource_pndn90.nc roms_psource_pndn90.00$n.nc
 elif (( n<100 )); then
     echo $n
     cp roms_psource_pndn90.nc roms_psource_pndn90.0$n.nc
 else
     echo ">>> " $n
     cp roms_psource_pndn90.nc roms_psource_pndn90.$n.nc
 fi
done
T2=$(date +%s)
diffsec="$(expr $T2 - $T1)"
