#!/bin/bash -l

echo
echo "KORVO starts ..."
echo

if (( ${#ROOT} == 0  ))
then
	echo "Set ROOT as the parent installation directory!!"
	exit 1
fi

if [ -d $ROOT ]
then
	mkdir -pv $ROOT/korvo
else
	echo "There does not exist $ROOT!"
	exit 1
fi

# echo "Loading modules ..."
# module unload intel-mkl/2017.3.196-v7uuj6z
# module load intel/17.0.4-74uvhji
# module load intel-mpi/2017.3-dfphq6k
# module load gcc/7.1.0
# module load libpsm2/10.3-17
# module load cmake/3.12.2-4zllpyo
# echo "Modules are loaded!"

set -eu

echo
echo "Download korvo ..."
if [ -d korvo_build ]
then
	rm -rf korvo_build/*
else
	mkdir -pv korvo_build
fi

cd korvo_build
if wget –q https://gtkorvo.github.io/korvo_bootstrap.pl
then
	echo WARNING: wget exited with: $?
fi

# Setup korvo
# See 'perl ./korvo_bootstrap.pl -h'
perl ./korvo_bootstrap.pl stable $ROOT/korvo
# Installed fresh ./korvo_build.pl
# Installed fresh ./korvo_tag_db
# Installed fresh ./korvo_arch
# Installed fresh ./build_config
# Specify version tag to use [stable] :
# Specify install directory [\$HOME] : [Set install directory]
# Configuring system for release "stable", install directory "[install directory]"

# Edit korvo_build_config
# First, generate static libraries below (used by ADIOS)
# Line 52: korvogithub configure --disable-shared
# Line 53: korvogithub cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_FLAGS=-fPIC -DCMAKE_CXX_FLAGS=-fPIC -DTARGET_CNL=1 -DPKG_CONFIG_EXECUTABLE=IGNORE
# Then, generate dynamic libraries below (used by LAMMPS)
# Line 52: korvogithub configure
# Line 53: korvogithub cmake

echo
echo "Build the static libraries of korvo ..."
sed -i 's/^korvogithub configure$/korvogithub configure --disable-shared/' korvo_build_config
sed -i 's/^korvogithub cmake$/korvogithub cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_FLAGS=-fPIC -DCMAKE_CXX_FLAGS=-fPIC -DTARGET_CNL=1 -DPKG_CONFIG_EXECUTABLE=IGNORE/' korvo_build_config
nice perl ./korvo_build.pl

echo
echo "Build the dynamic libraries of korvo ..."
rm -rf build_area build_results
sed -i 's/^korvogithub configure --disable-shared$/korvogithub configure/' korvo_build_config
sed -i 's/^korvogithub cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_FLAGS=-fPIC -DCMAKE_CXX_FLAGS=-fPIC -DTARGET_CNL=1 -DPKG_CONFIG_EXECUTABLE=IGNORE$/korvogithub cmake/' korvo_build_config
nice perl ./korvo_build.pl

cd ..

source ./env_korvo.sh
# export KORVO_HOME=$ROOT/korvo
# export PATH=$KORVO_HOME/bin:$PATH
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$KORVO_HOME/lib

echo
echo "KORVO is done!"
echo

