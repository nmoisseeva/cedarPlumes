#!/bin/bash
#=======input==========
F=F7
R=Rtest
Wloop=(5)
#Wloop=(12)
spinup=false
tall=true
#======end of input====

current=$(pwd)
echo "Running wind set for $F,$R:"
for i in "${Wloop[@]}"
do
	echo "--WIND RUN: $i m/s"
	#link main executables
	if $spinup; then
	        run=W$i$F${R}spinup
	        echo ".....creating a run folder $run"
	        mkdir -p ../runs/$run
	        cd ../runs/$run
	        if [ "$(ls -A)" ]; then
	                rm *
	        fi

		#link landuse, perturbed surface and sounding
		ln -s ../../init/landuse/LANDUSE.TBL_$F LANDUSE.TBL
		ln -s ../../init/sounding/input_soundingW$i$R input_sounding
		ln -s ../../init/surface/input_tsk$R input_tsk
		
		#link namelists
		if $tall; then
	        	ln -s ../../init/namelist/namelist.input${F}Tspinup namelist.input
		else
			ln -s ../../init/namelist/namelist.input${F}spinup namelist.input
		fi

		#create slurm script and run
		SLURMFILE="$run.sh"
		/bin/cat <<EOF >$SLURMFILE
#!/bin/bash
#SBATCH -t 23:00:00
#SBATCH --mem-per-cpu=3000M
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --account=def-rstull
#SBATCH --job-name=$run
#SBATCH --output=%x-%j.out

module load  nixpkgs/16.09  intel/2016.4  openmpi/2.1.1
module load wrf-fire-1tracer

mpirun -np 1 ideal.exe
srun wrf.exe
mv wrfout_* ../../complete/spinup/wrfout_$run
mv wrfrst_d01_0000-08-01_12:30:00 ../../restart/wrfrst_d01_0000-08-01_12:30:00_W$i$F$R
EOF
	else
	
              	run=W$i$F$R
	        echo ".....creating a run folder $run"
		mkdir -p ../runs/$run
		cd ../runs/$run
		if [ "$(ls -A)" ]; then
			rm *
		fi

		#link restart file
	        ln -s ../../restart/wrfrst_d01_0000-08-01_12:30:00_W${i}$F${R%*E} wrfrst_d01_0000-08-01_12:30:00
	        #link namelists
		if $tall; then
			ln -s ../../init/namelist/namelist.input${F}T namelist.input
		else
			ln -s ../../init/namelist/namelist.input$F namelist.input
		 fi

                #create slurm script and run
                SLURMFILE="$run.sh"
                /bin/cat <<EOF >$SLURMFILE
#!/bin/bash
#SBATCH -t 10:00:00
#SBATCH --mem-per-cpu=3000M
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --account=def-rstull
#SBATCH --job-name=$run
#SBATCH --output=%x-%j.out

module load  nixpkgs/16.09  intel/2016.4  openmpi/2.1.1
module load wrf-fire-1tracer

srun wrf.exe
mv wrfout_* ../../complete/wrfout_$run
EOF
	fi

	#link common files	
	ln -s ../../init/namelist/namelist.fire namelist.fire
	ln -s ../../init/namelist/namelist.fire_emissions ./

	#link slurm script and run
	echo ".....submitting job to slurm"
	sbatch $run.sh
	cd $current
done
echo "COMPLETE"
