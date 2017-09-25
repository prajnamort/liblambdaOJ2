FROM debian:latest

LABEL maintainer "kainwen@gmail.com"

RUN apt-get -y update
RUN apt-get install -y gcc g++ python3 cmake
RUN useradd -ms /bin/bash runoj

WORKDIR /code
ADD . /code/

ENV INSTALL_PREFIX="/usr/local/"
RUN cd /code/python_package && python3 setup.py install
RUN cp /code/tools/docker_judge.py /usr/local/bin/docker_judge \
 && chmod +x /usr/local/bin/docker_judge
