# Experimental environment for ADIOS2-coupled Applications
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
module load libpng/1.6.34-nhq7uj3
module load cmake/3.12.2-4zllpyo
module load jdk/8u141-b15-mopj6qr
module load tcl/8.6.6-x4wnbsg
module load bzip2/1.0.8-5ba64je
module load zlib/1.2.11-6632jqd
module load anaconda3/5.2.0
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/psm2-compat:/usr/lib64
```

#### (2) Download and install ADIOS 2
```
git clone https://github.com/ornladios/ADIOS2.git
cd ADIOS2
git checkout 78b5956c26aac8939f5cb3c6bd9f992e7361fc03
mkdir adios2-build
cd adios2-build
cmake -DCMAKE_INSTALL_PREFIX=$ROOT/adios2 -DADIOS2_USE_Fortran=OFF ..
make -j 8
make install
export ADIOS2_HOME=$ROOT/adios2
export PATH=$ADIOS2_HOME/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ADIOS2_HOME/lib64
export PYTHONPATH=$ADIOS2_HOME/lib64/python3.6/site-packages
```

#### (3) Download, compile, and test the applications Gray-Scott, PDF calculate, Gray plot, and PDF plot
Download coupled applications Gray-Scott, PDF calculator, Gray plot, and PDF plot:
```
git clone https://github.com/pnorbert/adiosvm.git
cd adiosvm
git checkout 547306a935d45204ec509e0af06540aac05d3045
cd ..
cp -r adiosvm/Tutorial/gray-scott gray-scott
patch gray-scott/simulation/gray-scott.cpp patch_gray-scott_Oct2019.txt
patch gray-scott/simulation/writer.cpp patch_writer_Oct2019.txt
```
Compile Gray-scott and PDF calculator:
```
cd gray-scott
mkdir build
cd build
export ADIOS2_DIR=$ROOT/adios2
cmake -DCMAKE_PREFIX_PATH=$ROOT/adios2 -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
make -j 8
```
In plot/gsplot.py and plot/pdfplot.py, add two lines:
```
import matplotlib
matplotlib.use("Agg")
```
before
```
import matplotlib.pyplot as plt
```
Configure Gray-scott and PDF calculator in the post-hoc mode:
Comment operation for SZ and set engine type as "BP4" in adios2.xml. 
Also, set step as 100 and adios_span as false in simulation/settings-files.json.

Run Gray-scott and PDF calculator in the post-hoc mode:
```
mkdir -pv BPgsplot
mkdir -pv BPpdfplot
mpiexec -n 2 build/gray-scott simulation/settings-files.json
bpls -l gs.bp
mpiexec -n 1 python3 plot/gsplot.py -i gs.bp -o BPgsplot/img
mpiexec -n 2 build/pdf_calc gs.bp pdf.bp 100
bpls -l pdf.bp
mpiexec -n 2 python3 plot/pdfplot.py -i pdf.bp -o BPpdfplot/fig
```
Configure Gray-scott and PDF calculator in the in-situ mode:
Set engine type as "SST", "RendezvousReaderCount" as 2, "QueueLimit" as 0, and "QueueFullPolicy" as "Block" in adios2.xml.
Also, set step as 100 and adios_span as false in simulation/settings-staging.json.

Run Gray-scott and PDF calculator in the in-situ mode:
```
mkdir -pv SSTgsplot
mkdir -pv SSTpdfplot
mpiexec -n 2 build/gray-scott simulation/settings-staging.json &
mpiexec -n 1 build/pdf_calc gs.bp pdf.bp 100 &
mpiexec -n 1 python3 plot/pdfplot.py -i pdf.bp -o SSTpdfplot/fig &
mpiexec -n 1 python3 plot/gsplot.py -i gs.bp -o SSTgsplot/img
```

#### (4) Download and install Swift/T
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
Set the installation path SWIFT_T_PREFIX=$ROOT/swift-t-install in dev/build/swift-t-settings.sh and 
set ENABLE_PYTHON as 1 and PYTHON_EXE as the python launcher's path in dev/build/swift-t-settings.sh.
Compile and install Swift/T:
```
dev/build/build-swift-t.sh
export SWIFT_T_HOME=$ROOT/swift-t-install
export PATH=$SWIFT_T_HOME/turbine/bin:$SWIFT_T_HOME/stc/bin:$PATH
```
