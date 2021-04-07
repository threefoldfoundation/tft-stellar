FROM jssdk:development

LABEL maintainer="rob@threefold.tech"

ARG version="master"
ENV version=${version}

#Install the activation service
RUN poetry run jsng "j.servers.threebot.default.packages.add(giturl='https://github.com/threefoldfoundation/tft-stellar/tree/${version}/ThreeBotPackages/activation_service')"

# Install the transaction funding service
RUN poetry run jsng "j.servers.threebot.default.packages.add(giturl='https://github.com/threefoldfoundation/tft-stellar/tree/${version}/ThreeBotPackages/transactionfunding_service')"

# Install the vesting  service
RUN poetry run jsng "j.servers.threebot.default.packages.add(giturl='https://github.com/threefoldfoundation/tft-stellar/tree/${version}/ThreeBotPackages/vesting_service')"

# Install the unlock service
RUN poetry run jsng "j.servers.threebot.default.packages.add(giturl='https://github.com/threefoldfoundation/tft-stellar/tree/${version}/ThreeBotPackages/unlock_service')"

# Start it with the development flag to prevent the threebot from checking the identity
CMD poetry run threebot start --development
