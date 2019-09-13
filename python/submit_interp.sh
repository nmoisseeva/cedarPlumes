#!/bin/bash

for Case in $( ls -p ../complete/. | grep -v / ) 
do
	tag=${Case:7}
	FILE="./slurm/interp_$tag.sh"

	/bin/cat <<EOF >$FILE
#!/bin/bash
#SBATCH -t 01:30:00
#SBATCH --mem-per-cpu=128000M
#SBATCH -n 1
#SBATCH --account=rrg-rstull

module load python
module load scipy-stack
source /home/moisseev/.vewrf/bin/activate

python /home/moisseev/projects/rrg-rstull/moisseev/plume/aug2019/python/prep_plumes.py $tag
echo Completed $tag
EOF
	echo Submitting $tag for interpolation
	sbatch ./slurm/interp_$tag.sh	

done

