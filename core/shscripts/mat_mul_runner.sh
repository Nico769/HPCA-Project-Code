#!/bin/bash
logs_dir=$HOME/cloud/core/logparsers/logs
[ -d $logs_dir ] && echo "logs directory already exists at $logs_dir" || mkdir -p $logs_dir
for MATDIM in 512 1024 2048; do
        for TEST in 1 2 3 4; do
            for NODES in 1 16 32; do
                echo "Running test number $TEST with $NODES nodes and $MATDIM x $MATDIM matricies..."
                mpiexec -f $HOME/cloud/machinefile -n $NODES python3 $HOME/cloud/core/algos/matmul.py $MATDIM >> $HOME/cloud/core/logparsers/logs/mpi.$NODES.$MATDIM.log
			done
		done
	done
done
echo "Done. Check the logs directory at $logs_dir"