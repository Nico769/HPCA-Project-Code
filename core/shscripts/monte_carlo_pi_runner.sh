#!/bin/bash
for TRIALS in 1000 10000 1000000; do
	for TEST in 1 2 3 4 5 6 7 8 9 10; do
		for NODES in 1 3 6; do
			mpiexec -f $HOME/cloud/machinefile -n $NODES python3 $HOME/cloud/core/algos/monte_carlo_pi.py $TRIALS >> $HOME/cloud/core/logparsers/logs/mpi.$NODES.$TRIALS.log
		done 
	done
done
