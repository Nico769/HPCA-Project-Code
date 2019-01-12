"""Estimate pi using a parallel Monte Carlo simulation.

   Implements an MPI version of a parallel Monte Carlo simulation for estimating pi.
   MPI's default channel is used.

   Usage:
        python main.py [total_num_trials]
        
        Options:
               -total_num_trials    the total number of trials ( (x,y) points) for the simulation.
                                    By default it is set to 1 million since a (probabilistic) precision of 3 decimal digits
                                    requires 10^(2*3) trials (1 million trials).
                                    see https://stackoverflow.com/questions/18139934/can-a-monte-carlo-pi-calculation-be-used-for-a-world-record

"""

from mpi4py import MPI
import numpy as np
from sys import argv

def random_points_generator(trials_per_node=0):
    """Evaluate if a pair (x,y) drawn from an uniform distribution falls inside the unit circle.

    Given a random distribution between 0 and 1, it evaluates if a pair (x,y) of random points
    falls inside the unit circle. If that's the case, a counter is incremented.

    Args:
        trials_per_node (int): the number of trials/drawns for this node/process.

    Returns:
        int: a counter who keeps track of the overall number of points fallen inside the circle.
    
    """
    points_fallen_inside_circle = 0
    # draw a pair (x,y) from an uniform distribution
    # between 0 and 1 for each trial
    # NOTE: each child process has its own seed
    # since np.random.seed() hasn't been invoked
    # This is good for randomness but terrible for
    # reproducibility (which we don't consider in this project)
    for _ in range(trials_per_node):
        x = np.random.uniform(0,1)
        y = np.random.uniform(0,1)
        # if (x,y) falls inside the unit circle
        # increment the counter by 1
        if (x*x+y*y) <= 1.0:
            points_fallen_inside_circle += 1

    return points_fallen_inside_circle

if __name__ == "__main__":
    # Check if the number of trials has been supplied via
    # the CLI. If not, use 1 million as default value.
    total_num_trials = int(argv[1]) if len(argv) > 1 else 1e6
    # MPI_Init() is automatically invoked
    # when MPI module is imported
    # Rename default channel for convenience
    comm = MPI.COMM_WORLD
    # Get the number of nodes on comm channel
    num_nodes = comm.Get_size()
    # Get their rank
    rank = comm.Get_rank()
    # Print a start checkpoint if I am the master node
    if rank == 0:
        print("Start", flush=True)
    # Compute number of trials per node
    trials_per_node = np.ceil(total_num_trials / num_nodes).astype(int)
    # Sync all nodes here to start a 'more accurate' time measurement
    comm.Barrier()
    # Init send (i.e. elapsed_buff) and receive (i.e. longest_elapsed_buff) buffer for MAX reduction
    # as a one dimensional zero-filled arrays
    elapsed_buff         = np.zeros(1,dtype=np.float64)
    # longest_elapsed_buff = np.zeros(1,dtype=np.float64)
    # Get start time
    start = MPI.Wtime()
    # Compute (x,y) random points which fall inside the circle
    points_in_circle_per_node = random_points_generator(trials_per_node)
    # Record the time when the function is done
    finish = MPI.Wtime()
    # Compute the time delta
    elapsed_buff[0] = (finish - start)
    # Each processor prints its wall-clock time
    print("Processor {0} finished in {1:.6f}s.".format(rank,elapsed_buff[0]), flush=True)
    # Do a MAX reduction to record the slowest processor
    # comm.Reduce([elapsed_buff, MPI.DOUBLE],[longest_elapsed_buff, MPI.DOUBLE],op=MPI.MAX,root=0)
    # Get rid of the array, just need a number
    # longest_elapsed = longest_elapsed_buff[0]
    # Init send (i.e. points_in_buff) and receive (i.e. tot_points_in_buff) buffer
    # for SUM reduction
    points_in_buff     = np.zeros(1,dtype=np.int32)
    tot_points_in_buff = np.zeros(1,dtype=np.int32)
    # Store points_in_circle_per_node in the buffer
    points_in_buff[0] = points_in_circle_per_node
    # Do a SUM reduction to retrieve the total number of points fallen
    # inside the circle
    comm.Reduce([points_in_buff, MPI.INT],[tot_points_in_buff, MPI.INT],op=MPI.SUM,root=0)
    # Get rid of the array, just need a number
    tot_points_in = tot_points_in_buff[0]
    # Master node estimates pi
    if rank == 0:
        # estimate pi according to 4*(total points in the circle) / overall trials)
        estimated_pi = 4*(tot_points_in / total_num_trials)
        # compute the error
        error_pi = np.abs(np.pi - estimated_pi)
        print("End", flush=True)
        # print("DEBUG: slowest processor wall-clock time: {:.6f}".format(longest_elapsed))
        # print("DEBUG: tot_points_in_buff: ", tot_points_in)
        # print("DEBUG: Pi is approximately: {:.6f}".format(estimated_pi))
        # print("DEBUG: Error is: {:.6f}".format(error_pi))

    # No need to MPI_Finalize() since mpi4py
    # implements an exit hook who does the job for us
