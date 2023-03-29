export type InputValidationsType = {
  isValid?: boolean;
  errorMessage?: string;
};

export type AlertType = {
  className?: string;
  title?: string;
  message?: string;
  isOpen?: boolean;
};

type VestingAccount = {
  address: string;
};

export type OnResponseVestingAccounts = {
  owner_adress?: string;
  vesting_accounts?: Array<VestingAccount>;
  Error?: string;
};

export type OnSelectAddress = {
  selectedAddress?: string;
  ownerAddress?: string;
  isSelected?: boolean;
};

export type StellarWalletVerifyModel = {
  public_key: string;
  content: string;
  signedContent: string;
};

export type UnvestingTransactionModel = {
  secret: string;
  address: string;
  content: string;
};
