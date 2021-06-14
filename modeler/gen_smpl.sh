#!/bin/bash

if [ ! -d lv ]
then
	mkdir lv
fi

if [ ! -d hs ]
then
	mkdir hs
fi

if [ ! -d gp ]
then
	mkdir gp
fi

python gen_smpl.py

