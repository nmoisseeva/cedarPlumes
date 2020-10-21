#!/bin/bash
#SBATCH -t 23:59:00
#SBATCH --mem-per-cpu=1000M
#SBATCH -n 1
#SBATCH --account=def-rstull
#SBATCH --job-name=rclone
#SBATCH --output=rclone.out


#/home/moisseev/apps/bin/rclone copy -v /home/moisseev/projects/rrg-rstull/moisseev/plume/aug2019/complete/wrfout* gcloudteam:main/aug2019/complete
/home/moisseev/apps/bin/rclone copy -v -L /home/moisseev/projects/rrg-rstull/moisseev/plume/synthetic_plume_data gcloudteam:synthetic_plume_data
