#!/bin/bash

if [ ${#} -lt 1 ]
then
	echo "Usage: eg. $0 filenames"
	exit 1
fi

files=$(ls $@)
# files=$(ls ${@:1})
file_array=$(echo "$files" | tr "\t" "\n")

P="Elapsed (wall clock) time (h:mm:ss or m:ss): "

index=0
max=-1
for filename in ${file_array[@]}
do
	if grep --max-count=1 --quiet "$P" $filename
	then
		time_format=$(grep "$P" $filename | sed -e "s/$P//g" | sed -e "s/\t//g")
		time_array=$(echo "$time_format" | tr ":" "\n")
		sec=0
		for num in ${time_array[@]}
		do
			sec=$(($sec * 60))
			sec=$(bc -l <<<"$num + $sec")
		done
		# echo "$filename: $sec seconds"
		index=$(($index + 1))
		dir=$(dirname $filename)
		echo -e "$sec\c" > $dir/time$index.txt
		if (( $(echo "$sec > $max" | bc -l) ))
		then
			max=$sec
		fi
	else
		echo "Error: the time is unavailable in the file $filename ."
		exit 1
	fi
done
# echo "Max time = $max seconds"
echo -e "$max\c"
exit 0

