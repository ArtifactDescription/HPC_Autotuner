#!/bin/bash -l

set -a
export ROOT=$PWD/install
mkdir -pv $ROOT

BUILD_LOG=build-$( date "+%Y-%m-%d-%H:%M_%p" ).log

{
echo ROOT=$ROOT
echo
source modules.sh
source build-korvo.sh
source build-adios.sh
source build-ht_sw.sh
source build-swiftT.sh
source build-lammps.sh
source build-swiftT_Py.sh
} 2>& 1 | tee $BUILD_LOG

