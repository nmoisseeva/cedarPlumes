#!/bin/bash
#=======input==========
InputFile=input_sounding
BaseVal=5.00
LoopVar=(3 4 6 7 8 9 10 11 12)
W=W5
R=R7T
#======end of input====

current=$(pwd)
echo "Creating input_sounding set for $R:"
cd ./sounding/
for i in "${LoopVar[@]}"
do
	echo "--WIND INPUT: $i m/s "

	#move to folder
	run=${InputFile}W$i$R
	cp $InputFile$W$R $run
	sed -i "s/ $BaseVal / ${i}.00 /g" $run
done
cd $current
echo "COMPLETE"
