#!/bin/bash -l

echo
echo "Heat transfer and stage write start ..."
echo
echo

set -eu

echo "Download Example-Heat_Transfer ..."
if [ -d Example-Heat_Transfer ]
then
	rm -rf Example-Heat_Transfer
fi
git clone https://github.com/CODARcode/Example-Heat_Transfer.git

echo
echo "Build heat transfer ..."
cd Example-Heat_Transfer
sed -i 's/^CC=cc$/CC=mpicc #cc/' Makefile
sed -i 's/^FC=ftn$/FC=mpif90 #ftn/' Makefile
make

echo
echo "Build stage write ..."
cd stage_write
sed -i 's/^CC=cc$/CC=mpicc #cc/' Makefile
sed -i 's/^FC=ftn$/FC=mpif90 #ftn/' Makefile
make

cd ..
echo
echo "Testing heat transfer and stage write ..."
mpiexec -n 12 ./heat_transfer_adios2 heat 4 3 40 50 6 5 &
mpiexec -n 3 ./stage_write/stage_write heat.bp staged.bp FLEXPATH "" MPI ""

mkdir -pv experiment
cd experiment
rm -f heat_transfer.xml
ln -s ../heat_transfer.xml heat_transfer.xml
cd ..
cp -f ../sbatch-bebop-ht.sh sbatch-bebop-ht.sh

cd ..

echo
echo "Heat transfer and stage write are done!"
echo

