#!/bin/bash -l

echo
echo "ADIOS2 starts ..."
echo

if (( ${#ROOT} == 0  ))
then
	echo "Set ROOT as the parent installation directory!"
	exit 1
fi

if [ -d $ROOT ]
then
	echo "Removing installed adios2 ..."
	rm -rf $ROOT/adios2
	mkdir -pv $ROOT/adios2
else
	echo "There does not exist $ROOT!"
	exit 1
fi

set -eu

echo
echo "Download ADIOS2 source code ..."
if [ -d ADIOS2 ]
then
	echo "Removing the previous ADIOS2 source code ..."
	rm -rf ADIOS2
fi
git clone https://github.com/ornladios/ADIOS2.git
cd ADIOS2
git checkout 78b5956c26aac8939f5cb3c6bd9f992e7361fc03

echo
echo "Build ADIOS2 ..."
echo 'mkdir adios2-build'
mkdir adios2-build
echo 'cd adios2-build'
cd adios2-build
echo 'cmake -DCMAKE_INSTALL_PREFIX=$ROOT/adios2 -DADIOS2_USE_Fortran=OFF ..'
cmake -DCMAKE_INSTALL_PREFIX=$ROOT/adios2 -DADIOS2_USE_Fortran=OFF ..
echo 'make -j 8'
make -j 8
echo 'make install'
make install
echo '../..'
cd ../..

echo 'source env-adios2.sh'
source env-adios2.sh
# export ADIOS2_HOME=$ROOT/adios2
# export PATH=$ADIOS2_HOME/bin:$PATH
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ADIOS2_HOME/lib64
# export PYTHONPATH=$ADIOS2_HOME/lib64/python3.6/site-packages

echo
echo "ADIOS2 is done!"
echo
