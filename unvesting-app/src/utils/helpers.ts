// This file contains any helper function can do some functionality.

const noConfigs = () => {
  throw new Error(
    'Invalid config. Set a correct value [test,main] in config.js',
  );
};

export const setConfig = () => {
  const network: string = window.STELLAR_NETWORK

  switch (network) {
    case 'test':
      window.config = {
        STELLAR_NETWORK: network,
        STELLAR_HORIZON_URL: 'https://horizon-testnet.stellar.org',
        SERVER_API_URL:
          'https://testnet.threefold.io/threefoldfoundation/vesting_service/',
      };
      break;
    case 'main':
      window.config = {
        STELLAR_NETWORK: network,
        STELLAR_HORIZON_URL: 'https://horizon.stellar.org',
        SERVER_API_URL:
          'https://tokenservices.threefold.io/threefoldfoundation/vesting_service/',
      };
      break;
    default:
      noConfigs();
  }
};
