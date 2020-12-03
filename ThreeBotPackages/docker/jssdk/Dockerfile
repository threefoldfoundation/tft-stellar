FROM ubuntu:20.04
LABEL maintainer="rob@threefold.tech"

RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam
RUN apt-get install -y tzdata
RUN apt-get upgrade -y

RUN apt-get install -y git python3-venv python3-pip redis-server tmux nginx
RUN pip3 install poetry

RUN mkdir /code
WORKDIR /code
RUN git clone https://github.com/threefoldtech/js-sdk
WORKDIR /code/js-sdk
RUN poetry install
CMD poetry shell
