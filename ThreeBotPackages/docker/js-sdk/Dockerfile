FROM ubuntu:20.04

LABEL maintainer="rob@threefold.tech"

#Update Ubuntu
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam
RUN apt-get install -y tzdata
RUN apt-get upgrade -y

#install prerequisites
RUN apt-get install -y git python3-venv python3-pip redis restic tmux nginx
RUN pip3 install poetry

#install js-sdk
RUN mkdir /code
WORKDIR /code
# clone the development branch since that one has cors support and stellar sdk 2.10.0
RUN git clone --branch development https://github.com/threefoldtech/js-sdk
WORKDIR /code/js-sdk
RUN poetry install

#prepare the threebot

#Create wallets not to crash the threebot on startup when checking the identity
RUN poetry run jsng 'j.clients.stellar.new("main",network="STD"); j.clients.stellar.main.save()'
RUN poetry run jsng 'j.clients.stellar.new("test",network="TEST"); j.clients.stellar.test.save()'
#Create the default threebot
RUN poetry run jsng 'j.servers.threebot.new("default"); j.servers.threebot.default.save()'

# Start it with the development flag to prevent the threebot from checking the identity
CMD poetry run threebot start --development
