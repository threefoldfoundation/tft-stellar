STELLAR_NETWORK="${STELLAR_NETWORK:=test}"

if [ -d dist ]
then
    file="dist/config.js"
else
    file="config.js"
fi

case $STELLAR_NETWORK in
  "test")
    STELLAR_HORIZON_URL="https://horizon-testnet.stellar.org"
    SERVER_API_URL="https://testnet.threefold.io/threefoldfoundation/vesting_service/"
  ;;
  *"main"*)    
    STELLAR_HORIZON_URL="https://horizon.stellar.org"
    SERVER_API_URL="https://tokenservices.threefold.io/threefoldfoundation/vesting_service/"
  ;;
  *)
    echo "Unknown 'STELLAR_NETWORK' selected!, Acceptable networks are [test | main]\n"
    return
  ;;
esac

configs="
window.configs = {
  STELLAR_HORIZON_URL: '$STELLAR_HORIZON_URL',
  SERVER_API_URL: '$SERVER_API_URL',
};
"

if [ -e $file ]
then
    rm $file
fi
echo $configs > $file
echo -e "\e[1;32m$configs"