#!/bin/bash

if [ ${#*} != 1 ]
then
	echo "$0 TURBINE_OUTPUT"
	exit 1
fi

rootdir=$1
outfile="time_list"
if [[ -f $rootdir/$outfile.csv ]]
then
	mv $rootdir/$outfile.csv $rootdir/$outfile-bak.csv
fi

for runid in $(ls $rootdir/run)
do
	path="$rootdir/run/$runid"
	if [ -d "$path" ]
	then
		#echo -e "$runid\t\c" >> $rootdir/$outfile.csv
		#$PWD/get_maxtime.sh $path/time_pdf_calc.txt >> $rootdir/$outfile.csv
		cat $path/time.txt >> $rootdir/$outfile.csv
		echo "" >> $rootdir/$outfile.csv
	fi
done
# sort $rootdir/$outfile.csv

exit 0

