#!/bin/bash
#SBATCH -t 30:00:00
#SBATCH --mem-per-cpu=4000M
#SBATCH --nodes=1
#SBATCH --ntasks=47
#SBATCH --account=def-rstull
#SBATCH --job-name=W9F7R6Tspinup
#SBATCH --output=%x-%j.out

module load  nixpkgs/16.09  intel/2016.4  openmpi/2.1.1
module load wrf-fire-1tracer

mpirun -np 1 ideal.exe
srun wrf.exe
mv wrfout_* ../../complete/spinup/wrfout_W9F7R6Tspinup
mv wrfrst_d01_0000-08-01_12:30:00 ../../restart/wrfrst_d01_0000-08-01_12:30:00_W9F7R6T
