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
            window.config.VITE_STELLAR_NETWORK.toLocaleLowerCase() === 'test'
              ? Networks.TESTNET
              : Networks.PUBLIC,
          );
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
                'The secret you provided does not match the selected wallet address.',
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
      <div class="row g-0">
        <div class="col-md-4">
          <img
            src="assets/Vesting-scheduleblue.png"
            class="img-fluid tf-image rounded-start"
            alt="Vesting-scheduleblue"
          />
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title d-flex justify-content-center">
              <span class="screen-view-dot">2</span>
              Sign and submit unvesting transaction
            </h5>
            <hr />
            <small>
              Please keep in mind that, the secret key is used within the
              browser to sign the transaction, it is not stored anywhere and not
              send anywhere.
            </small>
            <div class="row">
              <div class="col-12 padding-left-none padding-right-none">
                <Input
                  bind:value={privateKeyValue}
                  label="Wallet Private Key"
                  validation={validatePrivateKey}
                  className={'pk-input'}
                  bind:isLoading
                  onKeyPress={(e) => onKeypress(e)}
                  type="password"
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
              <button
                class="btn btn-primary ml-btn-action"
                on:click={unSetAddress}
              >
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
  </div>
</div>
