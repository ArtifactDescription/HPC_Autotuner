#!/bin/bash
#SBATCH -J heat_transfer
#SBATCH -p bdwall
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -o /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-Heat_Transfer/experiment/output.txt
#SBATCH -e /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-Heat_Transfer/experiment/error.txt
#SBATCH -t 00:01:00
#SBATCH --workdir=/blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-Heat_Transfer/experiment

export I_MPI_FABRICS=shm:tmi

/usr/bin/time -v -o time_heat_transfer_adios2.txt mpiexec -n 42 -ppn 1 -hosts bdw-0171,bdw-0172 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-Heat_Transfer/heat_transfer_adios2 heat 7 6 40 50 6 5 > output_heat_transfer_adios2.txt 2>&1 &
/usr/bin/time -v -o time_stage_write.txt mpiexec -n 30 -ppn 1 -hosts bdw-0171,bdw-0172 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-Heat_Transfer/stage_write/stage_write heat.bp staged.bp FLEXPATH "" MPI "" > output_stage_write.txt 2>&1

# /usr/bin/time -v -o time_heat_transfer_adios2.txt mpiexec -n 42 -ppn 1 -hosts bdw-0171 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-Heat_Transfer/heat_transfer_adios2 heat 7 6 40 50 6 5 > output_heat_transfer_adios2.txt 2>&1 &
# /usr/bin/time -v -o time_stage_write.txt mpiexec -n 37 -ppn 1 -hosts bdw-0172 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-Heat_Transfer/stage_write/stage_write heat.bp staged.bp FLEXPATH "" MPI "" > output_stage_write.txt 2>&1

# srun -n 12 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-Heat_Transfer/heat_transfer_adios2 heat 4 3 40 50 6 5  &
# srun -n 3 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-Heat_Transfer/stage_write/stage_write heat.bp staged.bp FLEXPATH "" MPI ""

