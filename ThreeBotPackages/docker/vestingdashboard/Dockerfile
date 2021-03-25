FROM jssdk:development

LABEL maintainer="rob@threefold.tech"

EXPOSE 443

#Install the Vesting dashboard
RUN poetry run jsng 'j.servers.threebot.default.packages.add(giturl="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/vesting_dashboard")'