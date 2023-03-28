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
  }
  return {
    isValid: true,
    errorMessage: '',
  };
};

export const validatePrivateKey = (value: string) => {
  if (value === '') {
    return {
      isValid: false,
      errorMessage: 'Private key is required!',
    };
  }
  if (value && value.length < 20) {
    return {
      isValid: false,
      errorMessage: 'Private key should be > 20 char.',
    };
  }
  if (!StrKey.isValidEd25519SecretSeed(value)) {
    return {
      isValid: false,
      errorMessage: 'The private Key seems to be not valid.',
    };
  }
  return {
    isValid: true,
    errorMessage: '',
  };
};
