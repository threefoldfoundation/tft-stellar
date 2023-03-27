import type { InputValidationsType } from './types';
import { StrKey } from 'stellar-sdk';

export const validateAddress = (
  value: string,
  noAddresses?: boolean,
): InputValidationsType => {
  if (value === '') {
    return {
      isValid: false,
      errorMessage: 'Address is required!',
    };
  }
  if (noAddresses) {
    return {
      isValid: false,
      errorMessage: 'Seems to be no linked address found.',
    };
    // 'Seems to be no linked address found.'
  }
  if (!StrKey.isValidEd25519PublicKey(value)) {
    return {
      isValid: false,
      errorMessage: 'Please enter a valid address.',
    };
  } else {
    return {
      isValid: true,
      errorMessage: '',
    };
  }
};

export const validatePrivateKey = (value: string) => {
  console.log( value );  
  return {
    isValid: true,
    errorMessage: 'Please enter a valid private key.',
  };
};
