#!/bin/bash

if [ ${#} != 1 ]
then
	echo "Usage: ./gen_smpl.sh workflow"
        echo "    workflow: lv, hs, gvpv"
	exit 1
fi

wf=$1

dir_name=../plot/combine

if [ ! -d ../plot ]
then
	mkdir ../plot
fi

if [ ! -d $dir_name ]
then
	mkdir $dir_name
fi

python combine.py $wf

