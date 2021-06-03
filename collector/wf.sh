#!/bin/bash

if [ ${#*} != 1 ]
then
	echo "$0 TURBINE_OUTPUT"
	exit 1
fi

rootdir=$1
outfile="time_list"
if [[ -f $rootdir/$outfile.dat ]]
then
	mv $rootdir/$outfile.dat $rootdir/$outfile-bak.dat
fi

#echo -e "#Proc\tPPW\t#Thread\tIOstep\t#Proc\tPPW\t#Thread\tExecTime" >> $rootdir/$outfile.dat
for runid in $(ls $rootdir/run)
do
	path="$rootdir/run/$runid"
	if [ -d "$path" ]
	then
		if [ -f "$path/time.txt" ]
		then
			filesize=$(stat -c%s "$path/time.txt")
			if [ $filesize -gt 0 ]
			then
				cat $path/time.txt >> $rootdir/$outfile.dat
			elif [ -f "$path/time1.txt" ] && [ -f "$path/time2.txt" ]
			then
				echo -e "$runid\t\c" >> $rootdir/$outfile.dat
				$PWD/get_maxtime.sh $path/time_*.txt >> $rootdir/$outfile.dat
			fi
		elif [[ -f "$path/time1.txt" && -f "$path/time2.txt" ]]
		then
			echo -e "$runid\t\c" >> $rootdir/$outfile.dat
			$PWD/get_maxtime.sh $path/time_*.txt >> $rootdir/$outfile.dat
		fi
		echo -e "\t\c" >> $rootdir/$outfile.dat
		# head -c -1 -q $path/time1.txt >> $rootdir/$outfile.dat
		head -q $path/time1.txt >> $rootdir/$outfile.dat
		# cat $path/time1.txt >> $rootdir/$outfile.dat
		echo -e "\t\c" >> $rootdir/$outfile.dat
		# head -c -1 -q $path/time2.txt >> $rootdir/$outfile.dat
		head -q $path/time2.txt >> $rootdir/$outfile.dat
		# cat $path/time2.txt >> $rootdir/$outfile.dat
		echo "" >> $rootdir/$outfile.dat
	fi
done
# sort $rootdir/$outfile.dat

exit 0

