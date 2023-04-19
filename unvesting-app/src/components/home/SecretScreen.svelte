<script lang="ts">
  import Navbar from '../home/Navbar.svelte';
  import Input from '../ui/Input.svelte';
  import { validatePrivateKey } from '../../utils/validations';
  import http from '../../utils/axios';
  import type { UnvestingTransactionModel } from '../../utils/types';
  import { activatePKStore, alertStore } from '../../utils/stores';
  import Alert from '../ui/Alert.svelte';
  import { TransactionBuilder, Networks, Keypair } from 'stellar-sdk';
  import { Stellar } from '../../utils/stellar';

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
          const tx = TransactionBuilder.fromXDR(
            res.data,
            window.config.STELLAR_NETWORK.toLocaleLowerCase() === 'test'
              ? Networks.TESTNET
              : Networks.PUBLIC,
          );
          tx.sign(sourceKeypair);
          try {
            const transactionResult = await stellar.submitTransaction(tx);
            console.log(JSON.stringify(transactionResult, null, 2));
            console.log(
              'Successfully submitted the unvesting transaction: ',
              transactionResult._links.transaction.href,
            );
            alertStore.set({
              message: 'Unvesting succeeded',
              className: 'success',
              isOpen: true,
            });
            isLoading = isSigned = false;
          } catch (e) {
            console.log('An error has occurred:', e);
            throw Error(e);
          }
        }
      })
      .catch((err) => {
        alertStore.set({
          message: err.response.data.error,
          className: 'danger',
          isOpen: true,
        });
        isSigned = isLoading = false;
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
                'The secret you provided does not match the previously entered wallet address',
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

  const unSetAddress = () => {
    return activatePKStore.set({});
  };
  $: disabled = !validatePrivateKey(privateKeyValue).isValid;
</script>

<Navbar />
<div class="container height-100">
  <div class="d-flex justify-content-center align-items-center home-card">
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title d-flex justify-content-center">
          <span class="screen-view-dot">2</span>
          Sign and submit the unvesting transaction
        </h5>
        <hr />
        <small>
          The guardians have prepared and signed an unvesting transaction but it
          still needs your signature.<br />
          The secret is used only on this page to sign the transaction, it is not
          stored nor sent anywhere.
        </small>
        <div class="row">
          <div class="col-12 padding-left-none padding-right-none">
            <Input
              bind:value={privateKeyValue}
              label="Wallet secret"
              validation={validatePrivateKey}
              className={'pk-input'}
              bind:isLoading
              onKeyPress={(e) => onKeypress(e)}
            />
          </div>
        </div>
        {#if $alertStore.isOpen}
          <Alert
            message={$alertStore.message}
            isOpen={$alertStore.isOpen}
            className={$alertStore.className}
          />
        {/if}
        <div class="btns d-flex justify-content-end">
          <button class="btn btn-primary ml-btn-action" on:click={unSetAddress}>
            <i class="fas fa-angle-left" />
            Back
          </button>
          <button
            {disabled}
            on:click={() => {
              onKeypress({ keyCode: 13 });
            }}
            class="btn btn-success ml-btn-action"
          >
            Sign & submit unvesting transaction
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
