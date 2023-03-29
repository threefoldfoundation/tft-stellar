// This file contains any helper function can do some functionality.

const noConfigs = () => {
  throw new Error(
    'Invalid config. Please try to export the `VITE_STELLAR_NETWORK` then run the server.',
  );
};

export const setConfig = () => {
  const network: string =
    import.meta.env.VITE_STELLAR_NETWORK != undefined
      ? import.meta.env.VITE_STELLAR_NETWORK
      : noConfigs();

  switch (network) {
  case 'test':
    window.config = {
      VITE_STELLAR_NETWORK: network,
      STELLAR_HORIZON_URL: 'https://horizon-testnet.stellar.org',
      SERVER_API_URL:
          'https://testnet.threefold.io/threefoldfoundation/vesting_service/',
    };
    break;
  case 'main':
    window.config = {
      VITE_STELLAR_NETWORK: network,
      STELLAR_HORIZON_URL: 'https://horizon.stellar.org',
      SERVER_API_URL:
          'https://tokenservices.threefold.io/threefoldfoundation/vesting_service/',
    };
    break;
  }
};
