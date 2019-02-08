"""Matrix multiplication

   Multiplies two square matrices A and B, storing the result in matrix C.

   Usage:
        python matmul.py [matrix_dimension]

        Options:
               -matrix_dimension    the dimension of the square matrices.
    
   The names of the matrices start with an uppercase.
	
"""
from mpi4py import MPI
import numpy as np
from time import time
from sys import argv

def matrixmul(A, B, tile_width, mat_dim):
    offset=tile_width*(comm.Get_rank())
    for i in range(tile_width):
        for j in range(mat_dim):
            for k in range(mat_dim):
                Partial[i+offset][j] += A[i+offset][k] * B[k][j]
    return Partial

if __name__ == "__main__":
    # Check if the matrices dimension has been supplied via
    # the CLI. If not, use 128 as default value.
    mat_dim = int(argv[1]) if len(argv) > 1 else 128
    # Rename default channel for convenience
    comm = MPI.COMM_WORLD
    # Get the number of nodes on comm channel
    num_nodes = comm.Get_size()
    # Get their rank
    rank = comm.Get_rank()
    # Compute tile_width
    tile_width = np.round(mat_dim / num_nodes).astype(int)
    # Fill the partial matrix with zeros
    Partial = np.zeros((mat_dim,mat_dim))
    # Fill the result matrix of the parallel execution with zeros
    Result = np.zeros((mat_dim,mat_dim))
    # Declare an empty matrix, A
    A = np.empty((mat_dim,mat_dim))
    # Declare an empty matrix, B
    B = np.empty((mat_dim,mat_dim))

    if rank == 0:
        print("Start", flush=True)
        # Init the first matrix, A, with random values
        A = np.random.random((mat_dim,mat_dim))
        # Init the second matrix, B, with random values
        B = np.random.random((mat_dim,mat_dim))

    # Broadcast A and B to worker nodes
    comm.Bcast(A,root=0)
    comm.Bcast(B,root=0)
    # Record now as the starting time
    parallel_start = MPI.Wtime()
    # Launch the matrix multiplication kernel
    Partial = matrixmul(A,B,tile_width,mat_dim)
    # Merge the blocks of matrix frome the processes in a single matrix
    comm.Reduce([Partial, MPI.DOUBLE],[Result, MPI.DOUBLE],op=MPI.SUM,root=0)
    # Record now as the finishing time
    parallel_finish = MPI.Wtime()
    # Init send (i.e. elapsed_buff) and receive (i.e. longest_elapsed_buff) buffer for MAX reduction
    # as a one dimensional zero-filled arrays
    elapsed_buff         = np.zeros(1,dtype=np.float64)
    longest_elapsed_buff = np.zeros(1,dtype=np.float64)
    # Compute the time delta
    elapsed_buff[0] = (parallel_finish - parallel_start)
    # Do a MAX reduction to record the slowest processor
    comm.Reduce([elapsed_buff, MPI.DOUBLE],[longest_elapsed_buff, MPI.DOUBLE],op=MPI.MAX,root=0)
    # Get rid of the array, just need a number
    tot_parallel = longest_elapsed_buff[0]

    if rank == 0:
        # Fill the C matrix with zeros
        C = np.zeros((mat_dim,mat_dim))
        # Record now as the starting time for the serial matmul
        serial_start = time()
        for i in range(mat_dim):
            for j in range(mat_dim):
                for k in range(mat_dim):
                    C[i][j] += A[i][k] * B[k][j]
        # Record now as the finishing time for the serial matmul
        serial_finish = time()

        # Compare the C matrix (serial) with the Result matrix (parallel execution) 
        P = np.subtract(C,Result)
                
        if np.sum(P) != 0:
            print("Serial and parallel executions provide different results, exiting..")
            exit()
        else:
            tot_serial = serial_finish - serial_start
            print("Total wall-clock time elapsed for serial execution {:.6f}".format(tot_serial), flush=True)
            # Even though the parallel execution time has been calculated
            # don't show it if there is only one processor/node
            if comm.Get_size() > 1:
                print("Total wall-clock time elapsed for parallel execution {:.6f}".format(tot_parallel), flush=True)
            print("End", flush=True)