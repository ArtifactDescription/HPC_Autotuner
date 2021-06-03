#!/bin/bash
lineIdx=0
while IFS='' read -r line || [[ -n "$line" ]]
do
	line=$(echo $line)
	if [ "$line" != "" ]
	then
		line=$(echo $line | sed -e "s/_/\t/g")
		line=$(echo $line | sed -e "s/ /\t/g")
		echo $line
	fi
done < "$1"

