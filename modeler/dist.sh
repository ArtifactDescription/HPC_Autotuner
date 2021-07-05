#!/bin/bash

if [ ${#} != 2 ]
then
	echo "Usage: ./dist.sh workflow performance"
        echo "    workflow: lv, hs, gvpv"
        echo "    performance: exec_time, comp_time"
	exit 1
fi

wf=$1
perfn=$2

dir_name=../plot/dist

if [ ! -d ../plot ]
then
	mkdir ../plot
fi

if [ ! -d $dir_name ]
then
	mkdir $dir_name
fi

python dist.py $wf $perfn

