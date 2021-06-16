#!/bin/bash -l

set -a

echo Loading modules...
module unload intel-mkl/2017.3.196-v7uuj6z
module load intel/17.0.4-74uvhji
module load intel-mpi/2017.3-dfphq6k
module load cmake/3.12.2-4zllpyo
module load jdk/8u141-b15-mopj6qr
module load tcl/8.6.6-x4wnbsg
module load anaconda3/5.2.0
echo Modules OK

export ROOT=$PWD/install

source env_korvo.sh
source env_adios.sh
source env_ant.sh
source env_swiftT.sh

