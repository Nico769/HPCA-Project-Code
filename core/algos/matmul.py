
""" execute with anaconda prompt from the directory of matrixmul.py
    
    mpi4py and Microsoft MPI must be installed:
        https://www.microsoft.com/en-us/download/details.aspx?id=57467
    
    EVERY TIME I EXECUTE THE CODE, AN ERROR APPEARS, BUT IT DOESN'T INTERFERE
    WITH THE RESULT OF THE COMPUTATION. I HAVEN'T FOUND A SOLUTION YET

    with the code:    mpiexec -n NUMERO DI NODI python -m matrixmul.py NUMERO DI RIGHE (O COLONNE, MATRICE QUADRATA)
"""
from mpi4py import MPI
import numpy as np
from sys import argv

def matrixmul(A, B, Partial, Rank, Tile_width, Row_dim, Col_dim):
    #count=0  #to get the percentage of completition of the operation
    offset=Tile_width*(Rank)
    for i in range(Tile_width):
        for j in range(Row_dim):
            for k in range(Col_dim):
                Partial[i+offset][j] += A[i+offset][k] * B[k][j] 
                
        #count+=1
        #print(count/(Mat_dim^2)*100,"%")

Row_dim = int(argv[1]) if len(argv) > 1 else 128
Col_dim = int(argv[2]) if len(argv) > 1 else 128
comm = MPI.COMM_WORLD
# Get the number of nodes on comm channel
num_nodes = comm.Get_size()
# Get their rank
Rank = comm.Get_rank()
# Compute tile_width
Tile_width = np.round(Row_dim / num_nodes).astype(int)
Partial=np.zeros((Row_dim,Row_dim))   #partial matrix initialization
Result=np.zeros((Row_dim,Row_dim))  #final matrix initialization

if(Rank==0):   
    A=np.zeros((Row_dim,Col_dim))   #first matrix initialization
    B=np.zeros((Col_dim,Row_dim))   #second matrix initialization    
    #C=np.zeros((Row_dim,Row_dim))   #check matrix initialization
    #P=np.zeros((Row_dim,Row_dim))   #check matrix initialization 2
    #generating matrix 1
    for i in range(Row_dim):
        for j in range(Col_dim):
            A[i][j]=np.random.rand()
    #generating matrix 2
    for i in range(Col_dim):
        for j in range(Row_dim):
            B[i][j]=np.random.rand()
    #generating product matrix
    #for i in range(Row_dim):
    #    for j in range(Row_dim):
    #        for k in range(Col_dim):
    #            C[i][j]+= A[i][k] * B[k][j] 
#uncomment the lines(45-48) to have a serial execution of the matrixmul 
    for i in range(1,num_nodes):
        comm.send(A,dest=i, tag=11)
        comm.send(B,dest=i, tag=12)
else:
    A=comm.recv(source=0, tag=11)
    B=comm.recv(source=0, tag=12)

comm.Barrier() #waiting for all the processes to have the same data
start = MPI.Wtime()
#execute matrix multiply
matrixmul(A,B,Partial,Rank, Tile_width, Row_dim, Col_dim)
comm.Barrier()
#merge the blocks of matrix frome the processes in a single matrix
comm.Reduce([Partial, MPI.DOUBLE],[Result, MPI.DOUBLE],op=MPI.SUM,root=0)
# Record the time when the function is done
finish = MPI.Wtime()
#check the result and/or print time elapsed
if (Rank==0):
#checking with product matrix C, needs lines(45-48)
    #for i in range(Row_dim):
    #    for j in range(Col_dim):
    #        for k in range(Row_dim):
    #            P[i][j]=C[i][j]-Result[i][j]
    #print(P)
    print("time elapsed:",finish - start,"s")