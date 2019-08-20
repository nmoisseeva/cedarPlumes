#!/bin/bash
#SBATCH -t 0-02:00
#SBATCH --mem-per-cpu=20000M
#SBATCH -n 1
#SBATCH --account=rrg-rstull

module load gcc/7.3.0 python/3.6
source /home/moisseev/.vewrf/bin/activate

python /home/moisseev/projects/rrg-rstull/moisseev/plume/mar18/python/prep_plumes.py txt
echo Completed txt
