FROM jssdk:development

LABEL maintainer="rob@threefold.tech"

RUN mkdir /data
VOLUME /data

#Install the statistics service
RUN poetry run jsng 'j.tools.git.ensure_repo("https://github.com/threefoldfoundation/tft-stellar")'

CMD poetry run /root/sandbox/code/github/threefoldfoundation/tft-stellar/ThreeBotPackages/unlock_service/scripts/export.py > /data/public-$(date +"%y-%m-%d-%H:%M")
