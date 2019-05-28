#!/bin/bash -l

echo
echo "ADIOS starts ..."
echo

if (( ${#ROOT} == 0  ))
then
	echo "Set ROOT as the parent installation directory!"
	exit 1
fi

if [ -d $ROOT ]
then
	mkdir -pv $ROOT/adios
else
	echo "There does not exist $ROOT!"
	exit 1
fi

set -eu

echo
echo "Download ADIOS ..."
if [ -f adios-1.13.1.tar.gz ]
then
	rm -fv adios-1.13.1.tar.gz
fi
if wget -q https://users.nccs.gov/~pnorbert/adios-1.13.1.tar.gz
then
	echo WARNING: wget exited with: $?
fi
if [ -d adios-1.13.1 ]
then
	rm -rf adios-1.13.1
fi
tar -zxf adios-1.13.1.tar.gz

export LIBS=-pthread

cd adios-1.13.1
echo
echo "Build ADIOS ..."
set -x
./configure --prefix=$ROOT/adios \
	--with-flexpath=$ROOT/korvo \
	CFLAGS="-g -O2 -fPIC" CXXFLAGS="-g -O2 -fPIC" FCFLAGS="-g -O2 -fPIC"
make -j 8
make install
set +x

cd ..

source ./env_adios.sh
# export ADIOS_HOME=$ROOT/adios
# export PATH=$ADIOS_HOME/bin:$PATH
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ADIOS_HOME/lib

echo
echo "ADIOS is done!"
echo
