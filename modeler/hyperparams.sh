#!/bin/bash

if [ ${#} != 6 ]
then
	echo "Usage: ./hyperparams.sh py_filename workflow performance #sample #runs algorithm"
        echo "    py_filename: num_iter, pct_rand, pct_repl"
        echo "    workflow: lv, hs, gvpv"
        echo "    performance: exec_time, comp_time"
        echo "    number of samples: 25, 50, 100"
        echo "    #runs: 10, 100"
        echo "    algorithm: al, geist, alic, ceal, alph, alich, cealh"
	exit 1
fi

param=$1
wf=$2
perfn=$3
num_smpl=$4
num_run=$5
algo=$6

dir_name=plot/$param/$wf'_'$perfn

if [ ! -d plot ]
then
	mkdir plot
fi

if [ ! -d plot/$param ]
then
	mkdir plot/$param
fi

if [ ! -d $dir_name ]
then
	mkdir $dir_name
fi

filename=$param'.py'
python $filename $wf $perfn $num_smpl $num_run $algo

