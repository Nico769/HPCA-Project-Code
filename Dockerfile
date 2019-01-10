FROM python:3.6-jessie

LABEL Nicola Landolfi <nicola.landolfi@student.unisi.it>

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils && \
    apt-get install -y mpich libatlas-base-dev && \
    apt-get clean && apt-get purge && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install numpy mpi4py pandas

CMD ["/bin/bash"]
