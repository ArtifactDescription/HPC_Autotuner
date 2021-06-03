#!/bin/bash -l

# Build in a computing node, rather than a log-in node
# salloc -N 1 -t 60
# ssh bdw-xxxx

set -a
export ROOT=$PWD/install
mkdir -pv $ROOT

BUILD_LOG=build-$( date "+%Y-%m-%d-%H:%M_%p" ).log

{
echo ROOT=$ROOT
echo
source module.sh
source build-adios2.sh
source build-gs_pdf.sh
source build-swiftT.sh
} 2>& 1 | tee $BUILD_LOG

