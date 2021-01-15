#!/bin/bash
#SBATCH -t 30:00:00
#SBATCH --mem-per-cpu=3000M
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --account=def-rstull

module load  nixpkgs/16.09  intel/2016.4  openmpi/2.1.1
module load wrf-fire-1tracer

mpirun -np 1 ideal.exe
srun wrf.exe
