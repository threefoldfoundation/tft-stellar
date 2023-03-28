<script lang="ts">
  import Input from '../ui/Input.svelte';
  import Alert from '../ui/Alert.svelte';
  import { validatePrivateKey } from '../../utils/validations';
  import { activatePKStore, alertStore } from '../../utils/stores';
  import { Stellar } from '../../utils/stellar';
  import http from '../../utils/axios';
  import type { UnvestingTransactionModel } from '../../utils/types';
  import { TransactionBuilder, Networks, Keypair } from 'stellar-sdk';

  let privateKeyValue: string;
  let isLoading: boolean;
  let isSigned: boolean;
  const stellar = new Stellar();

  const unvestingTransaction = async (options: UnvestingTransactionModel) => {
    await http
      .post('unvestingtransaction', { vestingaccount: options.address })
      .then(async (res) => {
        if (res && res.data) {
          options.content = res.data;
          const sourceKeypair = Keypair.fromSecret(options.secret);
          const tx = TransactionBuilder.fromXDR(res.data, Networks.TESTNET);
          tx.sign(sourceKeypair);
          try {
            const transactionResult = await stellar.submitTransaction(tx);
            console.log(JSON.stringify(transactionResult, null, 2));
            console.log(
              'Success! View the transaction at: ',
              transactionResult._links.transaction.href,
            );
            alertStore.set({
              message: 'Success! Transaction Submited!',
              className: 'success',
              isOpen: true,
            });
            isLoading = isSigned = false;
          } catch (e) {
            console.log('An error has occured:', e);
            throw Error(e);
          }
        }
      });
  };

  const onKeypress = async (e: { keyCode: number }) => {
    if (e.keyCode === 13) {
      if (validatePrivateKey(privateKeyValue).isValid) {
        isLoading = isSigned = true;
        await stellar.init(privateKeyValue).then(async (address) => {
          if (address != $activatePKStore.ownerAddress) {
            alertStore.set({
              message:
                'The secrest key you provided does not match the selected wallet address.',
              isOpen: true,
              className: 'danger',
            });
          } else {
            $alertStore.isOpen = false;
            const options: UnvestingTransactionModel = {
              secret: privateKeyValue,
              address: $activatePKStore.selectedAddress,
              content: '',
            };
            return await unvestingTransaction(options);
          }
          isLoading = isSigned = false;
        });
      }
    }
  };

  $: privateKeyValue, ((isSigned = false), (isLoading = false));
</script>

<div class="container">
  <div class="lock">
    <div class="alert w-100 mb-4 text-start">
      <h4>Validate Private Key</h4>
      Wallet address :
      <span class="text-primary">
        {$activatePKStore.ownerAddress}
      </span>
      <br />
      Selected Vesting address :
      <span class="text-primary">
        {$activatePKStore.selectedAddress}
      </span>
    </div>
    <div class="row w-100">
      <div class="col-8">
        <Input
          bind:value={privateKeyValue}
          label="Wallet Private Key"
          validation={validatePrivateKey}
          className={'pk-input'}
          bind:isLoading
          onKeyPress={(e) => onKeypress(e)}
        />
        {#if $alertStore.isOpen}
          <div class="mt-4">
            <Alert
              message={$alertStore.message}
              isOpen={$alertStore.isOpen}
              className={$alertStore.className}
            />
          </div>
        {/if}
      </div>
      <div class="col-4">
        {#if isSigned}
          <i class="fa-solid fa-lock-open unlocked" />
        {:else}
          <i class="fa-solid fa-lock locked" />
        {/if}
      </div>
    </div>
  </div>
</div>
