FROM ubuntu:latest

# update the OS
RUN echo "Updating the OS...."
RUN apt update 
RUN apt upgrade -y 

RUN echo "Adding missing software....."
RUN apt-get install -y git python3-venv python3-pip redis-server tmux nginx wget -y

RUN echo "Installing poetry...."
RUN pip3 install poetry 

RUN echo "Installing python"
RUN python3 -m pip install js-sdk 


# update and install the peotry environment + js-sdk
WORKDIR /root
RUN mkdir code
WORKDIR /root/code
RUN mkdir github
WORKDIR /root/code/github
RUN mkdir threefoldtech
WORKDIR /root/code/github/threefoldtech

RUN wget https://github.com/threefoldtech/js-sdk/tarball/master ; tar xvf ./master ; rm master 
RUN cd three*
RUN poetry update 
RUN poetry install
RUN poetry shell
