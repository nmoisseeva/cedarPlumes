#!/bin/bash
#=======input==========
F=F8
Sloop=(n200 200 500)
R=R0
W=W4
spinup=false
#======end of input====

current=$(pwd)
echo "Running surface heat set for $F,$W,$R:"
for i in "${Sloop[@]}"
do
	echo "--SURFACE FLUX RUN: $i W/M2"
	
	#link main executables
	run=${W}S${i}$F$R
	echo ".....creating a run folder $run"
	mkdir -p ../runs/$run
	cd ../runs/$run
	if [ "$(ls -A)" ]; then
		rm *
	fi

	#link restart file
	ln -s ../../restart/wrfrst_d01_0000-08-01_12:30:00_${W}S400$F$R wrfrst_d01_0000-08-01_12:30:00
	#link namelists
	ln -s ../../init/namelist/namelist.inputS${i}$F namelist.input
	
	#create slurm script and run
	SLURMFILE="$run.sh"
	/bin/cat <<EOF >$SLURMFILE
#!/bin/bash
#SBATCH -t 07:00:00
#SBATCH --mem=10000M
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=15
#SBATCH --account=rrg-rstull

module load wrf-fire
module load jasper

srun ./wrf.exe
mv wrfout_* ../../complete/wrfout_$run
EOF

	#link common files	
	ln -s /home/moisseev/scratch/rxcadre/wrf-fire/WRFV3/main/wrf.exe ./
	ln -s ../../init/namelist/namelist.fire namelist.fire
	
	#ln -s ../../init/slurm/$run.sh .
	echo ".....submitting job to slurm"
	sbatch $run.sh
	cd $current
done
echo "COMPLETE"
