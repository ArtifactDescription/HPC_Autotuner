#!/bin/bash

dir_name=../plot/combine

if [ ! -d ../plot ]
then
	mkdir ../plot
fi

if [ ! -d $dir_name ]
then
	mkdir $dir_name
fi

python combine.py

