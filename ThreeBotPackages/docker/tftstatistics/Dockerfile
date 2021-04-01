FROM jssdk:development

LABEL maintainer="rob@threefold.tech"

#Install the statistics service
RUN poetry run jsng 'j.servers.threebot.default.packages.add(giturl="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/tft_statistics")'

