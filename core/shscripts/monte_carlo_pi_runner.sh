#!/bin/bash
logs_dir=$HOME/cloud/core/logparsers/logs
[ -d $logs_dir ] && echo "logs directory already exists at $logs_dir" || mkdir -p $logs_dir
for TRIALS in 1000000 100000000; do
	scientific_trials=$(printf "%.e\n" ${TRIALS})
	for TEST in 1 2 3 4; do
		for NODES in 1 16 32; do
			mpiexec -f $HOME/cloud/machinefile -n $NODES python3 $HOME/cloud/core/algos/monte_carlo_pi.py $TRIALS >> $HOME/cloud/core/logparsers/logs/mpi.$NODES.$scientific_trials.log
		done 
	done
done
echo "Done. Check the logs directory at $logs_dir"