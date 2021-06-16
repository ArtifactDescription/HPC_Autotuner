
# This loads all modules for all builds for consistency

# Load modules gcc/7.1.0, libpsm2/10.3-17, and cmake/3.12.2-4zllpyo
# module spider cmake/3.12.2-4zllpyo
echo
echo Loading modules...
echo

module unload intel-mkl/2017.3.196-v7uuj6z
module load intel/17.0.4-74uvhji
module load intel-mpi/2017.3-dfphq6k
module load cmake/3.12.2-4zllpyo
module load jdk/8u141-b15-mopj6qr
module load tcl/8.6.6-x4wnbsg
module load anaconda3/5.2.0

echo
echo Modules OK
echo

