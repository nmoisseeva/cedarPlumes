#!/bin/bash
#SBATCH -t 23:59:00
#SBATCH --mem-per-cpu=1000M
#SBATCH -n 1
#SBATCH --account=def-rstull
#SBATCH --job-name=rclone
#SBATCH --output=rclone.out


/home/moisseev/apps/bin/rclone copy -v /home/moisseev/projects/rrg-rstull/moisseev/plume/aug2019 gcloudteam:main/aug2019
