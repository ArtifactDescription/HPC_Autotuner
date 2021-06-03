#!/bin/bash -l

# This loads all modules for all builds for consistency

echo Loading modules...

module unload intel-mkl/2017.3.196-v7uuj6z
module load intel/17.0.4-74uvhji
module load intel-mpi/2017.3-dfphq6k
module load libpng/1.6.34-nhq7uj3
module load cmake/3.12.2-4zllpyo
module load jdk/8u141-b15-mopj6qr
module load tcl/8.6.6-x4wnbsg
module load bzip2/1.0.8-5ba64je
module load zlib/1.2.11-6632jqd
module load anaconda3/5.2.0

echo Modules are loaded

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/psm2-compat:/usr/lib64

