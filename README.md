October 2020
nmoisseeva@eoas.ubc.ca


ComputeCanada cluster (Cedar) scripts
=====================================
Project directory for "synthetic plume" LES runs using a single tracer WRF-SFIRE installation on Cedar

# rclone.bash
-script submitting slurm request for copying files from cluster to GSuite

# /python
-contains scripts for interpolating, cross-sectioning and subsetting the data

# /init 
-contains scripts to generate WRF-SFIRE input files and to batch submit jobs to slurm 
-subfolders contain various WRF-SFIRE inputs for variety of fire and atmospheric conditions

