#!/bin/bash

if [ ${#} != 1 ]
then
	echo "Usage: ./gen_smpl.sh workflow"
        echo "    workflow: lv, hs, gvpv"
	exit 1
fi

wf=$1

if [ $wf == 'lv' ] && [ ! -d lv ] 
then
	mkdir lv
fi

if [ $wf == 'hs' ] && [ ! -d hs ]
then
	mkdir hs
fi

if [ $wf == 'gvpv' ] && [ ! -d gp ]
then
	mkdir gp
fi

python gen_smpl.py $wf

