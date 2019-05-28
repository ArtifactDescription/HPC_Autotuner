#!/bin/bash -l

echo
echo "Anaconda2 starts ..."
echo

if (( ${#ROOT} == 0  ))
then
	echo "Set ROOT as the parent installation directory!"
	exit 1
fi

if [ -d $ROOT ]
then
	echo "Removing anaconda2 ..."
	rm -rf $ROOT/anaconda2
else
	echo "There does not exist $ROOT!"
	exit 1
fi

set -eu


echo
echo "Download and install Anaconda ..."
echo
rm -fv Anaconda2-5.3.1-Linux-x86_64.sh
if wget -q https://repo.anaconda.com/archive/Anaconda2-5.3.1-Linux-x86_64.sh
then
	echo WARNING: wget exited with: $?
fi
chmod +x Anaconda2-5.3.1-Linux-x86_64.sh
./Anaconda2-5.3.1-Linux-x86_64.sh -p $ROOT/anaconda2
export PATH=$ROOT/anaconda2/bin:$PATH
conda create -n codar python=2.7
export PATH=$ROOT/anaconda2/envs/codar/bin:$PATH


echo
echo "Anaconda2 is done!"
echo

