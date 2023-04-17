import type { InputValidationsType } from './types';
import { StrKey } from 'stellar-sdk';

export const validateAddress = (
  value: string,
  noAddresses?: boolean,
): InputValidationsType => {
  if (value === '') {
    return {
      isValid: false,
      errorMessage: 'Address is required',
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
      errorMessage: 'Invalid address.',
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
      errorMessage: 'Private key is required',
    };
  }
  if (value && value.length < 20) {
    return {
      isValid: false,
      errorMessage: 'A private key should be longer than 20 characters.',
    };
  }
  if (!StrKey.isValidEd25519SecretSeed(value)) {
    return {
      isValid: false,
      errorMessage: 'Invalid private key.',
    };
  }
  return {
    isValid: true,
    errorMessage: '',
  };
};
