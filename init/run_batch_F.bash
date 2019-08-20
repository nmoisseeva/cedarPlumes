#!/bin/bash
#=======input==========
#Floop=(4 6 7 9 10 12)
Floop=(12 8)
S=S400
R=R0
W=W4
spinup=true
#======end of input====

current=$(pwd)
echo "Running fuel set for $S,$W,$R:"
for i in "${Floop[@]}"
do
	echo "--FUEL RUN: $i category"
	#link main executables
	if $spinup; then
	        run=$W${S}F$i${R}spinup
	        echo ".....creating a run folder $run"
	        mkdir -p ../runs/$run
	        cd ../runs/$run
	        if [ "$(ls -A)" ]; then
	                rm *
	        fi

		#link landuse and sounding
		ln -s ../../init/landuse/LANDUSE.TBL_F$i$R LANDUSE.TBL
		ln -s ../../init/sounding/input_sounding$W$R input_sounding
		#link namelists
	        ln -s ../../init/namelist/namelist.input${S}F${i}spinup namelist.input
                #link ideal
		ln -s /home/moisseev/scratch/rxcadre/wrf-fire/WRFV3/main/ideal.exe ./
	
	        #create slurm script and run
	        SLURMFILE="$run.sh"
	        /bin/cat <<EOF >$SLURMFILE
#!/bin/bash
#SBATCH -t 10:00:00
#SBATCH --mem=10000M
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=15
#SBATCH --account=rrg-rstull

module load wrf-fire
module load jasper

mpirun -np 1 ./ideal.exe
srun ./wrf.exe
mv wrfout_* ../../complete/spinup/wrfout_$run
mv wrfrst_d01_0000-08-01_12:30:00 ../../restart/wrfrst_d01_0000-08-01_12:30:00_$W${S}F$i$R
EOF

        else
	
              	run=$W${S}F$i${R}
	        echo ".....creating a run folder $run"
		mkdir -p ../runs/$run
		cd ../runs/$run
		if [ "$(ls -A)" ]; then
			rm *
		fi

		#link restart file
	        ln -s ../../restart/wrfrst_d01_0000-08-01_12:30:00_$W${S}F$i$R wrfrst_d01_0000-08-01_12:30:00
	        #link namelists
	        ln -s ../../init/namelist/namelist.input${S}F$i namelist.input

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
	fi

	#link common files	
	ln -s /home/moisseev/scratch/rxcadre/wrf-fire/WRFV3/main/wrf.exe ./
	ln -s ../../init/namelist/namelist.fire namelist.fire
	
	#ln -s ../../init/slurm/$run.sh .
	echo ".....submitting job to slurm"
	sbatch $run.sh
	cd $current
done
echo "COMPLETE"
