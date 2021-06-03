#!/bin/bash
#SBATCH -J lammps_voro
#SBATCH -p bdwall
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -o /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/experiment/output.txt
#SBATCH -e /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/experiment/error.txt
#SBATCH -t 00:01:00
#SBATCH --workdir=/blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/experiment

export I_MPI_FABRICS=shm:tmi

/usr/bin/time -v -o time_lmp_mpi.txt timeout 600 mpiexec -n 32 -ppn 8 -hosts bdw-0150,bdw-0151,bdw-0157,bdw-0158 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/lmp_mpi -i in.quench > output_lmp_mpi.txt 2>&1
# /usr/bin/time -v -o time_voro_adios_omp_staging.txt timeout 600 mpiexec -n 24 -ppn 1 -hosts bdw-0098,bdw-0099 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/voro_adios_omp_staging dump.bp adios_atom_voro.bp FLEXPATH > output_voro_adios_omp_staging.txt 2>&1

# /usr/bin/time -v -o time_lmp_mpi.txt mpiexec -n 38 -ppn 1 -hosts bdw-0098 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/lmp_mpi -i in.quench.short > output_lmp_mpi.txt 2>&1 &
# /usr/bin/time -v -o time_voro_adios_omp_staging.txt mpiexec -n 37 -ppn 1 -hosts bdw-0099 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/voro_adios_omp_staging dump.bp adios_atom_voro.bp FLEXPATH > output_voro_adios_omp_staging.txt 2>&1

# /usr/bin/time -v -o time_lmp_mpi.txt mpiexec -n 8 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/lmp_mpi -i in.quench.short > output_lmp_mpi.txt 2>&1 &
# /usr/bin/time -v -o time_voro_adios_omp_staging.txt mpiexec -n 4 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/voro_adios_omp_staging dump.bp adios_atom_voro.bp FLEXPATH > output_voro_adios_omp_staging.txt 2>&1

#srun -n 8 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/lmp_mpi -i in.quench.short &
#srun -n 4 /blues/gpfs/home/tshu/project/bebop/MPI_in_MPI/bebop-psm2/Example-LAMMPS/swift-all/voro_adios_omp_staging dump.bp adios_atom_voro.bp FLEXPATH

