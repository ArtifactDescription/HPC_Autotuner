# Experimental Environment for ADIOS1-coupled Applications
Environment setting in the cluster Bebop at LCRC in ANL is as follows. Either of quick start and manual setup can be used.

## 1.  Quick Start
```
./build.sh
source env.sh
```

## 2.  Manually Setup Environments
```
export ROOT=$PWD/install
mkdir -pv $ROOT
```

#### (1) Load modules
```
module unload intel-mkl/2017.3.196-v7uuj6z
module load intel/17.0.4-74uvhji
module load intel-mpi/2017.3-dfphq6k
module load cmake/3.12.2-4zllpyo
module load jdk/8u141-b15-mopj6qr
module load tcl/8.6.6-x4wnbsg
```

#### (2) Download and install FlexPath
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

#### (3) Download ADIOS 1 from https://users.nccs.gov/~pnorbert/adios-1.13.1.tar.gz and install ADIOS 1
```
tar -zxvf adios-1.13.1.tar.gz
export LIBS=-pthread
cd adios-1.13.1
./configure --prefix=$ROOT/adios --with-flexpath=$ROOT/korvo CFLAGS="-g -O2 -fPIC" CXXFLAGS="-g -O2 -fPIC" FCFLAGS="-g -O2 -fPIC"
make -j 8
make install
export ADIOS_HOME=$ROOT/adios
export PATH=$ADIOS_HOME/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ADIOS_HOME/lib
```

#### (4) Download, compile, and test the applications Heat-transfer and Stage-write
Download coupled applications Heat-transfer and Stage-write:
```
git clone https://github.com/CODARcode/Example-Heat_Transfer.git
cd Example-Heat_Transfer
git checkout e2353b06d0ded82ff00402e072987b7c1ed506a9
```
Modify Example-Heat_Transfer/Makefile and Example-Heat_Transfer/stage_write/stage_write to use compilers mpicc and mpif90, and compile:
```
cd Example-Heat_Transfer
make
cd Example-Heat_Transfer/stage_write
make
cd Example-Heat_Transfer
```
Test Heat-transfer and Stage-write in separate terminal windows:
```
mpiexec -n 12 ./heat_transfer_adios2 heat 4 3 40 50 6 5
```
```
mpiexec -n 3 ./stage_write/stage_write heat.bp staged.bp FLEXPATH "" MPI ""
```
Copy/link the configuration file heat_transfer.xml:
```
mkdir -pv experiment
ln -s heat_transfer.xml experiment/heat_transfer.xml
```

#### (5) Download and install Swift/T
Download and Install Ant:
```
wget https://www.apache.org/dist/ant/binaries/apache-ant-1.10.10-bin.tar.gz
tar -zxvf apache-ant-1.10.10-bin.tar.gz -C $ROOT
export ANT_HOME=$ROOT/apache-ant-1.10.10
export PATH=$ANT_HOME/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ANT_HOME/lib
```
Download Swift/T:
```
git clone https://github.com/swift-lang/swift-t.git
cd swift-t
git checkout remotes/origin/tong01
git checkout de99add30a64622a65f603e304f22f57ed3e20d4
```
Generate the compiling script:
```
dev/build/init-settings.sh
```
Set the installation path SWIFT_T_PREFIX=$ROOT/swift-t-install in the file dev/build/swift-t-settings.sh and compile/install Swift/T:
```
dev/build/build-swift-t.sh
export SWIFT_T_HOME=$ROOT/swift-t-install
export PATH=$SWIFT_T_HOME/turbine/bin:$SWIFT_T_HOME/stc/bin:$PATH
```

#### (6) Compile and test the application LAMMPS and Voro++
Request accessing the source code https://github.com/CODARcode/Example-LAMMPS.git

Download:
```
git clone https://github.com/CODARcode/Example-LAMMPS.git
```
Compile LAMMPS:
```
cd Example-LAMMPS/lammps/src
make yes-kspace yes-manybody yes-molecule yes-user-adios_staging
make mpi -j8
make mpi -j8 mode=shlib
```
Compile Voro++-0.4.6:
```
cd Example-LAMMPS/voro++-0.4.6/src
make -j8 CXX=mpicxx CFLAGS=-fPIC
```
Compile adios_integration (timeout_sec in voro_adios_omp_staging.h can be set.):
```
cd Example-LAMMPS/adios_integration
make -j8
```
Edit swift-liblammps/build.sh to set MPICC as $( which mpicc ) and compile swift-liblammps
```
cd Example-LAMMPS/swift-liblammps
sed -i 's/^MPICC=$( which cc )$/MPICC=$( which mpicc )/' build.sh
./build.sh
```
Compile swift-all:
```
cd ../swift-all
./build-16k.sh
cd ..
export PATH=$PWD/lammps/src:$PWD/adios_integration:$PATH
cd swift-all
```
Test LAMMPS and Voro++ in separate terminal windows:
```
mpiexec -n 8 ./lmp_mpi -i in.quench.short
```
```
mpiexec -n 4 ./voro_adios_omp_staging dump.bp adios_atom_voro.bp FLEXPATH
```

#### (7) Download and install Conda 2 and Python 2
```
$ wget https://repo.anaconda.com/archive/Anaconda2-5.3.1-Linux-x86_64.sh
$ chmod +x Anaconda2-5.3.1-Linux-x86_64.sh
$ ./Anaconda2-5.3.1-Linux-x86_64.sh -p $ROOT/anaconda2
...
Do you wish the installer to initialize Anaconda2
in your /home/ac.tshu/.bashrc ? [yes|no]
[no] >>> 
You may wish to edit your /home/ac.tshu/.bashrc to setup Anaconda2:
source /lcrc/project/Workflow/SC21/HPC_Autotuner/adios1-coupled/install/anaconda2/etc/profile.d/conda.sh
Do you wish to proceed with the installation of Microsoft VSCode? [yes|no]
>>> no
$ export PATH=$ROOT/anaconda2/bin:$PATH
$ conda create -n codar python=2.7
$ export PATH=$ROOT/anaconda2/envs/codar/bin:$PATH
```

#### (8) Reconfigure Swift/T with Python and Rebuild/reinstall Swift/T
Set ENABLE_PYTHON as 1 and PYTHON_EXE as the python launcher's path in dev/build/build-swift-t.sh and rebuild Swift/T:
```
dev/build/build-swift-t.sh
```
