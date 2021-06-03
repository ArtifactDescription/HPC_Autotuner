# In-situ Workflow Autotuner
## 1. Install Softwares and Run In-situ Workflow Applications
### 1.1  Scenario for ADIOS1-coupled Applications
#### 1.1.1  Setup Environments whole in one
```
./build-all.sh
source env_all.sh
```
#### 1.1.2  Setup Environments step by step
```
export ROOT=$PWD/install
mkdir -pv $ROOT
```
##### (1) Load modules
```
module unload intel-mkl/2017.3.196-v7uuj6z
module load intel/17.0.4-74uvhji
module load intel-mpi/2017.3-dfphq6k
module load cmake/3.12.2-4zllpyo
module load jdk/8u141-b15-mopj6qr
module load tcl/8.6.6-x4wnbsg
```
##### (2) Download and install FlexPath
```
mkdir korvo_build
cd korvo_build
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
Set environmental variable.
```
export KORVO_HOME=$ROOT/korvo
export PATH=$KORVO_HOME/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$KORVO_HOME/lib
```
##### (3) Download and install ADIOS 1
##### (4) Compile and test the application Heat-transfer and Stage-write
##### (5) Download and install Swift/T
##### (6) Compile and test the application LAMMPS and Voro++
##### (7) Download and install Conda
##### (8) Reconfigure Swift/T with Python and Rebuild/reinstall Swift/T

