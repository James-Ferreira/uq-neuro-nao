FROM --platform=amd64 ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# set environment variables that will be used by nao-sdk
ENV PYTHONPATH=${PYTHONPATH}:/nao-sdk/lib/python2.7/site-packages/
ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/nao-sdk

# install required packages & toolsß
RUN apt-get update && apt-get install -y \
python2-minimal \
curl

# install nao sdk
RUN curl -k -L https://community-static.aldebaran.com/resources/2.8.6/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz -o pynaoqi.tar.gz && \
    mkdir nao-sdk && \
    tar -xzf pynaoqi.tar.gz -C nao-sdk --strip-components=1 && \
    rm pynaoqi.tar.gz


# install pip2
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip2.py && \
    python2 get-pip2.py && \
    rm get-pip2.py

# install python requirements
COPY ./requirements-py2.txt /requirements-py2.txt
RUN python2 -m pip install --no-cache-dir -r /requirements-py2.txt
 
RUN apt-get install -y netcat tcpdump