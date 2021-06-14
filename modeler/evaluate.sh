#!/bin/bash

if [ ${#} != 4 ]
then
	echo "Usage: ./evaluate.sh workflow performance #sample #runs"
        echo "    workflow: lv, hs, gvpv"
        echo "    performance: exec_time, comp_time"
        echo "    number of samples: 25, 50, 100"
        echo "    #runs: 10, 100"
	exit 1
fi

wf=$1
perfn=$2
num_smpl=$3
num_run=$4

dir_name=plot/$wf/$perfn

if [ ! -d plot ]
then
	mkdir plot
fi

if [ ! -d plot/$wf ]
then
	mkdir plot/$wf
fi

if [ ! -d $dir_name ]
then
	mkdir $dir_name
fi

python evaluate.py $wf $perfn $num_smpl $num_run

