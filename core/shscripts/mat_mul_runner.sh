#!/bin/bash
for MATDIM in 256 512 1024; do
        for TEST in 1 2 3 4; do
            for NODES in 1 2 4 8; do
                mpiexec -f $HOME/cloud/machinefile -n $NODES python3 $HOME/cloud/core/algos/matmul.py $MATDIM >> $HOME/cloud/core/logparsers/logs/mpi.$NODES.$MATDIM.log
			done
		done
	done
done
