#!/bin/bash

graphFiles=`ls ./data/ | grep .gr`

for graph in $graphFiles
do
	filename=`echo $graph | cut -d'.' -f1`
	echo $graph $filename
	
	#You can change the following line to use your code, then use this file to run all of your experiments. For example, you can execute the python code with:
	#python src/RunExperiments.py ./data/$graph ./data/$filename.extra ./results/$filename_output.txt

done
