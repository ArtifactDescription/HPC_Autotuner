#!/bin/bash

if [ ${#*} != 2 ]
then
	echo "$0 TURBINE_OUTPUT NUM_APPS"
	exit 1
fi

rootdir=$1
num_apps=$2
outfile="time_list"
if [[ -f $rootdir/$outfile.csv ]]
then
	mv $rootdir/$outfile.csv $rootdir/$outfile-bak.csv
fi

#echo -e "#Proc\tPPW\t#Thread\tIOstep\t#Proc\tPPW\t#Thread\tExecTime" >> $rootdir/$outfile.csv
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
				cat $path/time.txt >> $rootdir/$outfile.csv
			fi
		fi

		if [ $num_apps -eq 2 ] && [[ -f "$path/time1.txt" && -f "$path/time2.txt" ]]
		then
			if [ ! -f "$path/time.txt" ] || [ $filesize -le 0 ]
			then
				echo -e "$runid\t\c" >> $rootdir/$outfile.csv
				$PWD/../get_maxtime.sh $path/time_*.txt >> $rootdir/$outfile.csv
			fi
			echo -e "\t\c" >> $rootdir/$outfile.csv
			head -q $path/time1.txt >> $rootdir/$outfile.csv
			echo -e "\t\c" >> $rootdir/$outfile.csv
			head -q $path/time2.txt >> $rootdir/$outfile.csv
		elif [ $num_apps -eq 3 ] && [[ -f "$path/time1.txt" && -f "$path/time2.txt" && -f "$path/time3.txt" ]]
		then
			if [ ! -f "$path/time.txt" ] || [ $filesize -le 0 ]
			then
				echo -e "$runid\t\c" >> $rootdir/$outfile.csv
				$PWD/../get_maxtime.sh $path/time_*.txt >> $rootdir/$outfile.csv

			fi
			echo -e "\t\c" >> $rootdir/$outfile.csv
			head -q $path/time1.txt >> $rootdir/$outfile.csv
			echo -e "\t\c" >> $rootdir/$outfile.csv
			head -q $path/time2.txt >> $rootdir/$outfile.csv
			echo -e "\t\c" >> $rootdir/$outfile.csv
			head -q $path/time3.txt >> $rootdir/$outfile.csv
		elif [ $num_apps -eq 4 ] && [[ -f "$path/time1.txt" && -f "$path/time2.txt" && -f "$path/time3.txt" && -f "$path/time4.txt" ]]
		then
			if [ ! -f "$path/time.txt" ] || [ $filesize -le 0 ]
			then
				echo -e "$runid\t\c" >> $rootdir/$outfile.csv
				$PWD/../get_maxtime.sh $path/time_*.txt >> $rootdir/$outfile.csv
			fi
			echo -e "\t\c" >> $rootdir/$outfile.csv
			head -q $path/time1.txt >> $rootdir/$outfile.csv
			echo -e "\t\c" >> $rootdir/$outfile.csv
			head -q $path/time2.txt >> $rootdir/$outfile.csv
			echo -e "\t\c" >> $rootdir/$outfile.csv
			head -q $path/time3.txt >> $rootdir/$outfile.csv
			echo -e "\t\c" >> $rootdir/$outfile.csv
			head -q $path/time4.txt >> $rootdir/$outfile.csv
		fi
		echo "" >> $rootdir/$outfile.csv
	fi
done
# sort $rootdir/$outfile.csv

exit 0

