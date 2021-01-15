#!/bin/bash
#SBATCH -t 10:00:00
#SBATCH --mem-per-cpu=3000M
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --account=def-rstull

module load  nixpkgs/16.09  intel/2016.4  openmpi/2.1.1
module load wrf-fire-1tracer

srun wrf.exe
