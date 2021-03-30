FROM ubuntu:20.04

LABEL maintainer="rob@threefold.tech"

#Update Ubuntu
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam
RUN apt-get install -y tzdata openssh-client
RUN apt-get upgrade -y


RUN mkdir /data
VOLUME /data

ADD backup.sh /backup.sh
ADD id_rsa /root/.ssh/id_rsa

ARG user
ENV user=$user
ARG server
ENV server=${server}

WORKDIR /
CMD ["/bin/sh", "-c", "ssh $user@$server -o StrictHostKeyChecking=false bash -s < backup.sh > /data/dashboarddata-$(date +\"%y-%m-%d-%H:%M\")"]
