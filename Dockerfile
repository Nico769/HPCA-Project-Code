FROM python:3.6-jessie

LABEL maintainer = Nicola Landolfi <nicola.landolfi@student.unisi.it>

COPY requirements.txt /

RUN apt-get update -y && \
    apt-get install -y mpich libatlas-base-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install -r /requirements.txt

COPY core/ /app
WORKDIR /app

CMD ["/bin/bash"]
