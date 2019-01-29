# Embarrassingly parallel algorithms with mpi4py

Matrix multiplication and Monte Carlo estimation of Pi using Python and [mpi4py](https://mpi4py.readthedocs.io/en/stable/).

This repository contains a simple implementation of these two popular parallel algorithms, a log file parser and a few orchestration shell scripts to run them. There is also a Dockerfile which can be used to quickly spin up a container on a single node for development purposes. The project is under active development as our final project for High Performance Computer Architecture course at 'Università degli Studi di Siena' under Professor Roberto Giorgi.

## Project structure

```

/$HOME/cloud
├── Dockerfile          # Docker image specs
├── requirements.txt    # Python scripts dependencies
├─┬ core                # Project main folder
│ ├── algos             # Algorithms folder
│ ├── logparsers        # Parser and logs folder
│ └── shscripts         # Shell scripts folder
└── your_machinefile    # Cluster machinefile

```

## Usage

Once your MPI environment has been set up, make sure the cluster shared folder is named ```cloud``` and is loca```$HOME``` path.

```monte_carlo_pi_runner.sh``` runs the ```algos/monte_carlo_pi.py``` for ```TEST``` times and different values of ```TRIALS``` and ```NODES``` (see the script), logging the ```monte_carlo_pi.py``` output onto a text file with the following naming convention: ```mpi.NUMBER_OF_NODES.NUMBER_OF_TRIALS_IN_SCIENTIFIC_NOTATION.log```

```sh

~/cloud/core/shscripts$ chmod 700 monte_carlo_pi_runner.sh    # give execute permission to the script
~/cloud/core/shscripts$ ./monte_carlo_pi_runner.sh            # run it

```

```mat_mul_runner.sh``` runs the ```algos/matmul.py``` for ```TEST``` times and several matricies dimensions, as well as different values of ```NODES``` (see the script), logging the ```matmul.py``` output onto a text file with the following naming convention: ```mpi.NUMBER_OF_NODES.SQUARE_MATRICIES_DIMENSION.log```

```all_logs_to_csv.sh``` invokes ```logparsers/parser.py``` for each log file stored in ```$HOME/cloud/core/logparsers/logs/``` (which is created when one of the previous scripts run for the first time) which will parse your log files and generate a ```LOG_FILE_NAME.csv``` csv file with the following format:

| Measurements | nodes_number | slowest_node_mc_pi | trials |
|--------------|--------------|--------------------|--------|
| 1            | 16           | 9.258786           | 1e+08  |
| 2            | 16           | 9.580477           | 1e+08  |
| 3            | 16           | 8.943837           | 1e+08  |
| 4            | 16           | 8.906039           | 1e+08  |

| Measurements | nodes_number | parallel_matmul | mat_dim |
|--------------|--------------|-----------------|---------|
| 1            | 4            | 51.801          | 512     |
| 2            | 4            | 51.8218         | 512     |
| 3            | 4            | 53.1612         | 512     |
| 4            | 4            | 53.7941         | 512     |

TODO: Add Excel files, graphs and reference section

## License

MIT - see [LICENSE](https://github.com/Nico769/HPCA-Project-Code/blob/master/LICENSE) © Francesco Casciola, Elia Giuseppe Ceroni, Nicola Landolfi