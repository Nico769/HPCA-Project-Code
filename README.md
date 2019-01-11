# Embarrassingly parallel algorithms with mpi4py

Matrix multiplication and Monte Carlo estimation of Pi using Python and [mpi4py](https://mpi4py.readthedocs.io/en/stable/).

This repository contains a simple implementation of these two popular parallel algorithms, a log file parser and a few orchestration shell scripts to run them. There is also a Dockerfile which can be used to quickly spin up a container on a single node for development purposes. The project is under active development as our final project for High Performance Computer Architecture course at 'Università degli Studi di Siena' under Professor Roberto Giorgi.

## Project structure

```
/$HOME/cloud
├── Dockerfile          # Docker image specs
├─┬ core                # Main project folder
│ ├── algos             # Algorithms folder
│ ├── logparsers        # Parser and logs folder
│ └── shscripts         # Shell scripts folder
└── your_machinefile    # Cluster machinefile
```

## Usage

TODO

## License

MIT - see [LICENSE](https://github.com/Nico769/HPCA-Project-Code/blob/master/LICENSE) © Francesco Casciola, Elia Giuseppe Ceroni, Nicola Landolfi