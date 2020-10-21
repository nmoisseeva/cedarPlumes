#!/bin/bash
#SBATCH -t 10:00:00
#SBATCH --mem-per-cpu=192000M
#SBATCH -n 1
#SBATCH --account=def-rstull

module load python
module load scipy-stack
source /home/moisseev/.vewrf/bin/activate

python /home/moisseev/projects/rrg-rstull/moisseev/plume/aug2019/python/export_last_frame.py

