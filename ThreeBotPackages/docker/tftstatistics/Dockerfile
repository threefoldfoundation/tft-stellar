FROM ubuntu:20.04

LABEL maintainer="rob@threefold.tech"

# Update Ubuntu
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam
RUN apt-get install -y tzdata
RUN apt-get upgrade -y


# install prerequisites
RUN apt-get install -y git python3-venv python3-pip redis-server tmux nginx
RUN pip3 install poetry


# Copy the source
RUN mkdir -p /code/threefoldfoundation/tft-stellar
COPY ./ThreeBotPackages /code/threefoldfoundation/tft-stellar/ThreeBotPackages

WORKDIR /code/threefoldfoundation/tft-stellar
# install js-sdk
COPY pyproject.toml /code/threefoldfoundation/tft-stellar/
COPY poetry.lock /code/threefoldfoundation/tft-stellar/
RUN poetry install

#Create the default threebot
RUN poetry run jsng 'j.servers.threebot.new("default"); j.servers.threebot.default.save()'

#Install the statistics service
RUN poetry run jsng 'j.servers.threebot.default.packages.add(path="/code/threefoldfoundation/tft-stellar/ThreeBotPackages/tft_statistics")'

# Start it with the development flag to prevent the threebot from checking the identity
CMD poetry run threebot start --development