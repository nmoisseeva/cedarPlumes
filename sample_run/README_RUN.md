Instructions for running WRF-SFIRE on Cedar
===========================================

nmoisseeva@eoas.ubc.ca
January 14, 2021

This is a quick summary of how to run WRF-SFIRE LES using the sample initalization files included in the subdirectories.

The included files are for a case study *W9F7R7T*. 
The methodology (and condition settings) are detailed in:
- Chapter 4 of https://open.library.ubc.ca/cIRcle/collections/ubctheses/24/items/1.0395299
- (brief journal summary)  https://doi.org/10.5194/acp-2020-827

#1. Ensure you have a working copy of WRF-SFIRE code on Cedar. 

#2. Run a spinup simulation:
	- cd to 'spinup_run'
	- ensure all initalization files are in place, including:
		-namelist.input - main configuration file (see WRF-SFIRE documentation for details)
		-input_sounding - sounding file, including temperature and wind profiles (see WRF documentation)
		-namelist.fire - fuel category settings (this model uses Anderson fuel categories)
		-namelist.fire_emissions - emission factors for each tracer (currently 1), for each fuel category
		-input_tsk - perturbed surface temperature field (used to kick-off convection, without adding "bubble" perturbation)
		-LANDUSE.TBL - surface initalization settings (roughness length etc) 
	-in submit_to_slurm_spinup.sh ensure wrf-sfire module name is consistent with your installation (currently called wrf-fire-1tracer)
	-submit to slurm (run 'sbatch submit_to_slurm_spinup.sh' in command line)

#3. Once the spinup simulation is complete, it should generate a wrf restart file (wrfrst*). Create a symbolic link to this file within the 'fire_run' subdirectory

#4. Run the main fire simulation:
	- cd to fire_run
	- ensure all initialization filres are in place, including:
		-namelist.input - main configuration file
		-namelist.fire
		-namelist.fire_emissions
	-in submit_to_slurm_fire.sh ensure wrf-sifre module name is consistent with your installation (currently called wrf-fire-1tracer) 
	-submit to slurm (run 'sbatch submit_to_slurm_fire.sh' in command line)


