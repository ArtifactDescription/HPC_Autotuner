# In-situ Workflow Autotuner
## Install Softwares and Run In-situ Workflow Applications
### Scenario 1: ADIOS1-coupled Applications
#### Setup Environments whole in one
```
./build-all.sh
source env_all.sh
```
#### Setup Environments step by step
```
export ROOT=$PWD/install
mkdir -pv $ROOT
```
#### Load modules
```
module unload intel-mkl/2017.3.196-v7uuj6z
module load intel/17.0.4-74uvhji
module load intel-mpi/2017.3-dfphq6k
module load cmake/3.12.2-4zllpyo
module load jdk/8u141-b15-mopj6qr
module load tcl/8.6.6-x4wnbsg
```
#### Download and install FlexPath
```
wget https://gtkorvo.github.io/korvo_bootstrap.pl
perl ./korvo_bootstrap.pl stable $ROOT/korvo
```
Edit korvo_build_config
```
korvogithub configure --disable-shared
korvogithub cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_FLAGS=-fPIC -DCMAKE_CXX_FLAGS=-fPIC -DTARGET_CNL=1 -DPKG_CONFIG_EXECUTABLE=IGNORE
```
Then, build the static libraries of korvo (used by ADIOS)
```
perl ./korvo_build.pl
```
Edit korvo_build_config
```
korvogithub configure
korvogithub cmake
```
Then, build the dynamic libraries of korvo (used by LAMMPS)
```
perl ./korvo_build.pl
```
#### Download and install 

