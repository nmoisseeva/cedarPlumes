#!/bin/bash

#for Case in $( ls -p ../complete/. | grep -v / )
for Case in $( ls ../complete/*W5F7R7T* )
do
	tag=${Case:19}
	echo $tag
	FILE="./slurm/interp_$tag.sh"

	/bin/cat <<EOF >$FILE
#!/bin/bash
#SBATCH -t 03:00:00
#SBATCH --mem-per-cpu=192000M
#SBATCH -n 1
#SBATCH --account=def-rstull
#SBATCH --job-name=$tag
#SBATCH --output=%x.out

module load python
module load scipy-stack
source /home/moisseev/.vezarr/bin/activate

#check if interpolated data exists, uncompress
current=$pwd
tardir=/home/moisseev/projects/rrg-rstull/moisseev/plume/aug2019/complete/interp/zarr/
testfile=$tardir${tag}.tar.gz

if test -f "$testfile"; then
	cd $tardir
	tar -xf ${tag}.tar.gz
	cd $current
fi

#run interpolation or slicing
python /home/moisseev/projects/rrg-rstull/moisseev/plume/aug2019/python/prep_plumes_zarr.py $tag

#clean up and compress
cd $tardir
if test -f "$testfile"; then
	#rm -r $tag
	echo Deleting $tag
fi

tar -czf ${tag}.tar.gz $tag
#rm -r $tag
echo Deleting $tag
cd $current
echo Completed $tag
EOF
	echo Submitting $tag for interpolation
	#sbatch ./slurm/interp_$tag.sh	

done

