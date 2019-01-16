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

Once your MPI environment has been set up, make sure your cluster shared folder is named ```cloud``` and is located at your ```$HOME``` path.

```monte_carlo_pi_runner.sh``` runs the ```algos/monte_carlo_pi.py``` for ```TEST``` times and different values of ```TRIALS``` and ```NODES``` (see the script), logging the ```monte_carlo_pi.py``` output onto a text file with the following naming convention: ```mpi.NUMBER_OF_NODES.NUMBER_OF_TRIALS_IN_SCIENTIFIC_NOTATION.log```

```sh

~/cloud/core/shscripts$ chmod 700 monte_carlo_pi_runner.sh    # give execute permission
~/cloud/core/shscripts$ ./monte_carlo_pi_runner.sh            # run it

```

```all_logs_to_csv.sh``` invokes ```logparsers/parser.py``` for each log file stored in ```$HOME/cloud/core/logparsers/logs/``` (please **manually** create the ```logs``` folder) which will parse your log files and generate a ```LOG_FILE_NAME.csv``` csv file with the following format:

| Measurements | CPU 1   | CPU 2   | CPU 3  | CPU 4   |
|--------------|---------|---------|--------|---------|
| 1            | 10.4978 | 7.1888  | 8.9944 | 10.4160 |
| 2            | 10.5558 | 8.4481  | 7.0874 | 10.5088 |
| 3            | 10.5298 | 10.0980 | 6.5676 | 10.3889 |

```mat_mul_runner.sh``` runs the ```algos/matmul.py``` for ```TEST``` times and several matricies dimensions, as well as different values of ```NODES``` (see the script), logging the ```matmul.py``` output onto a text file with the following naming convention: ```mpi.NUMBER_OF_NODES.NUMBER_OF_ROWS.NUMBER_OF_COLUMNS.log```

## License

MIT - see [LICENSE](https://github.com/Nico769/HPCA-Project-Code/blob/master/LICENSE) © Francesco Casciola, Elia Giuseppe Ceroni, Nicola Landolfi