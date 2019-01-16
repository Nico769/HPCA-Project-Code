#!/bin/bash
for ROWS in 256 512 1024; do
    for COLUMNS in 256 512 1024; do
        for TEST in 1 2 3 4; do
            for NODES in 1 2 4 8; do
                mpiexec -f $HOME/cloud/machinefile -n $NODES python3 $HOME/cloud/core/algos/matmul.py $ROWS $COLUMNS $COLUMNS $ROWS >> mpi.$NODES.$ROWS.$COLUMNS.log
			done
		done
	done
done
