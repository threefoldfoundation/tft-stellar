FROM jssdk

LABEL maintainer="rob@threefold.tech"

RUN poetry run jsng 'j.clients.stellar.new("activation_wallet",network="TEST"); j.clients.stellar.activation_wallet.save()'
RUN poetry run jsng 'j.clients.stellar.activation_wallet.activate_through_friendbot()'
#Create a main wallet not to crash the threebot on startup when checking the identity
RUN poetry run jsng 'j.clients.stellar.new("main",network="STD"); j.clients.stellar.main.save()'
#Create the default threebot
RUN poetry run jsng 'j.servers.threebot.new("default"); j.servers.threebot.default.save()'
#Install the activastion service
RUN poetry run jsng 'j.servers.threebot.default.packages.add(giturl="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/activation_service")'

CMD poetry run threebot start --development